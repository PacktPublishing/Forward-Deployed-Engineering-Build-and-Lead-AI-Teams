# Capstone Workshop 4 — Complete Readiness, Deployment, and Risk Planning

## Goal

Convert the approved architecture into a production-readiness review, phased deployment plan, and actionable risk register for the Enterprise AI Claims Assistant.

Continue in the same learner-owned capstone directory. The completed repository is a reference only.

## What You'll Build or Produce

- `readiness_deployment.json` — readiness controls, evidence, approvals, exceptions, rollback, rollout boundary, milestones, dependencies, and cutover checks.
- `risk_register.csv` — eight scored delivery risks with owners, responses, triggers, contingencies, and statuses.
- The Workshop 4 Git commit.

## Estimated Time

50–70 minutes.

## Cost Guardrails

This workshop runs locally and creates no infrastructure or external cost.

## Completion Evidence

- `python3 -m json.tool readiness_deployment.json` succeeds.
- Seven security and operational readiness categories contain evidence and owners.
- Business, technical, security, and operations approvals are complete.
- Wave 1 has an explicit cohort, volume, duration, feature flag, and manual fallback.
- Seven milestones form a valid dependency chain with exit evidence.
- Eight risks have mathematically correct scores and actionable triggers and contingencies.
- Git is clean after the Workshop 4 commit.

## Prerequisites

- Completed Workshops 1–3 in the same project directory
- Familiarity with production readiness, integrated deployment planning, cutover, rollback, and risk management

## Where This Workshop Fits

This workshop combines **Complete the Security and Production-Readiness Review** and **Build the Deployment Plan and Risk Register**. It turns technical design into controlled delivery.

## Step 1 — Create the Readiness and Deployment Artifact

Create `readiness_deployment.json`:

```json
{
  "metadata": {
    "lab_id": "lab_11",
    "customer": "Northstar Mutual",
    "initiative": "Enterprise AI Claims Assistant",
    "candidate": "claims-assistant-1.0.0",
    "review_date": "2026-08-17",
    "decision_stage": "phased production rollout"
  },
  "security_and_readiness": {
    "controls": [
      {
        "id": "C-01",
        "category": "identity_access",
        "owner": "Identity Engineering",
        "evidence": "Cross-tenant, wrong-role, and expired-session tests fail closed",
        "status": "PASS"
      },
      {
        "id": "C-02",
        "category": "data_protection",
        "owner": "Data Protection",
        "evidence": "Private boundary, minimization, retention, and PII log scan approved",
        "status": "PASS"
      },
      {
        "id": "C-03",
        "category": "model_guardrail",
        "owner": "AI Security",
        "evidence": "Direct and indirect prompt-injection suite blocked protected actions",
        "status": "PASS"
      },
      {
        "id": "C-04",
        "category": "human_approval",
        "owner": "Claims Platform",
        "evidence": "Bypass, replay, expired-token, and wrong-approver tests fail closed",
        "status": "PASS"
      },
      {
        "id": "C-05",
        "category": "observability_audit",
        "owner": "Security Operations",
        "evidence": "Audit completeness and immutability tests pass",
        "status": "PASS"
      },
      {
        "id": "C-06",
        "category": "reliability_recovery",
        "owner": "Site Reliability Engineering",
        "evidence": "Load, dependency-failure, idempotency, and rollback drills pass",
        "status": "PASS"
      },
      {
        "id": "C-07",
        "category": "operations",
        "owner": "Operations Owner",
        "evidence": "Runbook tabletop and primary/backup on-call review complete",
        "status": "PASS"
      }
    ],
    "approvals": [
      {
        "role": "Business Owner",
        "name": "Elena Ruiz",
        "approved": true
      },
      {
        "role": "Technical Owner",
        "name": "Jordan Kim",
        "approved": true
      },
      {
        "role": "Security Approver",
        "name": "Dana Brooks",
        "approved": true
      },
      {
        "role": "Operations Owner",
        "name": "Morgan Lee",
        "approved": true
      }
    ],
    "open_exceptions": [],
    "rollback_action": "Disable claims_ai_assist_rollout, preserve evidence, reconcile uncertain writes, notify accountable owners, and continue the manual claims workflow."
  },
  "deployment_plan": {
    "rollout_boundary": {
      "wave": "Wave 1 production rollout",
      "cohort": "75 trained licensed claims adjusters",
      "maximum_claims": 1500,
      "duration_days": 30,
      "feature_flag": "claims_ai_assist_rollout",
      "manual_workflow_available": true
    },
    "milestones": [
      {
        "id": "M-01",
        "name": "Outcome and scope sign-off",
        "owner": "Business Owner",
        "depends_on": [],
        "exit_evidence": "Signed outcome, scope, non-goals, and rollout boundary"
      },
      {
        "id": "M-02",
        "name": "Architecture and data readiness",
        "owner": "Technical Deployment Lead",
        "depends_on": [
          "M-01"
        ],
        "exit_evidence": "Approved design, effective-policy coverage, and version manifest"
      },
      {
        "id": "M-03",
        "name": "Evaluation and security approval",
        "owner": "Security Approver",
        "depends_on": [
          "M-02"
        ],
        "exit_evidence": "All release gates and readiness controls pass"
      },
      {
        "id": "M-04",
        "name": "Cutover readiness review",
        "owner": "Claims Operations Owner",
        "depends_on": [
          "M-03"
        ],
        "exit_evidence": "Training, on-call, rollback, communications, and support evidence complete"
      },
      {
        "id": "M-05",
        "name": "Wave 1 go-live",
        "owner": "Technical Deployment Lead",
        "depends_on": [
          "M-04"
        ],
        "exit_evidence": "Feature flag enabled only for the approved cohort"
      },
      {
        "id": "M-06",
        "name": "Hypercare and outcome review",
        "owner": "Product Partner",
        "depends_on": [
          "M-05"
        ],
        "exit_evidence": "Thirty-day scorecard, incidents, adoption, value, and next-wave decision"
      },
      {
        "id": "M-07",
        "name": "Operational handoff",
        "owner": "Operations Owner",
        "depends_on": [
          "M-06"
        ],
        "exit_evidence": "Runbooks, dashboards, support ownership, and backlog accepted"
      }
    ],
    "cutover_checks": [
      "Approved version manifest is pinned",
      "Only trained users are in the feature-flag cohort",
      "Primary and backup on-call owners are confirmed",
      "Rollback drill completed in under 10 minutes",
      "Manual claims workflow remains available"
    ]
  }
}
```

