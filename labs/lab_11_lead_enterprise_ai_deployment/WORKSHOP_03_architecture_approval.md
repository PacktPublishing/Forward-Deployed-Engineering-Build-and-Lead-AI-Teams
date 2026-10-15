# Capstone Workshop 3 — Design Architecture, Evaluation, and Human Approval

## Goal

Design the production AI workflow for the Enterprise AI Claims Assistant and define the evaluation and human-approval evidence required before the candidate can perform any protected action.

Continue in the same learner-owned capstone directory. Use the completed course repository only for comparison or recovery.

## What You'll Build or Produce

- `architecture_approval.json` — components, trust boundaries, request flow, evaluation segments, release gates, latest results, protected actions, and approval evidence.
- An authority trace showing approval before execution and audit after the result.
- The Workshop 3 Git commit.

## Estimated Time

45–60 minutes.

## Cost Guardrails

This workshop models architecture and evidence locally. It calls no model endpoint and creates no infrastructure.

## Completion Evidence

- `python3 -m json.tool architecture_approval.json` succeeds.
- The design separates probabilistic AI from deterministic controls.
- Four trust boundaries and the complete seven-stage workflow are explicit.
- Nine representative and adversarial evaluation segments are required.
- Six release gates have matching results and owners.
- A licensed claims adjuster approves every protected action before execution.
- Git is clean after the Workshop 3 commit.

## Prerequisites

- Completed Workshops 1–2 in the same project directory
- Familiarity with production AI architecture, trust boundaries, evaluation gates, and human approval

## Where This Workshop Fits

This workshop combines **Design the Production AI Architecture** and **Create the Evaluation and Human-Approval Strategy**. It turns the business and ownership contracts into enforceable technical and evidence boundaries.

## Step 1 — Create the Architecture and Approval Artifact

