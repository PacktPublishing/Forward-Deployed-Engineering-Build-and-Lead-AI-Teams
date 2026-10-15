# Enterprise AI Claims Assistant — Integrated Deployment Review

- **Decision:** PLAN_READY_FOR_EXECUTION
- **Target go-live:** 2026-09-21
- **Objective:** Deliver a controlled claims-assistant pilot to 25 licensed adjusters with measurable exit evidence and an operational handoff.

## Workstreams

| Workstream | Owner | Milestones |
| --- | --- | --- |
| Solution and integration | FDE Lead | M-01, M-03, M-05 |
| Data and policy readiness | Claims Data Lead | M-01, M-02 |
| Security and production controls | Security Lead | M-02, M-04 |
| Evaluation and release evidence | AI Quality Lead | M-03, M-04 |
| Adoption and change | Claims Operations Lead | M-05, M-06 |
| Go-live and operational transition | Technical Deployment Lead | M-06, M-07 |

## Milestones

| ID | Milestone | Target | DRI | Dependencies |
| --- | --- | --- | --- | --- |
| M-01 | Scope and interfaces baselined | 2026-08-21 | FDE Lead | None |
| M-02 | Data and security controls approved | 2026-08-28 | Security Lead | M-01 |
| M-03 | End-to-end staging slice complete | 2026-09-04 | FDE Lead | M-01, M-02 |
| M-04 | Production-readiness gates passed | 2026-09-10 | AI Quality Lead | M-03 |
| M-05 | Pilot users and operations prepared | 2026-09-14 | Claims Operations Lead | M-03 |
| M-06 | Cutover rehearsal accepted | 2026-09-18 | Technical Deployment Lead | M-04, M-05 |
| M-07 | Go-live decision recorded | 2026-09-21 | Executive Sponsor | M-06 |

## Critical Path

M-01 → M-02 → M-03 → M-04 → M-06 → M-07

## Risk Register

| Risk | Score | Owner | Response | Status | Contingency |
| --- | ---: | --- | --- | --- | --- |
| R-01 | 20 | Claims Platform Lead | MITIGATE | MITIGATED | Launch read-only assistance and defer protected writes |
| R-02 | 16 | Security Lead | MITIGATE | MITIGATED | Hold promotion and repair tenant enforcement |
| R-03 | 15 | Claims Data Lead | MITIGATE | MONITORED | Remove affected jurisdiction from cohort and repair metadata |
| R-04 | 12 | Claims Operations Lead | MITIGATE | MONITORED | Reduce cohort to trained adjusters and add office hours |
| R-05 | 12 | Site Reliability Lead | MITIGATE | MITIGATED | Tune retrieval limit concurrency and timeouts |
| R-06 | 12 | Technical Deployment Lead | AVOID | MONITORED | Require a new scope decision and release review |
| R-07 | 10 | Operations Owner | MITIGATE | MITIGATED | Delay go-live or add approved coverage |
| R-08 | 8 | AI Platform Lead | TRANSFER | MONITORED | Disable AI assistance and continue manual claims handling |

## Cutover and Rollback

1. Confirm signed release record and on-call roster
2. Enable claims_ai_assist_pilot for the named cohort
3. Run synthetic smoke claim and verify audit evidence
4. Release the cohort and monitor first ten assisted claims

**Abort conditions:**

- Any unauthorized protected action
- Cross-tenant or approved-boundary data exposure
- Missing audit evidence
- Smoke claim fails a blocking control

**Rollback:** Disable the feature flag preserve evidence reconcile uncertain writes and continue the manual workflow.

## Handoff

- Receiving owner: Claims AI Operations
- Acceptance: Receiving owner completes an observed operating shift
- Acceptance: Rollback and reconciliation drills pass
- Acceptance: Artifact links and accountable owners are current
