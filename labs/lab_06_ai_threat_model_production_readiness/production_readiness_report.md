# Enterprise AI Claims Assistant — Threat Model and Production Readiness

- **Decision:** READY_FOR_BOUNDED_PILOT
- **Candidate:** claims-assistant-0.6.0
- **Target:** production bounded pilot
- **Review date:** 2026-08-16

## Decision Boundary

- Primary user: Licensed Claims Adjuster
- The assistant may retrieve policy evidence, summarize with citations, and recommend an allowed next step.
- Claim adjudication, payment, reserve changes, customer communication, and claims-system writes remain protected human actions.

## Threat Summary

- Threats reviewed: 10
- Inherent risk: 4 critical, 6 high, 0 medium
- Controls traced to readiness evidence: 12/12

| Threat | Category | Inherent | Residual | Owner | Controls |
| --- | --- | --- | --- | --- | --- |
| T-01 | prompt_injection | critical | medium | AI Security Lead | C-02, C-04, C-05, C-09 |
| T-02 | tool_abuse | critical | low | Claims Platform Owner | C-01, C-04, C-05, C-06, C-09 |
| T-03 | data_exfiltration | critical | medium | Data Protection Officer | C-01, C-07, C-09 |
| T-04 | retrieval_integrity | high | medium | Policy Operations Lead | C-03, C-09, C-10 |
| T-05 | identity_tenant_isolation | critical | low | Identity Engineering Lead | C-01, C-07, C-09 |
| T-06 | secrets | high | low | AI Platform Lead | C-08, C-09, C-10 |
| T-07 | transaction_integrity | high | medium | Claims Platform Owner | C-05, C-06, C-09, C-12 |
| T-08 | audit | high | low | Security Operations Lead | C-09, C-12 |
| T-09 | change_management | high | low | Release Engineering Lead | C-03, C-10, C-12 |
| T-10 | denial_of_service | high | medium | Site Reliability Engineering Lead | C-09, C-11, C-12 |

## Production-Readiness Checklist

| Category | Check | Status | Owner | Evidence ID |
| --- | --- | --- | --- | --- |
| identity_access | IAM-01 | PASS | Identity Engineering | E-IAM-01 |
| identity_access | IAM-02 | PASS | AI Platform | E-IAM-02 |
| data_protection | DATA-01 | PASS | Data Protection | E-DATA-01 |
| data_protection | DATA-02 | PASS | Policy Operations | E-DATA-02 |
| model_tool_guardrails | GRD-01 | PASS | AI Security | E-GRD-01 |
| model_tool_guardrails | GRD-02 | PASS | FDE Team | E-GRD-02 |
| model_tool_guardrails | GRD-03 | PASS | Claims Platform | E-GRD-03 |
| environments_delivery | ENV-01 | PASS | Release Engineering | E-ENV-01 |
| observability_audit | OBS-01 | PASS | Security Operations | E-OBS-01 |
| observability_audit | OBS-02 | PASS | Site Reliability Engineering | E-OBS-02 |
| reliability_recovery | REL-01 | PASS | Claims Platform | E-REL-01 |
| reliability_recovery | REL-02 | PASS | Site Reliability Engineering | E-REL-02 |
| reliability_recovery | REL-03 | PASS | Operations Lead | E-REL-03 |
| operations_governance | OPS-01 | PASS | Operations Lead | E-OPS-01 |
| operations_governance | OPS-02 | PASS | Technical Deployment Lead | E-OPS-02 |

## Version Manifest

| Artifact | Version |
| --- | --- |
| Application | claims-assistant-0.6.0 |
| Model | approved-managed-llm-2026-07 |
| Prompt | claims-review-v6 |
| Retrieval | effective-policy-retrieval-v3 |
| Output Schema | claims-assist-schema-v1 |
| Evaluation Dataset | claims-pilot-eval-v1 |
| Infrastructure | claims-assistant-infra-v4 |

## Required Approvals

- Approved — Business Owner: Elena Ruiz
- Approved — Technical Owner: Jordan Kim
- Approved — Security Approver: Dana Brooks
- Approved — Operations Owner: Morgan Lee

## Bounded Pilot and Recovery

- Cohort: 25 licensed claims adjusters
- Maximum volume: 500 claims
- Duration: 14 days
- Feature flag: claims_ai_assist_pilot
- Manual workflow remains available: yes

### Rollback triggers

- Any unauthorized protected action
- Any confirmed cross-tenant or approved-boundary data exposure
- Missing audit evidence for a protected recommendation, approval, or action
- Prompt injection changes system policy or reaches a protected tool
- p95 latency exceeds 12 seconds for two consecutive monitoring windows
- Model cost exceeds the approved daily burn-rate alert

**Rollback action:** Disable claims_ai_assist_pilot, preserve evidence, reconcile uncertain writes by idempotency key, notify accountable owners, and continue the manual claims workflow.
