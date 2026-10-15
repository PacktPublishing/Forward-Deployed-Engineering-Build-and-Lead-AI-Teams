#!/usr/bin/env python3
"""Validate a threat model and generate an auditable production-readiness decision."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
THREAT_MODEL_FILE = ROOT / "threat_model.json"
CHECKLIST_FILE = ROOT / "production_readiness_checklist.json"
REPORT_FILE = ROOT / "production_readiness_report.md"

REQUIRED_THREAT_CATEGORIES = {
    "prompt_injection", "tool_abuse", "data_exfiltration", "retrieval_integrity",
    "identity_tenant_isolation", "secrets", "transaction_integrity", "audit",
    "change_management", "denial_of_service",
}
REQUIRED_CHECKLIST_CATEGORIES = {
    "identity_access", "data_protection", "model_tool_guardrails",
    "environments_delivery", "observability_audit", "reliability_recovery",
    "operations_governance",
}


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON artifact with a useful file-specific error."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot load {path.name}: {exc}") from exc


def unique_index(items: list[dict[str, Any]], label: str) -> dict[str, dict[str, Any]]:
    """Index records by unique, non-empty ID."""
    identifiers = [item.get("id") for item in items]
    if any(not identifier for identifier in identifiers):
        raise ValueError(f"{label} must have non-empty IDs")
    if len(identifiers) != len(set(identifiers)):
        raise ValueError(f"{label} IDs must be unique")
    return {item["id"]: item for item in items}


def flatten_checklist(checklist: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    """Return every readiness item while preserving its category."""
    return [
        {**item, "category": category}
        for category, items in checklist.items()
        for item in items
    ]


def validate_inputs(
    model: dict[str, Any], readiness: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    """Validate traceability, ownership, evidence, and release boundaries."""
    errors: list[str] = []
    required_model_sections = {
        "metadata", "decision_boundary", "assets", "trust_boundaries",
        "controls", "threats", "risk_policy",
    }
    missing_model_sections = required_model_sections - set(model)
    if missing_model_sections:
        errors.append("Missing threat-model sections: " + ", ".join(sorted(missing_model_sections)))

    checklist_doc = readiness.get("checklist", {})
    missing_checklist_categories = REQUIRED_CHECKLIST_CATEGORIES - set(checklist_doc)
    extra_checklist_categories = set(checklist_doc) - REQUIRED_CHECKLIST_CATEGORIES
    if missing_checklist_categories:
        errors.append("Missing checklist categories: " + ", ".join(sorted(missing_checklist_categories)))
    if extra_checklist_categories:
        errors.append("Unknown checklist categories: " + ", ".join(sorted(extra_checklist_categories)))

    try:
        assets = unique_index(model.get("assets", []), "Asset")
        boundaries = unique_index(model.get("trust_boundaries", []), "Trust boundary")
        controls = unique_index(model.get("controls", []), "Control")
        threats = list(unique_index(model.get("threats", []), "Threat").values())
        checklist_items = flatten_checklist(checklist_doc)
        unique_index(checklist_items, "Checklist item")
    except ValueError as exc:
        errors.append(str(exc))
        assets, boundaries, controls, threats, checklist_items = {}, {}, {}, [], []

    observed_categories = {threat.get("category") for threat in threats}
    missing_threat_categories = REQUIRED_THREAT_CATEGORIES - observed_categories
    if missing_threat_categories:
        errors.append("Missing threat categories: " + ", ".join(sorted(missing_threat_categories)))

    evidence_ids = [item.get("evidence_id") for item in checklist_items]
    if any(not evidence_id for evidence_id in evidence_ids):
        errors.append("Every checklist item must have an evidence_id")
    if len(evidence_ids) != len(set(evidence_ids)):
        errors.append("Checklist evidence IDs must be unique")
    evidence_set = set(evidence_ids)

    for control in controls.values():
        if control.get("status") != "implemented":
            errors.append(f"{control['id']} is not implemented")
        if not control.get("owner"):
            errors.append(f"{control['id']} has no owner")
        unknown_evidence = set(control.get("evidence_ids", [])) - evidence_set
        if unknown_evidence:
            errors.append(f"{control['id']} references unknown evidence: " + ", ".join(sorted(unknown_evidence)))

    for threat in threats:
        if set(threat.get("asset_ids", [])) - set(assets):
            errors.append(f"{threat['id']} references unknown assets")
        if set(threat.get("trust_boundary_ids", [])) - set(boundaries):
            errors.append(f"{threat['id']} references unknown trust boundaries")
        if set(threat.get("control_ids", [])) - set(controls):
            errors.append(f"{threat['id']} references unknown controls")
        if set(threat.get("verification_evidence_ids", [])) - evidence_set:
            errors.append(f"{threat['id']} references unknown verification evidence")
        if not threat.get("owner"):
            errors.append(f"{threat['id']} has no risk owner")
        if threat.get("residual_risk") in {"critical", "high"}:
            errors.append(f"{threat['id']} retains blocking residual risk")
        if threat.get("disposition") != "MITIGATE":
            errors.append(f"{threat['id']} lacks a MITIGATE disposition")

    mapped_controls = {control_id for item in checklist_items for control_id in item.get("control_ids", [])}
    if mapped_controls - set(controls):
        errors.append("Checklist references unknown controls: " + ", ".join(sorted(mapped_controls - set(controls))))
    if set(controls) - mapped_controls:
        errors.append("Controls without readiness evidence: " + ", ".join(sorted(set(controls) - mapped_controls)))

    for item in checklist_items:
        if item.get("status") not in {"PASS", "HOLD", "FAIL"}:
            errors.append(f"{item.get('id')} has an invalid status")
        if item.get("blocking") is not True:
            errors.append(f"{item.get('id')} must be an explicit blocking check")
        if not item.get("owner") or not item.get("evidence"):
            errors.append(f"{item.get('id')} needs an owner and concrete evidence")

    decision_boundary = model.get("decision_boundary", {})
    if decision_boundary.get("autonomous_protected_actions_allowed") is not False:
        errors.append("Autonomous protected actions must be prohibited")
    if len(decision_boundary.get("protected_actions", [])) < 3:
        errors.append("Protected action boundary is incomplete")

    pilot = readiness.get("pilot_boundary", {})
    if pilot.get("manual_workflow_available") is not True:
        errors.append("The manual claims workflow must remain available")
    if not pilot.get("feature_flag"):
        errors.append("The bounded pilot requires a feature flag")

    expected_roles = {"Business Owner", "Technical Owner", "Security Approver", "Operations Owner"}
    if {item.get("role") for item in readiness.get("approvers", [])} != expected_roles:
        errors.append("Business, technical, security, and operations approvers are required")

    open_exceptions = [
        item for item in readiness.get("exceptions", [])
        if item.get("status") == "OPEN" and item.get("risk_acceptance") != "APPROVED"
    ]
    if open_exceptions:
        errors.append("Open unaccepted production exceptions remain")

    if errors:
        raise ValueError("\n".join(f"- {error}" for error in errors))
    return threats, checklist_items, sorted(mapped_controls)


def decision_for(
    threats: list[dict[str, Any]],
    checklist_items: list[dict[str, Any]],
    approvers: list[dict[str, Any]],
) -> str:
    """Fail closed unless every blocking item and required approval passes."""
    checks_pass = all(item["status"] == "PASS" for item in checklist_items if item["blocking"])
    risks_acceptable = all(threat["residual_risk"] in {"low", "medium"} for threat in threats)
    approvals_complete = bool(approvers) and all(item.get("approved") is True for item in approvers)
    return "READY_FOR_BOUNDED_PILOT" if checks_pass and risks_acceptable and approvals_complete else "HOLD_FOR_REMEDIATION"


def build_report(
    model: dict[str, Any],
    readiness: dict[str, Any],
    threats: list[dict[str, Any]],
    checklist_items: list[dict[str, Any]],
    mapped_controls: list[str],
    decision: str,
) -> str:
    """Render the auditable threat and readiness review."""
    risk_counts = Counter(threat["inherent_risk"] for threat in threats)
    lines = [
        "# Enterprise AI Claims Assistant — Threat Model and Production Readiness",
        "",
        f"- **Decision:** {decision}",
        f"- **Candidate:** {readiness['metadata']['candidate']}",
        f"- **Target:** {readiness['metadata']['target_environment']}",
        f"- **Review date:** {readiness['metadata']['review_date']}",
        "",
        "## Decision Boundary",
        "",
        f"- Primary user: {model['decision_boundary']['primary_user']}",
        "- The assistant may retrieve policy evidence, summarize with citations, and recommend an allowed next step.",
        "- Claim adjudication, payment, reserve changes, customer communication, and claims-system writes remain protected human actions.",
        "",
        "## Threat Summary",
        "",
        f"- Threats reviewed: {len(threats)}",
        f"- Inherent risk: {risk_counts.get('critical', 0)} critical, {risk_counts.get('high', 0)} high, {risk_counts.get('medium', 0)} medium",
        f"- Controls traced to readiness evidence: {len(mapped_controls)}/{len(model['controls'])}",
        "",
        "| Threat | Category | Inherent | Residual | Owner | Controls |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for threat in threats:
        lines.append(
            f"| {threat['id']} | {threat['category']} | {threat['inherent_risk']} | "
            f"{threat['residual_risk']} | {threat['owner']} | {', '.join(threat['control_ids'])} |"
        )

    lines.extend([
        "", "## Production-Readiness Checklist", "",
        "| Category | Check | Status | Owner | Evidence ID |",
        "| --- | --- | --- | --- | --- |",
    ])
    for item in checklist_items:
        lines.append(
            f"| {item['category']} | {item['id']} | {item['status']} | "
            f"{item['owner']} | {item['evidence_id']} |"
        )

    lines.extend(["", "## Version Manifest", "", "| Artifact | Version |", "| --- | --- |"])
    for name, version in readiness["version_manifest"].items():
        lines.append(f"| {name.replace('_', ' ').title()} | {version} |")

    lines.extend(["", "## Required Approvals", ""])
    for approver in readiness["approvers"]:
        state = "Approved" if approver["approved"] else "Pending"
        lines.append(f"- {state} — {approver['role']}: {approver['name']}")

    pilot = readiness["pilot_boundary"]
    lines.extend([
        "", "## Bounded Pilot and Recovery", "",
        f"- Cohort: {pilot['cohort']}",
        f"- Maximum volume: {pilot['maximum_claims']} claims",
        f"- Duration: {pilot['duration_days']} days",
        f"- Feature flag: {pilot['feature_flag']}",
        "- Manual workflow remains available: yes",
        "", "### Rollback triggers", "",
    ])
    lines.extend(f"- {trigger}" for trigger in readiness["rollback_triggers"])
    lines.extend(["", f"**Rollback action:** {readiness['rollback_action']}", ""])
    return "\n".join(lines)


def main() -> int:
    try:
        model = load_json(THREAT_MODEL_FILE)
        readiness = load_json(CHECKLIST_FILE)
        threats, checklist_items, mapped_controls = validate_inputs(model, readiness)

        blocking_failures = [
            item["id"] for item in checklist_items
            if item["blocking"] and item["status"] != "PASS"
        ]
        if blocking_failures:
            raise ValueError("Blocking checks not passed: " + ", ".join(blocking_failures))

        pending_approvals = [
            item["role"] for item in readiness["approvers"]
            if item.get("approved") is not True
        ]
        if pending_approvals:
            raise ValueError("Pending approvals: " + ", ".join(pending_approvals))

        decision = decision_for(threats, checklist_items, readiness["approvers"])
        report = build_report(model, readiness, threats, checklist_items, mapped_controls, decision)
        REPORT_FILE.write_text(report, encoding="utf-8")
    except (KeyError, TypeError, ValueError) as exc:
        print(f"LAB 06 FAILED\n{exc}")
        return 1

    blocking_count = sum(item["blocking"] for item in checklist_items)
    print("LAB 06 PASSED")
    print(f"- Decision: {decision}")
    print(f"- Threats reviewed: {len(threats)}")
    print(f"- Controls traced: {len(mapped_controls)}/{len(model['controls'])}")
    print(f"- Blocking checks passed: {blocking_count}/{blocking_count}")
    print(f"- Report: {REPORT_FILE.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
