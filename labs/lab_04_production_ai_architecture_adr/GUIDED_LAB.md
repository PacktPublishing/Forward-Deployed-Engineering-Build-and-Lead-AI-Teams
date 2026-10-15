# Lab 04 — Create a Production AI Architecture and Architecture Decision Record

## Goal

Translate the Enterprise AI Claims Assistant’s workflow, data, security, reliability, cost, and human-approval requirements into a production architecture and a defensible Architecture Decision Record (ADR).

## What You'll Build or Produce

In your own project directory, you will create:

- `architecture_spec.json` — the production architecture’s decision contract, measurable requirements, trust boundaries, components, flows, controls, failure modes, environments, and owners.
- `ADR-001-retrieval-first-human-approved-assistant.md` — the selected design, alternatives, consequences, validation evidence, rollback, and revisit triggers.
- `run_lab.py` — the learner-built architecture validator that enforces component, flow, approval, access, audit, and ADR requirements.

The completed course repository contains the finished version of these same three project files. Use it only when stuck or comparing your result.

## Estimated Time

60–80 minutes.

## Cost Guardrails

This design lab runs locally and costs $0. Do not provision cloud resources, call a model API, upload claim data, or use customer credentials.

## Completion Evidence

You are finished when `run_lab.py` compiles and confirms 15 components and four flows, the approval service precedes the claims adapter, direct model tool access is blocked, audit failure is fail-closed, the ADR contains all decision sections, and your own Git working tree is clean.

## Prerequisites

- Python 3.10 or later for JSON and evidence checks.
- Git, a terminal, and a text editor.
- Basic JSON and Markdown familiarity.
- An understanding of retrieval, deterministic controls, human approval, SLOs, and environment promotion.

## Where This Lab Fits

This lab translates the approved discovery and value case into a production design. The new skill is separating probabilistic AI assistance from deterministic approval and execution while making reliability, security, cost, ownership, and rollback visible. You are designing the system that Lab 05 will build and evaluate.

## Step 1 — Create Your Independent Project

```bash
mkdir fde_lab_04
cd fde_lab_04
```

Do not edit the completed reference repository. Build the architecture and ADR from this guide; compare with the reference only when needed.

### Verification checkpoint

- **Expected result:** You are inside an empty `fde_lab_04` directory.
- **Acceptable variation:** Another directory name is acceptable.
- **Failure indicator:** You are changing files inside `lab_04_production_ai_architecture_adr`.
- **Corrective action:** Leave the reference repository and create a separate working directory.

## Step 2 — Build the Production Architecture Specification

Create `architecture_spec.json` with the complete production design:

