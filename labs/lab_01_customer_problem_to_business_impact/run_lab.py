#!/usr/bin/env python3
"""Run Lab 01: validate the customer-to-impact map and evaluate pilot evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
STAGES = ("discover", "design", "build", "run", "impact")


def load_json(name: str) -> dict[str, Any]:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def validate(data: dict[str, Any], scenario: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = ("customer_context", "decision", "scope", "baseline", "lifecycle", "outcomes")
    for field in required:
        if field not in data:
            errors.append(f"Missing section: {field}")

    lifecycle = data.get("lifecycle", {})
    for stage in STAGES:
        details = lifecycle.get(stage, {})
        for field in ("owner", "deliverable", "evidence", "exit_criterion"):
            if not details.get(field):
                errors.append(f"{stage}.{field} is required")

    baseline = data.get("baseline", {})
    current = baseline.get("current_value")
    target = baseline.get("target_value")
    if baseline.get("direction") == "decrease" and isinstance(current, (int, float)) and isinstance(target, (int, float)):
        if target >= current:
            errors.append("Target must be lower than the current value")
    expected_target = scenario.get("targets", {}).get("average_handling_time_minutes")
    if target != expected_target:
        errors.append(f"Target must match the customer evidence: {expected_target}")

    boundaries = " ".join(data.get("scope", {}).get("out_of_scope", [])).lower()
    if "deny claims" not in boundaries or "payments" not in boundaries:
        errors.append("Scope must prohibit autonomous denial and payment")

    outcomes = data.get("outcomes", {})
    values = [outcomes.get(key, "") for key in ("technical_output", "customer_outcome", "business_impact")]
    if not all(values) or len({value.lower() for value in values}) != 3:
        errors.append("Technical output, customer outcome, and business impact must be distinct")
    return errors


def evaluate(data: dict[str, Any], pilot: dict[str, Any]) -> tuple[str, list[str]]:
    baseline = data["baseline"]
    guardrail = data["outcomes"]["guardrail"]
    reasons: list[str] = []
    if pilot["sample_size"] < baseline["minimum_pilot_sample_size"]:
        reasons.append("Pilot sample is too small")
        return "continue_pilot", reasons
    if pilot["average_handling_time_minutes"] > baseline["target_value"]:
        reasons.append("Handling-time target was not met")
    if pilot["incorrect_fast_track_rate"] > guardrail["maximum_value"]:
        reasons.append("Incorrect fast-track guardrail was breached")
    return ("scale" if not reasons else "repair_and_retest"), reasons


def main() -> int:
    scenario = load_json("customer_scenario.json")
    lifecycle_map = load_json("lifecycle_map.json")
    pilot = load_json("pilot_results.json")
    errors = validate(lifecycle_map, scenario)
    if errors:
        print(f"LAB 01 FAILED — {len(errors)} issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    decision, reasons = evaluate(lifecycle_map, pilot)
    print("LAB 01 PASSED")
    print(f"- Customer problem: {lifecycle_map['customer_context']['problem_statement']}")
    print(f"- Lifecycle stages: {', '.join(STAGES)}")
    print(f"- Target: {lifecycle_map['baseline']['current_value']} -> {lifecycle_map['baseline']['target_value']} minutes")
    print(f"- Pilot decision: {decision}")
    for reason in reasons:
        print(f"  - {reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