Create `architecture_approval.json`:

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
  "architecture": {
    "principle": "Probabilistic AI prepares a cited recommendation; deterministic services enforce identity, policy, approval, execution, and audit.",
    "components": [
      {
        "name": "Adjuster Workspace",
        "type": "human_interface",
        "owner": "Claims Operations"
      },
      {
        "name": "Identity and Tenant Gateway",
        "type": "deterministic_control",
        "owner": "Identity Engineering"
      },
      {
        "name": "Effective Policy Retrieval",
        "type": "deterministic_control",
        "owner": "Claims Data"
      },
      {
        "name": "Claims Summary Model",
        "type": "probabilistic_ai",
        "owner": "AI Engineering"
      },
      {
        "name": "Recommendation Policy Gate",
        "type": "deterministic_control",
        "owner": "FDE Team"
      },
      {
        "name": "Human Approval Service",
        "type": "deterministic_control",
        "owner": "Claims Platform"
      },
      {
        "name": "Claims-System Adapter",
        "type": "protected_action",
        "owner": "Claims Platform"
      },
      {
        "name": "Immutable Audit Stream",
        "type": "deterministic_control",
        "owner": "Security Operations"
      }
    ],
    "trust_boundaries": [
      "Northstar user session to assistant service",
      "Assistant service to approved managed model endpoint",
      "Assistant service to claims and policy systems",
      "Protected action service to immutable audit store"
    ],
    "workflow": [
      "Authenticate the adjuster and enforce tenant and role scope.",
      "Retrieve only effective policy evidence for the authorized claim.",
      "Generate a schema-constrained cited summary and one allowed recommendation.",
      "Apply deterministic recommendation and protected-action policy.",
      "Require an explicit licensed-adjuster approval for every protected action.",
      "Execute with an approver-bound token and idempotency key.",
      "Write identity, evidence, versions, recommendation, approval, action, and result to the audit stream."
    ]
  },
  "evaluation_and_human_approval": {
    "evaluation_dataset": "claims-pilot-eval-v1",
    "required_segments": [
      "standard",
      "missing_evidence",
      "effective_date",
      "high_severity",
      "scanned_document",
      "prompt_injection",
      "jurisdiction",
      "duplicate_submission",
      "protected_action"
    ],
    "release_gates": [
      {
        "metric": "recommendation_agreement_percent",
        "operator": "min",
        "threshold": 90,
        "owner": "Claims Quality Lead"
      },
      {
        "metric": "citation_completeness_percent",
        "operator": "min",
        "threshold": 95,
        "owner": "Claims Quality Lead"
      },
      {
        "metric": "prompt_injection_block_percent",
        "operator": "min",
        "threshold": 100,
        "owner": "Security Engineer"
      },
      {
        "metric": "protected_action_human_approval_percent",
        "operator": "min",
        "threshold": 100,
        "owner": "Claims Operations Owner"
      },
      {
        "metric": "unauthorized_protected_actions",
        "operator": "max",
        "threshold": 0,
        "owner": "Security Approver"
      },
      {
        "metric": "audit_completeness_percent",
        "operator": "min",
        "threshold": 100,
        "owner": "Security Operations"
      }
    ],
    "latest_results": {
      "recommendation_agreement_percent": 92,
      "citation_completeness_percent": 99,
      "prompt_injection_block_percent": 100,
      "protected_action_human_approval_percent": 100,
      "unauthorized_protected_actions": 0,
      "audit_completeness_percent": 100
    },
    "human_approval": {
      "required": true,
      "role": "Licensed Claims Adjuster",
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
      "approval_evidence": [
        "approver identity",
        "claim and action scope",
        "fresh approval timestamp",
        "idempotency key",
        "final action result"
      ]
    }
  }
}
```

The design follows one rule: probabilistic AI may prepare a cited recommendation, but deterministic services enforce identity, authorization, recommendation policy, approval, execution, and audit.

### Verification checkpoint

- **Expected result:** Components include a human interface, one probabilistic AI component, deterministic controls, a protected-action adapter, and an immutable audit stream.
- **Acceptable variation:** Component names may match another platform if their responsibilities remain separated.
- **Failure indicator:** The model directly calls the claims system or decides whether approval is required.
- **Corrective action:** Route all protected execution through deterministic policy and approval services.

## Step 2 — Trace the Production Workflow

Walk through one recommendation from request to recorded result:

1. Authenticate the adjuster and enforce tenant and role scope.
2. Retrieve only authorized, effective policy evidence.
3. Generate a schema-constrained cited summary and one allowed recommendation.
4. Apply deterministic recommendation and protected-action policy.
5. Require explicit licensed-adjuster approval.
6. Execute with an approver-bound token and idempotency key.
7. Audit identity, evidence, versions, recommendation, approval, action, and result.

At every trust boundary, identify what is trusted, what remains untrusted, and which control must fail closed.

### Verification checkpoint

- **Expected result:** Approval appears before protected execution, and the final result is written to the audit stream.
- **Acceptable variation:** Additional validation or observability stages may be inserted without weakening the order.
- **Failure indicator:** Approval is inferred from model output, reused across actions, or recorded only after an untraceable write.
- **Corrective action:** Restore an explicit fresh approver-bound decision before execution and a complete post-result audit record.

## Step 3 — Evaluate the Candidate and Approval Boundary

The evaluation set covers normal cases, missing evidence, effective dates, high severity, scans, prompt injection, jurisdiction, duplicates, and protected actions. This prevents a strong average score from hiding a dangerous failure segment.

Review the six gates as hard release evidence:

| Evidence family | What it prevents |
| --- | --- |
| Recommendation agreement | Unreliable workflow guidance |
| Citation completeness | Unsupported or untraceable recommendations |
| Prompt-injection blocking | Untrusted content changing system policy |
| Human-approval completeness | Protected actions bypassing customer authority |
| Unauthorized action count | Consequential execution without authorization |
| Audit completeness | Missing evidence for investigation and accountability |

### Verification checkpoint

- **Expected result:** Every gate has a metric, operator, threshold, owner, and latest result.
- **Acceptable variation:** Add stricter gates or segments when the business risk requires them.
- **Failure indicator:** A quality average can offset an unauthorized action or missing approval.
- **Corrective action:** Keep safety and approval conditions as non-compensating hard gates.

## Step 4 — Validate Cross-Workshop Consistency and Commit

```bash
python3 -m json.tool architecture_approval.json
python3 -c "import json; files=['problem_value.json','team_decisions.json','architecture_approval.json']; docs=[json.load(open(f)) for f in files]; assert all(d['metadata']==docs[0]['metadata'] for d in docs); print('Metadata aligned')"
git add architecture_approval.json
git commit -m "Design capstone architecture and approval strategy"
git status --short --branch
```

### Verification checkpoint

- **Expected result:** JSON and metadata validation succeed and Git is clean.
- **Acceptable variation:** Equivalent local JSON validation is acceptable.
- **Failure indicator:** Architecture describes a different candidate or the human authority contradicts Workshop 2.
- **Corrective action:** Align metadata and restore the decision-rights boundary before committing.

## Map the Completed Workflow

| Earlier contract | Architecture or evidence response |
| --- | --- |
| Primary user and tenant scope | Identity and Tenant Gateway |
| Cited bounded recommendation | Retrieval, model, schema, and policy gate |
| Protected customer authority | Human Approval Service and licensed adjuster |
| Safety and quality outcome | Segmented evaluation and hard release gates |
| Accountable investigation | Immutable audit stream |

## Troubleshooting Cheatsheet

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Model can reach a protected tool | Control and model responsibilities are mixed | Insert deterministic policy and approval services. |
| High average hides a bad segment | Evaluation is not segmented | Add representative and adversarial segments with hard gates. |
| Approval evidence is incomplete | Approval is treated as a UI click only | Record identity, scope, freshness, idempotency key, and action result. |
| Metadata comparison fails | Workshop artifacts describe different candidates | Restore the Workshop 1 metadata object. |

## Cleanup

No external resources were created. Keep the project for Workshop 4.

## Completion Check

- [ ] Probabilistic and deterministic responsibilities are separated.
- [ ] Four trust boundaries are explicit.
- [ ] Approval precedes execution and audit follows the result.
- [ ] Nine evaluation segments cover normal and adversarial behavior.
- [ ] Six hard gates have results and owners.
- [ ] Protected actions require a licensed claims adjuster.
- [ ] My Workshop 3 commit is clean.

## Reflection

1. Which deterministic control most reduces the consequence of a plausible model error?
2. Which evaluation segment is easiest to overlook but most important for this case?
3. What evidence would you require to prove that approval cannot be replayed?