```json
{
  "metadata": {
    "lab_id": "lab_04",
    "customer": "Northstar Mutual",
    "initiative": "Enterprise AI Claims Assistant",
    "architecture_stage": "production-ready bounded pilot",
    "prepared_by": "Forward Deployed Engineering Team",
    "decision_date": "2026-08-16"
  },
  "decision_contract": {
    "primary_user": "Licensed Claims Adjuster",
    "assisted_decision": "Choose whether to request evidence, continue review, or escalate the claim",
    "allowed_recommendations": [
      "request_evidence",
      "continue_review",
      "escalate"
    ],
    "protected_actions": [
      "approve_or_deny_claim",
      "authorize_payment_or_change_reserves",
      "send_customer_communication_or_update_claims_system"
    ],
    "human_approval": {
      "required": true,
      "role": "Licensed Claims Adjuster",
      "mechanism": "Explicit approve, change, or reject action in the claims UI",
      "enforced_by": "approval_service",
      "approval_recorded_before": "claims_system_adapter"
    }
  },
  "non_functional_requirements": {
    "citation_completeness_percent_min": 95,
    "protected_action_human_approval_percent": 100,
    "p95_response_seconds_max": 12,
    "monthly_availability_percent_min": 99.5,
    "cost_usd_per_completed_assist_max": 1.5,
    "audit_event_completeness_percent": 100,
    "recovery_time_objective_minutes_max": 60,
    "recovery_point_objective_minutes_max": 15
  },
  "trust_boundaries": {
    "approved_environment": "Northstar private cloud account",
    "data_classification": "PII and confidential claim data",
    "network_egress": "Deny by default; allow only approved model and observability endpoints",
    "data_residency": "United States",
    "restricted_data_excluded": [
      "Special Investigations fraud indicators"
    ],
    "retention": {
      "prompt_and_response_days": 30,
      "audit_record_years": 7,
      "raw_documents": "Follow the claims retention policy"
    }
  },
  "components": [
    {
      "id": "adjuster_ui",
      "zone": "user",
      "owner": "Claims Operations",
      "responsibility": "Show cited evidence and collect explicit adjuster decisions"
    },
    {
      "id": "api_gateway",
      "zone": "application",
      "owner": "Platform Engineering",
      "responsibility": "Authenticate requests, apply rate limits, and attach trace IDs"
    },
    {
      "id": "identity_policy",
      "zone": "security",
      "owner": "Identity and Access Management",
      "responsibility": "Enforce SSO, role-based access, and claim-level authorization"
    },
    {
      "id": "workflow_orchestrator",
      "zone": "application",
      "owner": "FDE Team",
      "responsibility": "Run the bounded assist workflow and stop on failed controls"
    },
    {
      "id": "retrieval_service",
      "zone": "data",
      "owner": "FDE Team",
      "responsibility": "Retrieve effective policy passages and claim evidence with citations"
    },
    {
      "id": "policy_document_store",
      "zone": "data",
      "owner": "Policy Administration",
      "responsibility": "Store approved policy versions and claim documents encrypted at rest"
    },
    {
      "id": "policy_metadata_index",
      "zone": "data",
      "owner": "Claims Data",
      "responsibility": "Filter policy evidence by product, jurisdiction, and effective date"
    },
    {
      "id": "model_gateway",
      "zone": "model",
      "owner": "AI Platform",
      "responsibility": "Pin approved models, redact logs, enforce quotas, and prevent direct tool access"
    },
    {
      "id": "managed_llm",
      "zone": "model",
      "owner": "AI Platform",
      "responsibility": "Generate a schema-constrained summary and allowed recommendation"
    },
    {
      "id": "input_output_guardrails",
      "zone": "security",
      "owner": "Information Security",
      "responsibility": "Detect injection, validate citations and schema, and block unsafe output"
    },
    {
      "id": "approval_service",
      "zone": "security",
      "owner": "Claims Platform",
      "responsibility": "Verify approver identity and bind approval to action, claim, and version"
    },
    {
      "id": "claims_system_adapter",
      "zone": "integration",
      "owner": "Claims Platform",
      "responsibility": "Execute allowlisted idempotent writes only with a valid approval token"
    },
    {
      "id": "audit_log",
      "zone": "audit",
      "owner": "Risk and Compliance",
      "responsibility": "Store immutable retrieval, model, approval, and action events"
    },
    {
      "id": "telemetry",
      "zone": "operations",
      "owner": "Site Reliability Engineering",
      "responsibility": "Measure quality, safety, latency, availability, cost, and adoption"
    },
    {
      "id": "secrets_manager",
      "zone": "security",
      "owner": "Platform Engineering",
      "responsibility": "Issue and rotate short-lived service credentials"
    }
  ],
  "flows": [
    {
      "id": "evidence_assisted_review",
      "path": [
        "adjuster_ui",
        "api_gateway",
        "identity_policy",
        "workflow_orchestrator",
        "retrieval_service",
        "policy_metadata_index",
        "policy_document_store",
        "model_gateway",
        "managed_llm",
        "input_output_guardrails",
        "adjuster_ui",
        "audit_log"
      ],
      "result": "Cited summary plus one allowed recommendation",
      "writes_system_of_record": false,
      "approval_required": false
    },
    {
      "id": "protected_action_execution",
      "path": [
        "adjuster_ui",
        "api_gateway",
        "identity_policy",
        "approval_service",
        "claims_system_adapter",
        "audit_log"
      ],
      "result": "Human-approved, idempotent claims-system action",
      "writes_system_of_record": true,
      "approval_required": true
    },
    {
      "id": "low_confidence_fallback",
      "path": [
        "input_output_guardrails",
        "workflow_orchestrator",
        "adjuster_ui",
        "audit_log"
      ],
      "result": "No recommendation; manual review with reason",
      "writes_system_of_record": false,
      "approval_required": false
    },
    {
      "id": "audit_failure_stop",
      "path": [
        "audit_log",
        "workflow_orchestrator",
        "adjuster_ui"
      ],
      "result": "Workflow stopped; manual claims process remains available",
      "writes_system_of_record": false,
      "approval_required": false
    }
  ],
  "controls": {
    "identity": {
      "sso_required": true,
      "least_privilege": true,
      "claim_level_authorization": true,
      "service_credentials": "Short-lived and rotated by secrets_manager"
    },
    "data": {
      "encryption_in_transit": true,
      "encryption_at_rest": true,
      "pii_redacted_from_operational_logs": true,
      "effective_date_filter_required": true
    },
    "model": {
      "approved_model_allowlist": true,
      "training_on_customer_data": false,
      "schema_validation": true,
      "citation_validation": true,
      "prompt_injection_detection": true
    },
    "execution": {
      "direct_model_tool_access": false,
      "allowlisted_actions": [
        "request_evidence",
        "continue_review",
        "escalate"
      ],
      "idempotency_keys_required": true,
      "approval_token_required_for_writes": true
    },
    "audit": {
      "immutable": true,
      "trace_id_end_to_end": true,
      "record_retrieval_model_approval_action": true,
      "audit_failure_behavior": "fail_closed"
    }
  },
  "failure_modes": [
    {
      "id": "policy_retrieval_timeout",
      "detection": "Retrieval exceeds 3 seconds or returns no effective policy version",
      "response": "Retry once, then stop recommendation and route to manual review",
      "owner": "FDE Team"
    },
    {
      "id": "low_grounding",
      "detection": "Citation validation fails or support score is below the release threshold",
      "response": "Return no recommendation and show the missing-evidence reason",
      "owner": "AI Platform"
    },
    {
      "id": "claims_write_timeout",
      "detection": "Claims adapter does not confirm the idempotency key",
      "response": "Do not retry blindly; reconcile action state before resubmission",
      "owner": "Claims Platform"
    },
    {
      "id": "audit_write_failure",
      "detection": "Required audit event cannot be durably stored",
      "response": "Fail closed, stop the AI workflow, and preserve the manual process",
      "owner": "Risk and Compliance"
    }
  ],
  "environments": [
    {
      "name": "dev",
      "isolated": true,
      "data": "Synthetic claims only",
      "promotion_evidence": "Unit, schema, and policy tests pass"
    },
    {
      "name": "test",
      "isolated": true,
      "data": "De-identified representative evaluation set",
      "promotion_evidence": "Quality, safety, injection, and failure tests pass"
    },
    {
      "name": "staging",
      "isolated": true,
      "data": "Approved masked production-like data",
      "promotion_evidence": "Load, recovery, observability, and security review pass"
    },
    {
      "name": "prod",
      "isolated": true,
      "data": "Authorized pilot claims",
      "promotion_evidence": "Business, technical, and security approvers sign the release record"
    }
  ],
  "ownership": {
    "business_owner": "Elena Ruiz, VP of Claims Operations",
    "user_representative": "Marcus Lee, Senior Claims Adjuster",
    "data_owner": "Priya Shah, Director of Claims Data",
    "technical_owner": "Jordan Kim, Forward Deployed Engineering Lead",
    "security_approver": "Dana Brooks, Information Security Director"
  }
}
```

