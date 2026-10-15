#!/usr/bin/env python3
"""Run Lab 02: validate the Forward Deployed role charter and RACI matrix."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
ROLES = {
    "fde_lead", "ai_fde", "platform_fde", "security_fde",
    "deployment_strategist", "claims_owner", "adjuster_lead",
}


def incomplete(value: Any) -> bool:
    if isinstance(value, str):
        return not value.strip() or "todo" in value.lower()
    if isinstance(value, list):
        return not value or any(incomplete(item) for item in value)
    if isinstance(value, dict):
        return not value or any(incomplete(item) for item in value.values())
    return value is None


def main() -> int:
    charter = json.loads((ROOT / "role_charter.json").read_text(encoding="utf-8"))
    with (ROOT / "raci_matrix.csv").open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        headers = list(reader.fieldnames or [])
        rows = list(reader)

    errors: list[str] = []
    required = (
        "role_id", "role_name", "mission", "primary_customer", "owned_outcomes",
        "key_activities", "decision_rights", "escalation_paths",
        "success_metrics", "out_of_scope",
    )
    for field in required:
        if field not in charter or incomplete(charter[field]):
            errors.append(f"Role charter field is incomplete: {field}")

    if charter.get("role_id") != "fde_lead":
        errors.append("role_id must be fde_lead")
    if len(charter.get("decision_rights", [])) < 4:
        errors.append("At least four decision rights are required")
    boundaries = " ".join(charter.get("out_of_scope", [])).lower()
    if "claim denials" not in boundaries or "payments" not in boundaries:
        errors.append("The charter must preserve human claim-denial and payment authority")

    if not headers or headers[0] != "work_item" or set(headers[1:]) != ROLES:
        errors.append("RACI headers do not match the required roles")
    if len(rows) != 9:
        errors.append("RACI must contain nine delivery decisions")
    for row in rows:
        values = [row.get(role, "").upper() for role in headers[1:]]
        if values.count("A") != 1:
            errors.append(f"{row.get('work_item')}: exactly one Accountable role is required")
        if "R" not in values:
            errors.append(f"{row.get('work_item')}: at least one Responsible role is required")
        if any(value not in {"R", "A", "C", "I"} for value in values):
            errors.append(f"{row.get('work_item')}: invalid RACI code")
    go_live = next((row for row in rows if "go-live" in row.get("work_item", "").lower()), {})
    if go_live.get("claims_owner") != "A":
        errors.append("Claims owner must be Accountable for production go-live")

    if errors:
        print(f"LAB 02 FAILED — {len(errors)} issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print("LAB 02 PASSED")
    print(f"- Role: {charter['role_name']}")
    print(f"- Owned outcomes: {len(charter['owned_outcomes'])}")
    print(f"- Delivery decisions mapped: {len(rows)}")
    print("- Production go-live authority: Claims Operations Owner")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
