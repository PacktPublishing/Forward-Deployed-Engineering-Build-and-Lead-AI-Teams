#!/usr/bin/env python3
"""Evaluate productization and reusability decisions from portfolio evidence."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
POLICY_FILE = ROOT / "productization_policy.json"
MATRIX_FILE = ROOT / "productization_matrix.csv"
REPORT_FILE = ROOT / "productization_review.md"


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot load {path.name}: {exc}") from exc


def load_matrix(path: Path) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))
    except OSError as exc:
        raise ValueError(f"Cannot load {path.name}: {exc}") from exc


def score(item: dict[str, str]) -> int:
    return (
        2 * int(item["reuse_demand"])
        + 2 * int(item["standardization"])
        + int(item["strategic_fit"])
        - int(item["customer_coupling"])
        - int(item["security_variance"])
        - int(item["maintenance_burden"])
    )


def expected_decision(policy: dict[str, Any], item: dict[str, str], item_score: int) -> str:
    if item["lifecycle_status"] == "retire":
        return "RETIRE"
    for threshold in policy["decision_thresholds"]:
        if threshold["minimum_score"] <= item_score <= threshold["maximum_score"]:
            return threshold["decision"]
    raise ValueError(f"No decision threshold covers score {item_score}")


def validate(
    policy: dict[str, Any], rows: list[dict[str, str]]
) -> list[dict[str, Any]]:
    errors: list[str] = []
    required_sections = {
        "metadata", "scales", "scoring_formula", "decision_thresholds",
        "overrides", "decision_definitions", "portfolio_rules",
        "review_cadence", "accountable_roles",
    }
    missing = required_sections - set(policy)
    if missing:
        errors.append("Missing policy sections: " + ", ".join(sorted(missing)))

    expected_columns = {
        "item_id", "capability", "reuse_demand", "standardization",
        "strategic_fit", "customer_coupling", "security_variance",
        "maintenance_burden", "lifecycle_status", "proposed_decision",
        "owner", "evidence",
    }
    if rows and set(rows[0]) != expected_columns:
        errors.append("Decision-matrix columns do not match the required schema")
    ids = [item.get("item_id") for item in rows]
    if not ids or len(ids) != len(set(ids)):
        errors.append("Item IDs must be present and unique")

    reviewed: list[dict[str, Any]] = []
    allowed_decisions = set(policy.get("decision_definitions", {}))
    for item in rows:
        try:
            numeric_values = [
                int(item[field])
                for field in [
                    "reuse_demand", "standardization", "strategic_fit",
                    "customer_coupling", "security_variance", "maintenance_burden",
                ]
            ]
        except (KeyError, TypeError, ValueError):
            errors.append(f"{item.get('item_id')} contains invalid scoring data")
            continue
        if any(value not in range(1, 6) for value in numeric_values):
            errors.append(f"{item['item_id']} scores must be integers 1 through 5")
        item_score = score(item)
        calculated = expected_decision(policy, item, item_score)
        if item.get("proposed_decision") not in allowed_decisions:
            errors.append(f"{item['item_id']} has an unsupported decision")
        if item.get("proposed_decision") != calculated:
            errors.append(
                f"{item['item_id']} proposes {item.get('proposed_decision')} "
                f"but the policy calculates {calculated}"
            )
        if not item.get("owner") or not item.get("evidence"):
            errors.append(f"{item['item_id']} needs an owner and evidence")
        if calculated == "CUSTOM_EXTENSION" and "review date" not in item["evidence"].lower():
            errors.append(f"{item['item_id']} custom extension needs a dated review")
        if calculated == "RETIRE" and "archive" not in item["evidence"].lower():
            errors.append(f"{item['item_id']} retirement needs a removal or archive action")
        if calculated in {"PRODUCT", "PLATFORM"} and int(item["reuse_demand"]) < 4:
            errors.append(f"{item['item_id']} lacks repeated demand for {calculated}")
        reviewed.append({**item, "score": item_score, "calculated_decision": calculated})

    if errors:
        raise ValueError("\n".join(f"- {error}" for error in errors))
    return reviewed


def build_report(
    policy: dict[str, Any], reviewed: list[dict[str, Any]], decision: str
) -> str:
    counts = Counter(item["calculated_decision"] for item in reviewed)
    lines = [
        "# Enterprise AI Claims Assistant — Productization and Reusability Review", "",
        f"- **Decision:** {decision}",
        f"- **Scope:** {policy['metadata']['portfolio_scope']}", "",
        "## Decision Matrix", "",
        "| Item | Capability | Score | Decision | Owner |",
        "| --- | --- | ---: | --- | --- |",
    ]
    for item in sorted(reviewed, key=lambda row: row["score"], reverse=True):
        lines.append(
            f"| {item['item_id']} | {item['capability']} | {item['score']} | "
            f"{item['calculated_decision']} | {item['owner']} |"
        )
    lines.extend(["", "## Portfolio Mix", ""])
    for label in ["PRODUCT", "PLATFORM", "CONFIGURATION", "CUSTOM_EXTENSION", "RETIRE"]:
        lines.append(f"- {label}: {counts.get(label, 0)}")
    lines.extend(["", "## Decision Definitions", ""])
    for label, definition in policy["decision_definitions"].items():
        lines.append(f"- **{label}:** {definition}")
    lines.extend(["", "## Guardrails", ""])
    lines.extend(f"- {rule}" for rule in policy["portfolio_rules"])
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    try:
        policy = load_json(POLICY_FILE)
        rows = load_matrix(MATRIX_FILE)
        reviewed = validate(policy, rows)
        decision = "PORTFOLIO_PLAN_APPROVED"
        REPORT_FILE.write_text(build_report(policy, reviewed, decision), encoding="utf-8")
    except (KeyError, TypeError, ValueError) as exc:
        print(f"LAB 09 FAILED\n{exc}")
        return 1

    counts = Counter(item["calculated_decision"] for item in reviewed)
    print("LAB 09 PASSED")
    print(f"- Decision: {decision}")
    print(f"- Components reviewed: {len(reviewed)}")
    print(f"- Product candidates: {counts['PRODUCT']}")
    print(f"- Platform candidates: {counts['PLATFORM']}")
    print(f"- Custom extensions: {counts['CUSTOM_EXTENSION']}")
    print(f"- Retirements: {counts['RETIRE']}")
    print(f"- Report: {REPORT_FILE.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