Why this matters: the architecture starts with the user’s decision and authority boundary, then connects measurable requirements to components, ordered flows, controls, safe failure behavior, environments, and owners.

Review these critical boundaries:

| Boundary | Required design evidence |
| --- | --- |
| Human authority | Licensed adjuster approval is required before protected writes |
| Probabilistic AI | The model produces only a cited summary and one allowlisted recommendation |
| Deterministic execution | The approval service precedes the claims-system adapter |
| Data | PII stays in the approved US private-cloud boundary |
| Audit | Missing required evidence fails closed while manual work remains available |
| Operations | Quality, latency, availability, cost, recovery, and ownership are measurable |

### Verification checkpoint

- **Expected result:** The specification contains 15 uniquely owned components, four ordered flows, layered controls, four failure modes, four isolated environments, and five accountable owners.
- **Acceptable variation:** You may split a component if responsibilities and all flow references remain explicit.
- **Failure indicator:** The model can directly call the claims adapter, an unapproved write is possible, or a failure has no safe response and owner.
- **Corrective action:** Separate recommendation generation from deterministic approval and execution, then bind every control and failure to an enforcing component and owner.

## Step 3 — Write the Architecture Decision Record

Create `ADR-001-retrieval-first-human-approved-assistant.md`:

```markdown
# ADR-001 — Retrieval-First, Human-Approved Claims Assistant

- **Status:** Accepted for bounded pilot
- **Date:** 2026-08-16
- **Decision owners:** Jordan Kim, Forward Deployed Engineering Lead; Dana Brooks, Information Security Director
- **Business approver:** Elena Ruiz, VP of Claims Operations

## Context

Northstar Mutual's intake specialists assemble evidence from claim forms, policy documents, and adjuster notes. The current median intake-to-assignment time is 18 hours, rework is 22%, and citation completeness is 71%. Policy documents have inconsistent version and effective-date metadata, claim data contains PII, and fraud indicators are excluded from the pilot.

The assistant may summarize evidence and recommend `request_evidence`, `continue_review`, or `escalate`. It must not approve or deny a claim, authorize payment or reserve changes, send customer communications, or update the claims system without a licensed claims adjuster's explicit approval.

## Decision

Use a retrieval-first architecture with effective-date filtering, an approved managed language model behind a model gateway, schema and citation guardrails, and a separate deterministic approval and execution path.

The model receives only authorized claim context and retrieved policy passages. It produces a cited summary and one allowlisted recommendation. It has no direct access to the claims-system adapter. A protected write requires an approval token bound to the licensed adjuster, claim, proposed action, and artifact version. The claims adapter verifies that token and an idempotency key before writing.

All retrieval, model, guardrail, human-decision, and downstream-action events use an end-to-end trace ID and are written to the immutable audit log. If a required audit event cannot be stored, the AI workflow fails closed while the manual claims process remains available.

## Decision Drivers

- Preserve 100% human approval for protected claim actions.
- Raise citation completeness to at least 95% without using the wrong policy version.
- Keep PII inside Northstar's approved environment and exclude restricted fraud data.
- Meet a 12-second p95 response objective and a $1.50 maximum cost per completed assist.
- Make model, prompt, retrieval, approval, and action evidence independently auditable.
- Support rollback to the manual workflow and replacement of the model or retrieval implementation.

## Alternatives Considered

### Autonomous agent with direct claims-system tools

Rejected for the pilot. It weakens separation of duties, expands the prompt-injection blast radius, and could execute a protected action without an independently verified approval token.

### Fine-tune a model before fixing policy metadata

Rejected. Fine-tuning would not reliably solve effective-date retrieval and would make current policy evidence harder to inspect. Metadata remediation and retrieval evaluation are required first.

### Deterministic rules and templates only

Not selected as the complete solution. Rules remain appropriate for field completeness, authorization, routing constraints, and write enforcement, but they do not adequately summarize variable claim documents. This remains the fallback if AI quality gates are not met.

## Consequences

### Positive

- Citations and effective-date filters make recommendations inspectable.
- The model gateway, guardrails, approval service, and adapter create independent control layers.
- Model and retrieval implementations can change without changing claims-system authorization.
- Fail-closed audit behavior preserves evidence for regulated actions.

### Negative

- More components increase latency, operational ownership, and integration testing.
- Policy metadata must be remediated before production promotion.
- Human approval limits full automation and requires careful UI design.
- Immutable audit retention and representative evaluations add operating cost.

## Validation and Rollback

Promote only after representative quality, citation, injection, authorization, load, recovery, and audit tests pass. Monitor citation completeness, protected-action approval, p95 latency, availability, cost, rework, and adoption by claim type.

Disable the AI assist feature flag and continue the manual claims workflow if citation completeness drops below 95%, any unauthorized protected action occurs, required audit evidence is missing, or PII crosses the approved boundary. Reconcile any uncertain adapter write by idempotency key before retrying.

## Revisit Triggers

Revisit this decision if policy metadata becomes reliably normalized, a model or retrieval change materially alters quality or cost, regulations or residency requirements change, a new protected action is proposed, or pilot evidence supports expansion beyond the three approved recommendations.
```

