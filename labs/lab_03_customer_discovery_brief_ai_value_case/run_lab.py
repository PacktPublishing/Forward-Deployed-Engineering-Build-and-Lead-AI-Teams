#!/usr/bin/env python3
"""Run Lab 03: validate the discovery brief and AI value hypothesis."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
OWNER_ROLES = {
    "business_owner", "user_representative", "data_owner",
    "technical_owner", "security_approver",
}
METRICS = {
    "median_intake_to_assignment_hours",
    "intake_rework_rate_percent",
    "citation_completeness_percent",
    "human_approval_rate_percent",
    "weekly_active_adjusters_percent",
}


def incomplete(value: Any) -> bool:
    if isinstance(value, str):
        return not value.strip() or any(token in value.lower() for token in ("todo", "tbd"))
    if isinstance(value, list):
        return not value or any(incomplete(item) for item in value)
    if isinstance(value, dict):
        return not value or any(incomplete(item) for item in value.values())
    return value is None


def main() -> int:
    brief = json.loads((ROOT / "discovery_brief.json").read_text(encoding="utf-8"))
    with (ROOT / "value_hypothesis.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    errors: list[str] = []
    required = (
        "engagement", "problem", "decision_contract", "ai_fit", "data_readiness",
        "pilot", "governance", "risks", "discovery_exit_criteria", "recommendation",
    )
    for section in required:
        if section not in brief or incomplete(brief[section]):
            errors.append(f"Discovery section is incomplete: {section}")

    owners = brief.get("governance", {}).get("owners", {})
    if set(owners) != OWNER_ROLES:
        errors.append("All five governance owners are required")
    approval = brief.get("governance", {}).get("human_approval", {})
    if approval.get("required") is not True:
        errors.append("Human approval must remain required")
    protected = " ".join(approval.get("protected_actions", [])).lower()
    if "approve or deny" not in protected or "payment" not in protected:
        errors.append("Protected claim decisions and payment must remain human-controlled")

    ids = {row.get("metric_id", "") for row in rows}
    if ids != METRICS:
        errors.append("The value hypothesis must contain the five required metrics")
    human = next((row for row in rows if row.get("metric_id") == "human_approval_rate_percent"), {})
    if human.get("baseline") != "100" or human.get("target") != "100":
        errors.append("Human approval baseline and target must both be 100 percent")
    for row in rows:
        try:
            baseline = float(row["baseline"])
            target = float(row["target"])
        except (KeyError, ValueError):
            errors.append(f"{row.get('metric_id', 'metric')}: baseline and target must be numeric")
            continue
        direction = row.get("direction")
        if direction == "lower" and target >= baseline:
            errors.append(f"{row['metric_id']}: target must be lower than baseline")
        if direction == "higher" and target <= baseline:
            errors.append(f"{row['metric_id']}: target must be higher than baseline")
        if direction == "equal" and target != baseline:
            errors.append(f"{row['metric_id']}: target must equal baseline")

    if errors:
        print(f"LAB 03 FAILED — {len(errors)} issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print("LAB 03 PASSED")
    print(f"- Recommendation: {brief['recommendation']['decision']}")
    print(f"- Metrics: {len(rows)}")
    print(f"- Risks: {len(brief['risks'])}")
    print(f"- Pilot: {brief['pilot']['duration_weeks']} weeks, {brief['pilot']['teams']} teams, {brief['pilot']['maximum_claims']} claims maximum")
    print("- Human approval for protected actions: 100%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
