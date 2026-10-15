# Enterprise AI Claims Assistant — Executive Deployment Decision

- **Decision:** APPROVE_PHASED_PRODUCTION_ROLLOUT
- **Customer:** Northstar Mutual
- **Candidate:** claims-assistant-1.0.0
- **Approved boundary:** 75 trained licensed claims adjusters; maximum 1500 claims over 30 days
- **Business outcome:** Reduce handling time and rework while improving quality and citation completeness without allowing unauthorized protected actions.

## Decision Rationale

The four-week pilot passed 11/11 adoption, outcome, quality, safety, and operations gates. The pinned release candidate passed 6/6 evaluation and human-approval gates. All 7 readiness controls and all 4 required approvals are complete.

## Latest-Week Scorecard

| Metric | Rule | Actual | Owner | Result |
| --- | --- | ---: | --- | --- |
| active_adoption_percent | >= 80 | 88.00 | Claims Operations Lead | PASS |
| assisted_claim_rate_percent | >= 70 | 87.50 | Claims Operations Lead | PASS |
| recommendation_acceptance_percent | >= 75 | 82.00 | Claims Quality Lead | PASS |
| handling_time_reduction_percent | >= 25 | 30.95 | Business Owner | PASS |
| rework_reduction_percent | >= 25 | 39.29 | Claims Quality Lead | PASS |
| quality_score_percent | >= 92 | 94.50 | Claims Quality Lead | PASS |
| citation_completeness_percent | >= 95 | 99.00 | Claims Quality Lead | PASS |
| p95_latency_seconds | <= 12 | 10.20 | Site Reliability Lead | PASS |
| benefit_cost_ratio | >= 3 | 15.92 | Finance Partner | PASS |
| unauthorized_protected_actions | <= 0 | 0.00 | Security Approver | PASS |
| audit_completeness_percent | >= 100 | 100.00 | Security Operations | PASS |

## Release and Human-Approval Evidence

| Metric | Rule | Actual | Owner | Result |
| --- | --- | ---: | --- | --- |
| recommendation_agreement_percent | >= 90 | 92.00 | Claims Quality Lead | PASS |
| citation_completeness_percent | >= 95 | 99.00 | Claims Quality Lead | PASS |
| prompt_injection_block_percent | >= 100 | 100.00 | Security Engineer | PASS |
| protected_action_human_approval_percent | >= 100 | 100.00 | Claims Operations Owner | PASS |
| unauthorized_protected_actions | <= 0 | 0.00 | Security Approver | PASS |
| audit_completeness_percent | >= 100 | 100.00 | Security Operations | PASS |

## Rollout and Rollback

- Feature flag: `claims_ai_assist_rollout`
- Manual workflow available: true
- Rollback: Disable claims_ai_assist_rollout, preserve evidence, reconcile uncertain writes, notify accountable owners, and continue the manual claims workflow.

## Highest Risks

| Risk | Score | Owner | Status | Trigger | Contingency |
| --- | ---: | --- | --- | --- | --- |
| R-01: Claims-system write API is not certified for the rollout window | 20 | Claims Platform Lead | MITIGATED | Certification slips beyond milestone M-04 | Launch read-only assistance and defer protected writes |
| R-02: Cross-tenant authorization defect appears in preproduction | 20 | Security Lead | MITIGATED | Any negative authorization test succeeds | Stop promotion and repair tenant enforcement |
| R-03: Effective-date metadata is incomplete for a rollout jurisdiction | 15 | Claims Data Lead | MONITORED | Policy coverage falls below 100 percent | Remove the jurisdiction from scope and repair metadata |
| R-04: Training completion falls below 90 percent before a rollout wave | 12 | Claims Operations Lead | MONITORED | Completion is below target three days before cutover | Limit the wave to trained adjusters and add office hours |
| R-05: p95 latency exceeds 12 seconds under rollout load | 12 | Site Reliability Lead | MITIGATED | Two consecutive monitoring windows exceed the SLO | Disable the feature flag and continue manual handling |

## Reusable Capability Decisions

- **PRODUCT — Prompt-injection evaluation pack:** Versioned test contract with deployment-specific fixtures Owner: AI Quality Product Owner.
- **PRODUCT — Effective-policy retrieval pattern:** Shared retrieval contract with configured jurisdiction and source connectors Owner: Knowledge Platform Product Owner.
- **PRODUCT — Protected-action audit schema:** Shared identity, evidence, approval, action, and result schema Owner: Security Product Owner.
- **PLATFORM — Enterprise identity adapter framework:** Shared adapter interface with customer-specific identity configuration Owner: Identity Platform Owner.
- **CONFIGURATION — Tenant claim-field mapping:** Declarative mapping that cannot fork shared source Owner: Implementation Configuration Owner.
- **CUSTOM_EXTENSION — Northstar legacy mainframe adapter:** Customer-funded isolated extension with review date 2027-03-31 Owner: Northstar Integration Owner.

## Next Governance Decision

At day 30, the Business Owner, Claims Operations Owner, Technical Owner, Security Approver, and Product Owner review the scorecard, incidents, open risks, support load, and reusable-capability evidence before expanding, repairing, pausing, or ending the rollout.