Why this matters: the specification records what will exist. The ADR preserves why the team selected it, which alternatives were rejected, what consequences were accepted, and when the decision must be revisited.

### Verification checkpoint

- **Expected result:** The ADR records accepted status, context, decision, drivers, three alternatives, positive and negative consequences, validation and rollback, and revisit triggers.
- **Acceptable variation:** A different architecture is acceptable only if it satisfies the hard safety and data boundaries and is defended with equivalent evidence.
- **Failure indicator:** The ADR merely lists components or omits alternatives, negative consequences, rollback, or revisit conditions.
- **Corrective action:** Document the decision logic and operational trade-offs, not only the diagram.

## Step 4 — Build the Architecture Validator

Why this matters: an architecture decision is only actionable when its safety, flow, ownership, and rollback constraints can be checked. You will build the same validator contained in the completed reference repository.

Create `run_lab.py`:

```python
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
```

### Verification checkpoint

- **Expected result:** `run_lab.py` contains the complete validator above.
- **Acceptable variation:** Comments or formatting may differ if validation behavior and printed evidence remain equivalent.
- **Failure indicator:** The file is missing, truncated, or references different architecture or ADR filenames.
- **Corrective action:** Replace it with the complete source above and save it beside the architecture specification and ADR.

## Step 5 — Compile and Run the Completed Project

Why this matters: compilation catches Python syntax errors; the main run validates the architecture contract and ADR as one production-readiness decision.

Run:

