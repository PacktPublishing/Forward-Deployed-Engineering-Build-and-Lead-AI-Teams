#!/usr/bin/env python3
"""Validate Lab 04 production architecture and ADR evidence."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
ARCHITECTURE_FILE = ROOT / "architecture_spec.json"
ADR_FILE = ROOT / "ADR-001-retrieval-first-human-approved-assistant.md"

REQUIRED_COMPONENTS = {
    "adjuster_ui",
    "api_gateway",
    "identity_policy",
    "workflow_orchestrator",
    "retrieval_service",
    "policy_document_store",
    "policy_metadata_index",
    "model_gateway",
    "managed_llm",
    "input_output_guardrails",
    "approval_service",
    "claims_system_adapter",
    "audit_log",
    "telemetry",
    "secrets_manager",
}
EXPECTED_ACTIONS = {"request_evidence", "continue_review", "escalate"}
EXPECTED_ENVIRONMENTS = {"dev", "test", "staging", "prod"}
REQUIRED_OWNERS = {
    "business_owner",
    "user_representative",
    "data_owner",
    "technical_owner",
    "security_approver",
}
REQUIRED_FAILURES = {
    "policy_retrieval_timeout",
    "low_grounding",
    "claims_write_timeout",
    "audit_write_failure",
}
ADR_HEADINGS = {
    "Context",
    "Decision",
    "Decision Drivers",
    "Alternatives Considered",
    "Consequences",
    "Validation and Rollback",
    "Revisit Triggers",
}


def incomplete(value: Any) -> bool:
    """Return True when a required artifact contains blanks or placeholders."""
    if isinstance(value, str):
        normalized = value.strip().lower()
        return not normalized or any(token in normalized for token in ("todo", "tbd", "fixme"))
    if isinstance(value, list):
        return not value or any(incomplete(item) for item in value)
    if isinstance(value, dict):
        return not value or any(incomplete(item) for item in value.values())
    return value is None


def validate_architecture(spec: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required_sections = {
        "metadata",
        "decision_contract",
        "non_functional_requirements",
        "trust_boundaries",
        "components",
        "flows",
        "controls",
        "failure_modes",
        "environments",
        "ownership",
    }
    missing_sections = required_sections - set(spec)
    if missing_sections:
        errors.append("Missing architecture sections: " + ", ".join(sorted(missing_sections)))
        return errors

    for section in required_sections:
        if incomplete(spec[section]):
            errors.append(f"Architecture section is incomplete: {section}")

    contract = spec["decision_contract"]
    if set(contract.get("allowed_recommendations", [])) != EXPECTED_ACTIONS:
        errors.append("Allowed recommendations must remain request_evidence, continue_review, and escalate")

    approval = contract.get("human_approval", {})
    if approval.get("required") is not True:
        errors.append("Protected claim actions must require explicit adjuster approval")
    if approval.get("role") != "Licensed Claims Adjuster":
        errors.append("The approval role must remain Licensed Claims Adjuster")
    if approval.get("enforced_by") != "approval_service":
        errors.append("The approval_service must enforce human approval")
    if approval.get("approval_recorded_before") != "claims_system_adapter":
        errors.append("Approval must be recorded before the claims_system_adapter")

    nfr = spec["non_functional_requirements"]
    exact_thresholds = {
        "citation_completeness_percent_min": 95,
        "protected_action_human_approval_percent": 100,
        "audit_event_completeness_percent": 100,
    }
    for key, expected in exact_thresholds.items():
        if nfr.get(key) != expected:
            errors.append(f"{key} must be {expected}")
    if nfr.get("p95_response_seconds_max", 999) > 12:
        errors.append("p95 response objective cannot exceed 12 seconds")
    if nfr.get("monthly_availability_percent_min", 0) < 99.5:
        errors.append("Monthly availability objective cannot be below 99.5 percent")
    if nfr.get("cost_usd_per_completed_assist_max", 999) > 1.5:
        errors.append("Cost objective cannot exceed $1.50 per completed assist")

    components = spec["components"]
    component_ids = [item.get("id") for item in components]
    if len(component_ids) != len(set(component_ids)):
        errors.append("Component IDs must be unique")
    missing_components = REQUIRED_COMPONENTS - set(component_ids)
    if missing_components:
        errors.append("Missing required components: " + ", ".join(sorted(missing_components)))
    for component in components:
        for field in ("id", "zone", "owner", "responsibility"):
            if incomplete(component.get(field)):
                errors.append(f"Component {component.get('id', '<unknown>')} is missing {field}")

    flows = {flow.get("id"): flow for flow in spec["flows"]}
    known_components = set(component_ids)
    for flow_id, flow in flows.items():
        unknown = set(flow.get("path", [])) - known_components
        if unknown:
            errors.append(f"Flow {flow_id} references unknown components: {', '.join(sorted(unknown))}")

    protected_flow = flows.get("protected_action_execution", {})
    protected_path = protected_flow.get("path", [])
    if protected_flow.get("approval_required") is not True:
        errors.append("The protected action flow must require approval")
    if protected_flow.get("writes_system_of_record") is not True:
        errors.append("The protected action flow must identify its system-of-record write")
    if "approval_service" not in protected_path or "claims_system_adapter" not in protected_path:
        errors.append("The protected action flow must include approval_service and claims_system_adapter")
    elif protected_path.index("approval_service") > protected_path.index("claims_system_adapter"):
        errors.append("approval_service must precede claims_system_adapter")

    assist_flow = flows.get("evidence_assisted_review", {})
    if assist_flow.get("writes_system_of_record") is not False:
        errors.append("The evidence-assisted review flow must not write to the system of record")

    controls = spec["controls"]
    if controls.get("execution", {}).get("direct_model_tool_access") is not False:
        errors.append("The model must not have direct tool access")
    if set(controls.get("execution", {}).get("allowlisted_actions", [])) != EXPECTED_ACTIONS:
        errors.append("Execution allowlist must match the three approved recommendations")
    if controls.get("execution", {}).get("approval_token_required_for_writes") is not True:
        errors.append("System-of-record writes must require an approval token")
    if controls.get("audit", {}).get("audit_failure_behavior") != "fail_closed":
        errors.append("Audit failure behavior must remain fail_closed")
    if controls.get("model", {}).get("training_on_customer_data") is not False:
        errors.append("Customer data must not be used for model training")

    failures = {item.get("id"): item for item in spec["failure_modes"]}
    missing_failures = REQUIRED_FAILURES - set(failures)
    if missing_failures:
        errors.append("Missing failure modes: " + ", ".join(sorted(missing_failures)))
    audit_response = failures.get("audit_write_failure", {}).get("response", "").lower()
    if "fail closed" not in audit_response or "manual" not in audit_response:
        errors.append("Audit failure must fail closed while preserving the manual workflow")

    environments = spec["environments"]
    environment_names = {item.get("name") for item in environments}
    if environment_names != EXPECTED_ENVIRONMENTS:
        errors.append("Environments must be dev, test, staging, and prod")
    if not all(item.get("isolated") is True for item in environments):
        errors.append("Every environment must be isolated")

    if set(spec["ownership"]) != REQUIRED_OWNERS:
        errors.append("All five accountable owner roles are required")

    boundaries = spec["trust_boundaries"]
    if "fraud" not in " ".join(boundaries.get("restricted_data_excluded", [])).lower():
        errors.append("Restricted fraud indicators must remain excluded from the pilot")
    if "deny by default" not in boundaries.get("network_egress", "").lower():
        errors.append("Network egress must be deny by default")

    return errors


def validate_adr(text: str) -> list[str]:
    errors: list[str] = []
    headings = set(re.findall(r"^## (.+)$", text, flags=re.MULTILINE))
    missing = ADR_HEADINGS - headings
    if missing:
        errors.append("ADR is missing headings: " + ", ".join(sorted(missing)))

    required_evidence = {
        "accepted status": "**Status:** Accepted for bounded pilot",
        "retrieval-first decision": "retrieval-first architecture",
        "separate approval path": "separate deterministic approval and execution path",
        "no direct model tools": "no direct access to the claims-system adapter",
        "fail-closed behavior": "fails closed",
        "manual fallback": "manual claims process remains available",
        "rollback trigger": "unauthorized protected action",
        "trade-off": "More components increase latency",
    }
    lower_text = text.lower()
    for label, phrase in required_evidence.items():
        if phrase.lower() not in lower_text:
            errors.append(f"ADR is missing {label}: {phrase}")

    alternatives = re.findall(r"^### (.+)$", text, flags=re.MULTILINE)
    if len(alternatives) < 3:
        errors.append("ADR must compare at least three alternatives")
    return errors


def main() -> int:
    try:
        spec = json.loads(ARCHITECTURE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"LAB 04 FAILED — cannot load architecture_spec.json: {exc}")
        return 1

    try:
        adr = ADR_FILE.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"LAB 04 FAILED — cannot load ADR: {exc}")
        return 1

    errors = validate_architecture(spec) + validate_adr(adr)
    if errors:
        print(f"LAB 04 FAILED — {len(errors)} issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print("LAB 04 PASSED")
    print(f"- Architecture stage: {spec['metadata']['architecture_stage']}")
    print(f"- Components: {len(spec['components'])}; flows: {len(spec['flows'])}")
    print("- Human approval for protected actions: 100%")
    print("- Model direct claims-system access: blocked")
    print(f"- Audit failure behavior: {spec['controls']['audit']['audit_failure_behavior']}")
    print("- ADR status: Accepted for bounded pilot")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
