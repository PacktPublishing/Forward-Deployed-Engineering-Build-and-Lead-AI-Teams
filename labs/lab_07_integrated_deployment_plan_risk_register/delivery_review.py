#!/usr/bin/env python3
"""Validate an integrated deployment plan and generate its delivery review."""

from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
PLAN_FILE = ROOT / "deployment_plan.json"
RISK_FILE = ROOT / "risk_register.csv"
REPORT_FILE = ROOT / "deployment_review.md"


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot load {path.name}: {exc}") from exc


def load_risks(path: Path) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))
    except OSError as exc:
        raise ValueError(f"Cannot load {path.name}: {exc}") from exc


def validate(plan: dict[str, Any], risks: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    required_sections = {
        "metadata", "scope", "workstreams", "milestones", "critical_path",
        "decision_rights", "delivery_cadence", "cutover", "hypercare", "handoff",
    }
    missing = required_sections - set(plan)
    if missing:
        errors.append("Missing plan sections: " + ", ".join(sorted(missing)))

    milestones = plan.get("milestones", [])
    milestone_ids = [item.get("id") for item in milestones]
    if not milestone_ids or len(milestone_ids) != len(set(milestone_ids)):
        errors.append("Milestone IDs must be present and unique")
    milestone_index = {item["id"]: item for item in milestones if item.get("id")}
    positions = {milestone_id: index for index, milestone_id in enumerate(milestone_ids)}
    for milestone in milestones:
        try:
            date.fromisoformat(milestone["target_date"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"{milestone.get('id')} has an invalid target date")
        if not milestone.get("dri") or not milestone.get("exit_evidence"):
            errors.append(f"{milestone.get('id')} needs a DRI and exit evidence")
        for dependency in milestone.get("depends_on", []):
            if dependency not in milestone_index:
                errors.append(f"{milestone.get('id')} references unknown dependency {dependency}")
            elif positions[dependency] >= positions[milestone["id"]]:
                errors.append(f"{milestone['id']} dependency {dependency} is not earlier")

    workstreams = plan.get("workstreams", [])
    for workstream in workstreams:
        if not workstream.get("owner"):
            errors.append(f"{workstream.get('id')} has no owner")
        unknown = set(workstream.get("milestone_ids", [])) - set(milestone_ids)
        if unknown:
            errors.append(f"{workstream.get('id')} references unknown milestones")

    critical_path = plan.get("critical_path", [])
    if not critical_path or set(critical_path) - set(milestone_ids):
        errors.append("Critical path must use known milestones")

    required_decisions = {"scope", "architecture", "security", "go_live", "incident"}
    decisions = {item.get("decision") for item in plan.get("decision_rights", [])}
    if decisions != required_decisions:
        errors.append("Decision rights must cover scope architecture security go_live and incident")

    cutover = plan.get("cutover", {})
    if not cutover.get("steps") or not cutover.get("abort_conditions") or not cutover.get("rollback_action"):
        errors.append("Cutover requires steps abort conditions and rollback")
    handoff = plan.get("handoff", {})
    if not handoff.get("receiving_owner") or not handoff.get("acceptance_criteria"):
        errors.append("Handoff requires a receiving owner and acceptance criteria")

    required_risk_fields = {
        "risk_id", "category", "description", "probability", "impact", "score",
        "owner", "response", "trigger", "contingency", "status",
    }
    if risks and set(risks[0]) != required_risk_fields:
        errors.append("Risk-register columns do not match the required schema")
    risk_ids = [item.get("risk_id") for item in risks]
    if not risk_ids or len(risk_ids) != len(set(risk_ids)):
        errors.append("Risk IDs must be present and unique")
    for risk in risks:
        try:
            probability = int(risk["probability"])
            impact = int(risk["impact"])
            score = int(risk["score"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"{risk.get('risk_id')} has invalid numeric scoring")
            continue
        if probability not in range(1, 6) or impact not in range(1, 6):
            errors.append(f"{risk['risk_id']} probability and impact must be 1 through 5")
        if score != probability * impact:
            errors.append(f"{risk['risk_id']} score does not equal probability times impact")
        if not risk.get("owner") or not risk.get("trigger") or not risk.get("contingency"):
            errors.append(f"{risk['risk_id']} lacks ownership trigger or contingency")
        if risk.get("response") not in {"AVOID", "MITIGATE", "TRANSFER", "ACCEPT"}:
            errors.append(f"{risk['risk_id']} has an invalid response")
        if score >= 15 and risk.get("status") == "OPEN":
            errors.append(f"{risk['risk_id']} is an unresolved blocking risk")
    if errors:
        raise ValueError("\n".join(f"- {error}" for error in errors))
    return [risk["risk_id"] for risk in risks if int(risk["score"]) >= 15 and risk["status"] == "OPEN"]


def build_report(plan: dict[str, Any], risks: list[dict[str, str]], decision: str) -> str:
    lines = [
        "# Enterprise AI Claims Assistant — Integrated Deployment Review", "",
        f"- **Decision:** {decision}",
        f"- **Target go-live:** {plan['metadata']['target_go_live']}",
        f"- **Objective:** {plan['scope']['objective']}", "",
        "## Workstreams", "",
        "| Workstream | Owner | Milestones |", "| --- | --- | --- |",
    ]
    for item in plan["workstreams"]:
        lines.append(f"| {item['name']} | {item['owner']} | {', '.join(item['milestone_ids'])} |")
    lines.extend(["", "## Milestones", "", "| ID | Milestone | Target | DRI | Dependencies |", "| --- | --- | --- | --- | --- |"])
    for item in plan["milestones"]:
        dependencies = ", ".join(item["depends_on"]) or "None"
        lines.append(f"| {item['id']} | {item['name']} | {item['target_date']} | {item['dri']} | {dependencies} |")
    lines.extend(["", "## Critical Path", "", " → ".join(plan["critical_path"]), "", "## Risk Register", "", "| Risk | Score | Owner | Response | Status | Contingency |", "| --- | ---: | --- | --- | --- | --- |"])
    for risk in sorted(risks, key=lambda item: int(item["score"]), reverse=True):
        lines.append(f"| {risk['risk_id']} | {risk['score']} | {risk['owner']} | {risk['response']} | {risk['status']} | {risk['contingency']} |")
    lines.extend(["", "## Cutover and Rollback", ""])
    lines.extend(f"{index}. {step}" for index, step in enumerate(plan["cutover"]["steps"], start=1))
    lines.extend(["", "**Abort conditions:**", ""])
    lines.extend(f"- {item}" for item in plan["cutover"]["abort_conditions"])
    lines.extend(["", f"**Rollback:** {plan['cutover']['rollback_action']}", "", "## Handoff", "", f"- Receiving owner: {plan['handoff']['receiving_owner']}"])
    lines.extend(f"- Acceptance: {item}" for item in plan["handoff"]["acceptance_criteria"])
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    try:
        plan = load_json(PLAN_FILE)
        risks = load_risks(RISK_FILE)
        blocking = validate(plan, risks)
        decision = "PLAN_READY_FOR_EXECUTION" if not blocking else "HOLD_FOR_REMEDIATION"
        REPORT_FILE.write_text(build_report(plan, risks, decision), encoding="utf-8")
    except (KeyError, TypeError, ValueError) as exc:
        print(f"LAB 07 FAILED\n{exc}")
        return 1

    print("LAB 07 PASSED")
    print(f"- Decision: {decision}")
    print(f"- Milestones: {len(plan['milestones'])}")
    print(f"- Workstreams: {len(plan['workstreams'])}")
    print(f"- Risks: {len(risks)}")
    print(f"- Unresolved blocking risks: {len(blocking)}")
    print(f"- Report: {REPORT_FILE.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