```bash
python3 -m py_compile run_lab.py
python3 run_lab.py
```

Expected output:

```text
LAB 04 PASSED
- Architecture stage: production-ready bounded pilot
- Components: 15; flows: 4
- Human approval for protected actions: 100%
- Model direct claims-system access: blocked
- Audit failure behavior: fail_closed
- ADR status: Accepted for bounded pilot
```

### Verification checkpoint

- **Expected result:** Compilation is silent and the validator prints `LAB 04 PASSED` with the six architecture evidence lines.
- **Acceptable variation:** Your Python executable may be named `python` instead of `python3`.
- **Failure indicator:** A traceback, `LAB 04 FAILED`, missing evidence, or a nonzero exit status.
- **Corrective action:** Read the reported error, repair the named architecture or ADR requirement, and rerun both commands.

## Step 6 — Inspect the Design as an Operational Contract

Why this matters: a production architecture must show exactly where evidence, approval, execution, and audit responsibilities change hands.

Use the two project artifacts and validator output to answer:

1. Which component retrieves governed evidence?
2. Which component has authority to approve a protected action?
3. Why must the approval service appear before the claims-system adapter?
4. What happens when audit persistence fails?
5. Which evidence would justify promoting beyond the bounded pilot?

### Verification checkpoint

- **Expected result:** Your answers identify governed retrieval, human approval authority, ordered execution, fail-closed audit behavior, and promotion evidence.
- **Acceptable variation:** Component descriptions may use your own words while preserving the architecture boundaries.
- **Failure indicator:** The model appears to have direct execution authority, audit failure is fail-open, or promotion lacks measurable gates.
- **Corrective action:** Trace the relevant component, flow, control, failure mode, and ADR section, then correct the artifact and rerun `python3 run_lab.py`.

## Step 7 — Commit Your Completed Project

Why this matters: a clean commit records the exact architecture decision package reviewers can inspect and compare.

Run in your own project directory:

```bash
printf '__pycache__/\n*.py[cod]\n.DS_Store\n' > .gitignore
git init -b main
git add .gitignore architecture_spec.json ADR-001-retrieval-first-human-approved-assistant.md run_lab.py
git commit -m "Complete production AI architecture and ADR"
git status
```

### Verification checkpoint

- **Expected result:** Git creates a commit on `main` and reports a clean working tree.
- **Acceptable variation:** An existing repository may already be initialized; commit the same three project files and `.gitignore`.
- **Failure indicator:** A cache or unintended file is staged, or Git reports uncommitted changes.
- **Corrective action:** Remove transient files, stage only `.gitignore` and the three learner-built files, commit, and rerun `git status`.

## Map the Completed Workflow

1. The decision contract defines the user, allowed recommendations, protected actions, and human authority.
2. Measurable requirements and trust boundaries constrain design options.
3. Components and ordered flows separate evidence retrieval, recommendation, approval, execution, and audit.
4. The Python validator enforces the architecture and ADR constraints.
5. Layered controls and failure modes preserve safe manual fallback.
6. Environment promotion requires quality, safety, reliability, and approval evidence.
7. The ADR records why retrieval-first, human-approved architecture was selected and when it should change.

## Troubleshooting Cheatsheet

| Symptom | Likely cause | Corrective action |
| --- | --- | --- |
| JSON line/column error | Missing comma, quote, brace, or bracket | Repair the location reported by `json.tool` |
| Approval assertion fails | Human approval is disabled or path is incomplete | Restore required approval and the approval service |
| Execution-order failure | Adapter precedes approval service | Reorder the protected path |
| Direct-access failure | Model tool access was enabled | Restore `direct_model_tool_access: false` |
| Validator or ADR check fails | Required architecture evidence, decision section, or status is absent | Repair the item named by the validator |

## Cleanup

Keep `architecture_spec.json`, `ADR-001-retrieval-first-human-approved-assistant.md`, `run_lab.py`, `.gitignore`, and your Git history. No additional cleanup is required after the project passes and the working tree is clean.

## Completion Check

- [ ] I created the architecture specification, ADR, and Python validator from this guide.
- [ ] `run_lab.py` compiles and prints `LAB 04 PASSED`.
- [ ] The approval service precedes the claims-system adapter.
- [ ] Direct model tool access remains blocked.
- [ ] Audit failure remains fail-closed with manual fallback.
- [ ] The ADR records alternatives, consequences, rollback, and revisit triggers.
- [ ] My own Git working tree is clean.

## Reflection

Which architecture boundary most reduces the risk of a plausible model output becoming an unauthorized customer action, and what evidence proves that boundary is enforced?
