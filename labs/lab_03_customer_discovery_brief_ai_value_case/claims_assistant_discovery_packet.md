# Enterprise AI Claims Assistant — Discovery Packet

Northstar Mutual processes property claims from email, scanned forms, policy systems, and a claims platform. Intake specialists manually summarize each submission, locate policy evidence, identify missing information, and assign the claim to an adjuster queue. Leadership has asked whether an AI assistant can improve this workflow.

## Current baseline

| Metric | Baseline | Source |
| --- | ---: | --- |
| Median intake-to-assignment time | 18 hours | Claims platform |
| Claims returned for missing or incorrect intake information | 22% | Quality review |
| Audit records with complete source citations | 71% | Audit log |
| Claim denials or payments receiving human approval | 100% | Claims platform |
| Weekly active adjusters using an AI assistant | 0% | Not yet deployed |

Northstar receives about 12,000 property claims per month. Claims Operations estimates that intake specialists spend 28 minutes per claim assembling evidence and writing the first summary, but this estimate has not yet been validated through a time study.

## People and ownership

- **Business owner:** Elena Ruiz, VP of Claims Operations
- **User representative:** Marcus Lee, Senior Claims Adjuster
- **Data owner:** Priya Shah, Director of Claims Data
- **Technical owner:** Jordan Kim, Forward Deployed Engineering Lead
- **Security approver:** Dana Brooks, Information Security Director
- **Human approval role:** Licensed Claims Adjuster

## Candidate workflow

The assistant could summarize submissions, retrieve policy evidence, identify missing information, recommend a routing queue, and draft an adjuster work note.

The assistant must not approve or deny a claim, authorize payment, change a policy record, send a customer-facing decision, or update the claims system without human approval.

## Available data

| Source | Owner | Readiness | Known issue |
| --- | --- | --- | --- |
| Claim intake forms | Claims Data | Ready with conditions | Structured fields are 97% complete |
| Policy documents | Policy Administration | Needs remediation | Version and effective-date labels are inconsistent |
| Adjuster notes | Claims Operations | Needs review | Free text contains abbreviations and sensitive information |
| Fraud indicators | Special Investigations | Restricted | Not approved for the first pilot |

Claim data contains personally identifiable information. It must remain inside Northstar's approved environment. Every source retrieval, recommendation, human decision, and downstream action must be auditable.

## Pilot boundary

Leadership will fund an eight-week pilot covering three adjuster teams and no more than 1,500 claims. The pilot may recommend **request evidence**, **continue review**, or **escalate**. It must not automate a protected claim action.

## Decision needed

The discovery team must recommend one of four outcomes:

1. Proceed to a bounded pilot.
2. Run a smaller prototype to close evidence gaps.
3. Pause until named prerequisites are resolved.
4. Do not proceed with AI.

The steering committee will approve or reject the recommendation. Progression beyond the pilot requires evidence for quality, safety, adoption, cycle time, rework, and auditability.
