# Enterprise AI Claims Assistant — Release Decision

- **Decision:** APPROVE_BOUNDED_PILOT
- **Evaluation run:** 2026-08-16
- **Release scope:** Retrieve effective policy evidence, produce a cited claim summary, and recommend one allowed next step without autonomous claim adjudication.

## Version Manifest

| Artifact | Version |
| --- | --- |
| Application | `claims-assistant-0.5.0` |
| Model | `approved-managed-llm-2026-07` |
| Prompt | `claims-review-v5` |
| Retrieval | `effective-policy-retrieval-v3` |
| Output Schema | `claims-assist-schema-v1` |
| Evaluation Dataset | `claims-pilot-eval-v1` |

## Release Gates

| Metric | Rule | Actual | Result |
| --- | --- | ---: | --- |
| case_count | >= 12 | 12 | PASS |
| segment_coverage_percent | >= 100 | 100 | PASS |
| recommendation_agreement_percent | >= 90 | 100 | PASS |
| citation_completeness_percent | >= 95 | 100 | PASS |
| schema_validity_percent | >= 99 | 100 | PASS |
| prompt_injection_block_percent | >= 100 | 100 | PASS |
| protected_action_human_approval_percent | >= 100 | 100 | PASS |
| unauthorized_protected_actions | <= 0 | 0 | PASS |
| p95_latency_seconds | <= 12 | 11.20 | PASS |
| mean_cost_usd | <= 1.5 | 0.97 | PASS |
| audit_completeness_percent | >= 100 | 100 | PASS |

## Required Approvals

- Approved — Business Owner: Elena Ruiz
- Approved — Technical Owner: Jordan Kim
- Approved — Security Approver: Dana Brooks

## Bounded Pilot

- Cohort: 25 licensed claims adjusters
- Maximum volume: 500 claims
- Duration: 14 days
- Feature flag: `claims_ai_assist_pilot`
- Manual workflow remains available: yes

## Rollback

- Any unauthorized protected action
- Citation completeness below 95 percent
- Missing required audit evidence
- PII crosses the approved boundary
- p95 latency exceeds 12 seconds for two consecutive monitoring windows

**Action:** Disable the feature flag, preserve evidence, reconcile uncertain writes by idempotency key, and continue the manual claims workflow.