The readiness controls cover identity, data, model guardrails, human approval, observability, recovery, and operations. A status is credible only when it includes a named owner and concrete evidence.

### Verification checkpoint

- **Expected result:** Seven unique control categories have IDs, owners, evidence, and `PASS` status; four approval domains are present.
- **Acceptable variation:** Add organization-specific controls without removing the seven required categories.
- **Failure indicator:** A checklist says “ready” without evidence, an owner, rollback, or an exception record.
- **Corrective action:** Replace assertions with test, drill, review, or signed approval evidence and name the accountable owner.

## Step 2 — Inspect the Rollout Boundary and Critical Path

Trace the milestone dependencies from outcome sign-off through operational handoff:

```text
M-01 Outcome and scope
→ M-02 Architecture and data
→ M-03 Evaluation and security
→ M-04 Cutover readiness
→ M-05 Wave 1 go-live
→ M-06 Hypercare and outcome review
→ M-07 Operational handoff
```

Each milestone exits on evidence, not a calendar date alone. Wave 1 is intentionally constrained to 75 trained adjusters, 1,500 claims, 30 days, and one feature flag while manual handling stays available.

### Verification checkpoint

- **Expected result:** Every dependency references a real milestone, every milestone has one owner and exit evidence, and no dependency cycle exists.
- **Acceptable variation:** Parallelize work where dependencies genuinely allow it.
- **Failure indicator:** Go-live can occur before evaluation, security, training, on-call, or rollback evidence is complete.
- **Corrective action:** Restore the blocking dependency and explicit exit evidence.

## Step 3 — Build the Risk Register

Create `risk_register.csv`:

```csv
risk_id,category,description,probability,impact,score,owner,response,trigger,contingency,status
R-01,integration,Claims-system write API is not certified for the rollout window,4,5,20,Claims Platform Lead,MITIGATE,Certification slips beyond milestone M-04,Launch read-only assistance and defer protected writes,MITIGATED
R-02,security,Cross-tenant authorization defect appears in preproduction,4,5,20,Security Lead,MITIGATE,Any negative authorization test succeeds,Stop promotion and repair tenant enforcement,MITIGATED
R-03,data,Effective-date metadata is incomplete for a rollout jurisdiction,3,5,15,Claims Data Lead,MITIGATE,Policy coverage falls below 100 percent,Remove the jurisdiction from scope and repair metadata,MONITORED
R-04,adoption,Training completion falls below 90 percent before a rollout wave,3,4,12,Claims Operations Lead,MITIGATE,Completion is below target three days before cutover,Limit the wave to trained adjusters and add office hours,MONITORED
R-05,reliability,p95 latency exceeds 12 seconds under rollout load,3,4,12,Site Reliability Lead,MITIGATE,Two consecutive monitoring windows exceed the SLO,Disable the feature flag and continue manual handling,MITIGATED
R-06,scope,An executive requests enterprise-wide rollout before wave evidence,3,4,12,Technical Deployment Lead,AVOID,Requested cohort exceeds the approved wave boundary,Require a new scope decision and readiness review,MONITORED
R-07,operations,Primary or backup on-call coverage is missing during cutover,2,5,10,Operations Owner,MITIGATE,Any severity-one slot lacks both roles,Delay cutover or add approved coverage,MITIGATED
R-08,product,Customer-specific adapter changes leak into shared platform code,2,4,8,Product Owner,AVOID,Shared-core pull request contains Northstar-only logic,Move logic to the isolated extension and review the contract,MONITORED
```

