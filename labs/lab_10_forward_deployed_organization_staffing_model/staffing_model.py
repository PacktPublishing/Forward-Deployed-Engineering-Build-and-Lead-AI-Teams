#!/usr/bin/env python3
"""Validate a forward deployed organization and portfolio staffing model."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
MODEL_FILE = ROOT / "organization_model.json"
PORTFOLIO_FILE = ROOT / "engagement_portfolio.csv"
REPORT_FILE = ROOT / "staffing_plan.md"

FTE_FIELDS = [
    "fde_fte", "ai_fte", "architect_fte", "platform_fte",
    "security_fte", "product_fte", "delivery_fte",
]


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot load {path.name}: {exc}") from exc


def load_portfolio(path: Path) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))
    except OSError as exc:
        raise ValueError(f"Cannot load {path.name}: {exc}") from exc


def validate(
    model: dict[str, Any], rows: list[dict[str, str]]
) -> tuple[dict[str, float], dict[str, float]]:
    errors: list[str] = []
    required_sections = {
        "metadata", "operating_model", "roles", "staffing_rules",
        "governance", "decision_rights", "scaling_triggers",
        "anti_hero_controls", "career_levels",
    }
    missing = required_sections - set(model)
    if missing:
        errors.append("Missing organization sections: " + ", ".join(sorted(missing)))

    role_index = {item.get("id"): item for item in model.get("roles", [])}
    expected_role_ids = {field.removesuffix("_fte") for field in FTE_FIELDS}
    if set(role_index) != expected_role_ids:
        errors.append("Organization roles must match the seven staffing fields")
    if len(role_index) != len(model.get("roles", [])):
        errors.append("Role IDs must be unique")

    expected_columns = {
        "engagement_id", "customer", "phase", "priority", "complexity", "risk",
        "region", "dri", "backup_dri", *FTE_FIELDS,
    }
    if rows and set(rows[0]) != expected_columns:
        errors.append("Engagement-portfolio columns do not match the required schema")
    engagement_ids = [item.get("engagement_id") for item in rows]
    priorities = [item.get("priority") for item in rows]
    if not engagement_ids or len(engagement_ids) != len(set(engagement_ids)):
        errors.append("Engagement IDs must be present and unique")
    if len(priorities) != len(set(priorities)):
        errors.append("Portfolio priorities must be unique")

    demand = {role_id: 0.0 for role_id in expected_role_ids}
    allowed_phases = {"discovery", "design", "build", "pilot", "go_live", "hypercare"}
    for item in rows:
        try:
            complexity = int(item["complexity"])
            risk = int(item["risk"])
            int(item["priority"])
            allocation = {field: float(item[field]) for field in FTE_FIELDS}
        except (KeyError, TypeError, ValueError):
            errors.append(f"{item.get('engagement_id')} has invalid numeric values")
            continue
        if item.get("phase") not in allowed_phases:
            errors.append(f"{item['engagement_id']} has an unsupported phase")
        if complexity not in range(1, 6) or risk not in range(1, 6):
            errors.append(f"{item['engagement_id']} complexity and risk must be 1 through 5")
        if not item.get("dri") or not item.get("backup_dri") or item["dri"] == item["backup_dri"]:
            errors.append(f"{item['engagement_id']} needs different primary and backup DRIs")
        if any(value < 0 for value in allocation.values()):
            errors.append(f"{item['engagement_id']} has negative staffing")
        for field, value in allocation.items():
            demand[field.removesuffix("_fte")] += value
        if risk == 5 and (allocation["architect_fte"] < 0.5 or allocation["security_fte"] < 0.5):
            errors.append(f"{item['engagement_id']} high risk lacks architecture or security coverage")
        if item["phase"] == "go_live" and (allocation["platform_fte"] < 1.0 or allocation["delivery_fte"] < 0.5):
            errors.append(f"{item['engagement_id']} go-live coverage is incomplete")
        if item["phase"] == "discovery" and (allocation["fde_fte"] < 1.0 or allocation["product_fte"] < 0.5):
            errors.append(f"{item['engagement_id']} discovery coverage is incomplete")
        if item["phase"] == "pilot" and (allocation["ai_fte"] < 1.0 or allocation["platform_fte"] < 0.5):
            errors.append(f"{item['engagement_id']} pilot coverage is incomplete")

    utilization: dict[str, float] = {}
    for role_id, role in role_index.items():
        capacity = float(role.get("available_fte", 0))
        target = float(role.get("max_target_utilization_percent", 0))
        if capacity <= 0 or not (0 < target <= 100):
            errors.append(f"{role_id} has invalid capacity or target")
            continue
        utilization[role_id] = round(100 * demand[role_id] / capacity, 2)
        if utilization[role_id] > target:
            errors.append(
                f"{role['title']} utilization {utilization[role_id]:.1f}% "
                f"exceeds target {target:.1f}%"
            )
        if not role.get("accountabilities"):
            errors.append(f"{role['title']} lacks accountabilities")

    required_decisions = {
        "Engagement priority", "Technical standard", "Security exception",
        "Staff reassignment", "Hiring trigger",
    }
    if {item.get("decision") for item in model.get("decision_rights", [])} != required_decisions:
        errors.append("Organization decision rights are incomplete")
    if len(model.get("scaling_triggers", [])) < 5:
        errors.append("At least five scaling triggers are required")
    if len(model.get("anti_hero_controls", [])) < 5:
        errors.append("Anti-hero controls are incomplete")

    if errors:
        raise ValueError("\n".join(f"- {error}" for error in errors))
    return demand, utilization


def build_report(
    model: dict[str, Any],
    rows: list[dict[str, str]],
    demand: dict[str, float],
    utilization: dict[str, float],
    decision: str,
) -> str:
    role_index = {item["id"]: item for item in model["roles"]}
    lines = [
        "# Forward Deployed Organization and Staffing Plan", "",
        f"- **Decision:** {decision}",
        f"- **Planning horizon:** {model['metadata']['planning_horizon']}",
        f"- **Topology:** {model['operating_model']['topology']}", "",
        "## Engagement Portfolio", "",
        "| Priority | Engagement | Phase | DRI | Backup | Risk |",
        "| ---: | --- | --- | --- | --- | ---: |",
    ]
    for item in sorted(rows, key=lambda row: int(row["priority"])):
        lines.append(
            f"| {item['priority']} | {item['customer']} | {item['phase']} | "
            f"{item['dri']} | {item['backup_dri']} | {item['risk']} |"
        )
    lines.extend(["", "## Capacity by Role", "", "| Role | Demand FTE | Available FTE | Utilization | Target |", "| --- | ---: | ---: | ---: | ---: |"])
    for role in model["roles"]:
        role_id = role["id"]
        lines.append(
            f"| {role['title']} | {demand[role_id]:.1f} | "
            f"{float(role['available_fte']):.1f} | {utilization[role_id]:.1f}% | "
            f"{float(role['max_target_utilization_percent']):.1f}% |"
        )
    lines.extend(["", "## Scaling Triggers", ""])
    for item in model["scaling_triggers"]:
        lines.append(f"- **Trigger:** {item['trigger']} **Action:** {item['action']}")
    lines.extend(["", "## Anti-Hero Controls", ""])
    lines.extend(f"- {item}" for item in model["anti_hero_controls"])
    lines.extend(["", "## Governance", ""])
    for item in model["governance"]:
        lines.append(f"- {item['cadence']} — {item['owner']}: {', '.join(item['decisions'])}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    try:
        model = load_json(MODEL_FILE)
        rows = load_portfolio(PORTFOLIO_FILE)
        demand, utilization = validate(model, rows)
        decision = "PORTFOLIO_STAFFED_WITH_GUARDRAILS"
        REPORT_FILE.write_text(
            build_report(model, rows, demand, utilization, decision),
            encoding="utf-8",
        )
    except (KeyError, TypeError, ValueError) as exc:
        print(f"LAB 10 FAILED\n{exc}")
        return 1

    role_index = {item["id"]: item for item in model["roles"]}
    peak_role = max(utilization, key=utilization.get)
    print("LAB 10 PASSED")
    print(f"- Decision: {decision}")
    print(f"- Engagements staffed: {len(rows)}")
    print(f"- Role pools: {len(role_index)}")
    print(f"- Peak utilization: {role_index[peak_role]['title']} {utilization[peak_role]:.1f}%")
    print("- Overallocated roles: 0")
    print(f"- Report: {REPORT_FILE.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
