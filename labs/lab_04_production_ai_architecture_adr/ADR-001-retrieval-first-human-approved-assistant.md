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