Use `probability × impact` for prioritization, with both values on a 1–5 scale. The trigger tells the owner when to act. The contingency is the pre-agreed response if mitigation is insufficient.

### Verification checkpoint

- **Expected result:** Eight unique risks cover integration, security, data, adoption, reliability, scope, operations, and product concerns.
- **Acceptable variation:** Add a risk when it introduces a new category, owner, trigger, or contingency.
- **Failure indicator:** A risk says only “model may fail,” has no owner, or uses “monitor” without an activation trigger.
- **Corrective action:** State a concrete event, calculate its score, assign an owner, and define response and contingency.

## Step 4 — Test Cutover and Rollback Readiness

Conduct a tabletop using two risk triggers:

1. A cross-tenant negative authorization test succeeds before promotion.
2. p95 latency exceeds 12 seconds for two consecutive rollout windows.

For each, identify who detects it, who decides, how the feature flag changes, how evidence is preserved, which users are notified, and how manual claims handling continues.

### Verification checkpoint

- **Expected result:** Both scenarios stop or constrain AI assistance without disabling the manual workflow.
- **Acceptable variation:** The notification and incident workflow may follow your organization's process.
- **Failure indicator:** Rollback depends on redeploying code, loses evidence, or interrupts all claim handling.
- **Corrective action:** Use the feature flag, preserve audit evidence, reconcile uncertain writes, and retain the manual path.

## Step 5 — Validate and Commit Workshop 4

```bash
python3 -m json.tool readiness_deployment.json
python3 -c "import csv; rows=list(csv.DictReader(open('risk_register.csv'))); assert len(rows)>=8; assert all(int(r['score'])==int(r['probability'])*int(r['impact']) for r in rows); assert all(r['owner'] and r['trigger'] and r['contingency'] for r in rows); print('Risk register valid')"
git add readiness_deployment.json risk_register.csv
git commit -m "Complete capstone readiness and delivery plan"
git status --short --branch
```

### Verification checkpoint

- **Expected result:** JSON validates, `Risk register valid` prints, and Git is clean.
- **Acceptable variation:** Equivalent local CSV validation is acceptable.
- **Failure indicator:** A score is incorrect or a risk lacks owner, trigger, or contingency.
- **Corrective action:** Repair the reported risk fields and rerun before committing.

## Map the Completed Workflow

| Architecture evidence | Delivery control |
| --- | --- |
| Identity and authorization tests | Identity-access readiness control |
| Model and approval gates | Model-guardrail and human-approval controls |
| Audit and recovery design | Observability, recovery, and operations controls |
| Passed readiness review | Cutover milestone dependency |
| Known uncertainty | Owned risk, trigger, response, and contingency |
| Approved rollout boundary | Feature-flagged Wave 1 with manual fallback |

## Troubleshooting Cheatsheet

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Readiness says PASS without evidence | Checklist completion replaced proof | Add the exact test, drill, review, or signed record. |
| Milestone dependency is circular | Work packages depend on each other | Identify the real prerequisite and remove the cycle. |
| Risk score is wrong | Score was typed independently | Recalculate probability × impact. |
| Contingency is vague | Mitigation and recovery were confused | State the concrete action taken after the trigger fires. |
| Rollback disables claims operations | AI assistance and core workflow are coupled | Preserve the manual workflow behind a separate boundary. |

## Cleanup

No external resources were created. Keep all project files for Workshop 5.

## Completion Check

- [ ] Seven readiness categories have owners and evidence.
- [ ] Four approval domains are complete and exceptions are explicit.
- [ ] The rollout boundary constrains cohort, volume, duration, and feature access.
- [ ] Milestone dependencies and exit evidence form a valid path.
- [ ] Eight risks have correct scores, owners, triggers, and contingencies.
- [ ] Rollback preserves evidence and manual handling.
- [ ] My Workshop 4 commit is clean.

## Reflection

1. Which readiness control is easiest to mark complete without sufficient evidence?
2. Which milestone would you refuse to compress under executive pressure?
3. Which risk trigger would require immediate rollback rather than continued monitoring?
