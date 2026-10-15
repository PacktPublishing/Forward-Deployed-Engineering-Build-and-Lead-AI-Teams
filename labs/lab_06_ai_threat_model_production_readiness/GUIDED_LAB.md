# Lab 06 — Complete an AI Threat Model and Production-Readiness Checklist

## Goal

Create a traceable AI threat model and an executable production-readiness review for Northstar Mutual's Enterprise AI Claims Assistant. You will define the system's decision boundary, assets, trust boundaries, threats, control ownership, readiness evidence, human approvals, pilot limits, and rollback conditions. Then you will run a Python review that fails closed unless the threat model and production evidence are complete.

Build this lab in your own new project directory. The completed reference repository is for comparison if you become stuck; do not perform the exercise by editing the reference repository.

## What You'll Build or Produce

You will create:

- `threat_model.json` — the decision boundary, assets, trust boundaries, controls, and ten priority threats.
- `production_readiness_checklist.json` — fifteen blocking checks with owners and evidence across seven readiness categories.
- `readiness_review.py` — an executable review that validates traceability and generates the decision.
- `production_readiness_report.md` — the generated audit-friendly review record.
- `.gitignore` — Git hygiene for the Python workflow.

## Estimated Time

75–100 minutes.

## Cost Guardrails

This lab uses Python's standard library and local JSON files only. It makes no network calls, provisions no cloud resources, and requires no paid model or platform account.

## Completion Evidence

You are finished when:

- `python3 -m py_compile readiness_review.py` succeeds;
- `python3 readiness_review.py` prints `LAB 06 PASSED` and `READY_FOR_BOUNDED_PILOT`;
- all ten threat categories have an owner, mapped controls, verification evidence, and low or medium residual risk;
- all twelve controls trace to readiness evidence;
- all fifteen blocking readiness checks pass;
- business, technical, security, and operations approvals are present;
- `production_readiness_report.md` records the decision, pilot boundary, and rollback conditions; and
- your own Git repository is clean on branch `main`.

## Prerequisites

- Python 3.10 or later
- Git
- A text editor
- Familiarity with JSON, basic Python, trust boundaries, least privilege, and human approval controls
- The case boundary: the assistant may retrieve effective policy evidence, create a cited summary, and recommend `request_evidence`, `continue_review`, or `escalate`. It must not autonomously adjudicate claims, authorize money, communicate with customers, or update the claims system.

## Where This Lab Fits

This lab challenges the release candidate from Lab 05 before customer deployment. You will trace concrete threats to enforcing controls and production evidence, then verify identity, data protection, guardrails, observability, reliability, recovery, and accountable approval. Passing means the bounded pilot is ready for a controlled delivery plan—not an unrestricted launch.

## Step 1 — Create Your Project

Create and enter a new directory:

```bash
mkdir lab_06_ai_threat_model_production_readiness
cd lab_06_ai_threat_model_production_readiness
```

Create `.gitignore`:

```gitignore
__pycache__/
*.py[cod]
.DS_Store
```

Why this matters: you are building the completed project independently. The reference repository represents the same finished state and is only a recovery aid.

### Verification checkpoint

- **Expected result:** You are in an empty learner-owned directory containing only `.gitignore`.
- **Acceptable variation:** You may choose another directory name.
- **Failure indicator:** You are inside the completed reference repository or an earlier lab.
- **Corrective action:** Stop, create a separate directory, and continue there.

## Step 2 — Define the Threat Model

Create `threat_model.json`:

```json
{
  "metadata": {
    "lab_id": "lab_06",
    "customer": "Northstar Mutual",
    "initiative": "Enterprise AI Claims Assistant",
    "review_scope": "Bounded production pilot",
    "prepared_by": "Forward Deployed Engineering Team",
    "review_date": "2026-08-16"
  },
  "decision_boundary": {
    "primary_user": "Licensed Claims Adjuster",
    "allowed_assistance": [
      "Retrieve effective policy evidence",
      "Produce a cited claim summary",
      "Recommend request_evidence, continue_review, or escalate"
    ],
    "protected_actions": [
      "Approve or deny a claim",
      "Authorize payment or change reserves",
      "Send customer communication or update the claims system"
    ],
    "autonomous_protected_actions_allowed": false
  },
  "assets": [
    {
      "id": "A-01",
      "name": "Claim files and customer PII",
      "classification": "Restricted",
      "owner": "Claims Data Owner",
      "required_properties": [
        "confidentiality",
        "integrity",
        "authorized use"
      ]
    },
    {
      "id": "A-02",
      "name": "Effective policy corpus and metadata",
      "classification": "Confidential",
      "owner": "Policy Operations",
      "required_properties": [
        "integrity",
        "effective-date accuracy",
        "jurisdiction accuracy"
      ]
    },
    {
      "id": "A-03",
      "name": "Assistant recommendation and citations",
      "classification": "Confidential",
      "owner": "Claims Quality Lead",
      "required_properties": [
        "integrity",
        "traceability",
        "schema validity"
      ]
    },
    {
      "id": "A-04",
      "name": "Claims-system protected actions",
      "classification": "Restricted",
      "owner": "Claims Platform Owner",
      "required_properties": [
        "authorization",
        "idempotency",
        "human approval"
      ]
    },
    {
      "id": "A-05",
      "name": "Audit and release evidence",
      "classification": "Confidential",
      "owner": "Security Operations",
      "required_properties": [
        "completeness",
        "immutability",
        "retention"
      ]
    },
    {
      "id": "A-06",
      "name": "Service credentials and model endpoints",
      "classification": "Secret",
      "owner": "AI Platform",
      "required_properties": [
        "confidentiality",
        "rotation",
        "least privilege"
      ]
    }
  ],
  "trust_boundaries": [
    {
      "id": "B-01",
      "from": "Adjuster browser",
      "to": "Claims Assistant API",
      "data": "Claim context and user intent",
      "enforcement": "SSO, tenant-scoped authorization, request validation"
    },
    {
      "id": "B-02",
      "from": "Claims Assistant API",
      "to": "Policy retrieval service",
      "data": "Search query and retrieved policy evidence",
      "enforcement": "Service identity, signed index version, effective-date and jurisdiction filters"
    },
    {
      "id": "B-03",
      "from": "Claims Assistant API",
      "to": "Managed LLM endpoint",
      "data": "Minimum necessary claim context and policy evidence",
      "enforcement": "Private endpoint, encryption, PII minimization, no provider training"
    },
    {
      "id": "B-04",
      "from": "Claims Assistant API",
      "to": "Claims system",
      "data": "Human-approved protected command",
      "enforcement": "Approver-bound token, allowlisted operation, idempotency key"
    },
    {
      "id": "B-05",
      "from": "Application services",
      "to": "Audit platform",
      "data": "Identity, versions, evidence, decision, approval, and action result",
      "enforcement": "Append-only logging and fail-closed audit delivery"
    }
  ],
  "controls": [
    {
      "id": "C-01",
      "name": "Tenant-scoped identity and least privilege",
      "type": "prevent",
      "owner": "Identity Engineering",
      "status": "implemented",
      "evidence_ids": [
        "E-IAM-01"
      ]
    },
    {
      "id": "C-02",
      "name": "Untrusted-content separation and injection detection",
      "type": "prevent",
      "owner": "AI Platform",
      "status": "implemented",
      "evidence_ids": [
        "E-GRD-01"
      ]
    },
    {
      "id": "C-03",
      "name": "Versioned retrieval with effective-date and jurisdiction filters",
      "type": "prevent",
      "owner": "Policy Operations",
      "status": "implemented",
      "evidence_ids": [
        "E-DATA-02"
      ]
    },
    {
      "id": "C-04",
      "name": "Schema-constrained recommendation allowlist",
      "type": "prevent",
      "owner": "FDE Team",
      "status": "implemented",
      "evidence_ids": [
        "E-GRD-02"
      ]
    },
    {
      "id": "C-05",
      "name": "Human approval with approver-bound action token",
      "type": "prevent",
      "owner": "Claims Platform",
      "status": "implemented",
      "evidence_ids": [
        "E-GRD-03"
      ]
    },
    {
      "id": "C-06",
      "name": "Idempotent writes and uncertain-write reconciliation",
      "type": "correct",
      "owner": "Claims Platform",
      "status": "implemented",
      "evidence_ids": [
        "E-REL-01"
      ]
    },
    {
      "id": "C-07",
      "name": "PII minimization, encryption, and approved data boundary",
      "type": "prevent",
      "owner": "Data Protection",
      "status": "implemented",
      "evidence_ids": [
        "E-DATA-01"
      ]
    },
    {
      "id": "C-08",
      "name": "Managed secrets, rotation, and workload identity",
      "type": "prevent",
      "owner": "AI Platform",
      "status": "implemented",
      "evidence_ids": [
        "E-IAM-02"
      ]
    },
    {
      "id": "C-09",
      "name": "Complete immutable audit trail with fail-closed delivery",
      "type": "detect",
      "owner": "Security Operations",
      "status": "implemented",
      "evidence_ids": [
        "E-OBS-01"
      ]
    },
    {
      "id": "C-10",
      "name": "Signed version manifest and controlled environment promotion",
      "type": "prevent",
      "owner": "Release Engineering",
      "status": "implemented",
      "evidence_ids": [
        "E-ENV-01"
      ]
    },
    {
      "id": "C-11",
      "name": "Rate limits, timeouts, circuit breakers, and cost budgets",
      "type": "prevent",
      "owner": "Site Reliability Engineering",
      "status": "implemented",
      "evidence_ids": [
        "E-REL-02"
      ]
    },
    {
      "id": "C-12",
      "name": "Feature flag, manual path, rollback, and incident runbook",
      "type": "correct",
      "owner": "Operations Lead",
      "status": "implemented",
      "evidence_ids": [
        "E-REL-03",
        "E-OPS-01"
      ]
    }
  ],
  "threats": [
    {
      "id": "T-01",
      "category": "prompt_injection",
      "scenario": "A claim attachment instructs the model to ignore policy rules, reveal hidden context, or invoke a protected action.",
      "asset_ids": [
        "A-01",
        "A-03",
        "A-04"
      ],
      "trust_boundary_ids": [
        "B-01",
        "B-03",
        "B-04"
      ],
      "likelihood": "high",
      "impact": "critical",
      "inherent_risk": "critical",
      "control_ids": [
        "C-02",
        "C-04",
        "C-05",
        "C-09"
      ],
      "verification_evidence_ids": [
        "E-GRD-01",
        "E-GRD-02",
        "E-GRD-03",
        "E-OBS-01"
      ],
      "owner": "AI Security Lead",
      "residual_risk": "medium",
      "disposition": "MITIGATE"
    },
    {
      "id": "T-02",
      "category": "tool_abuse",
      "scenario": "A user or compromised service attempts a non-allowlisted claim denial, payment, reserve change, or customer communication.",
      "asset_ids": [
        "A-04",
        "A-05"
      ],
      "trust_boundary_ids": [
        "B-01",
        "B-04",
        "B-05"
      ],
      "likelihood": "medium",
      "impact": "critical",
      "inherent_risk": "critical",
      "control_ids": [
        "C-01",
        "C-04",
        "C-05",
        "C-06",
        "C-09"
      ],
      "verification_evidence_ids": [
        "E-IAM-01",
        "E-GRD-02",
        "E-GRD-03",
        "E-REL-01",
        "E-OBS-01"
      ],
      "owner": "Claims Platform Owner",
      "residual_risk": "low",
      "disposition": "MITIGATE"
    },
    {
      "id": "T-03",
      "category": "data_exfiltration",
      "scenario": "Claim PII crosses the approved boundary through prompts, logs, model output, or cross-tenant retrieval.",
      "asset_ids": [
        "A-01",
        "A-05"
      ],
      "trust_boundary_ids": [
        "B-01",
        "B-03",
        "B-05"
      ],
      "likelihood": "medium",
      "impact": "critical",
      "inherent_risk": "critical",
      "control_ids": [
        "C-01",
        "C-07",
        "C-09"
      ],
      "verification_evidence_ids": [
        "E-IAM-01",
        "E-DATA-01",
        "E-OBS-01"
      ],
      "owner": "Data Protection Officer",
      "residual_risk": "medium",
      "disposition": "MITIGATE"
    },
    {
      "id": "T-04",
      "category": "retrieval_integrity",
      "scenario": "The assistant cites a stale, wrong-jurisdiction, poisoned, or unauthorized policy document.",
      "asset_ids": [
        "A-02",
        "A-03"
      ],
      "trust_boundary_ids": [
        "B-02"
      ],
      "likelihood": "high",
      "impact": "high",
      "inherent_risk": "high",
      "control_ids": [
        "C-03",
        "C-09",
        "C-10"
      ],
      "verification_evidence_ids": [
        "E-DATA-02",
        "E-OBS-01",
        "E-ENV-01"
      ],
      "owner": "Policy Operations Lead",
      "residual_risk": "medium",
      "disposition": "MITIGATE"
    },
    {
      "id": "T-05",
      "category": "identity_tenant_isolation",
      "scenario": "An adjuster or service accesses a claim, policy, or action outside its tenant, role, or assigned authority.",
      "asset_ids": [
        "A-01",
        "A-02",
        "A-04"
      ],
      "trust_boundary_ids": [
        "B-01",
        "B-02",
        "B-04"
      ],
      "likelihood": "medium",
      "impact": "critical",
      "inherent_risk": "critical",
      "control_ids": [
        "C-01",
        "C-07",
        "C-09"
      ],
      "verification_evidence_ids": [
        "E-IAM-01",
        "E-DATA-01",
        "E-OBS-01"
      ],
      "owner": "Identity Engineering Lead",
      "residual_risk": "low",
      "disposition": "MITIGATE"
    },
    {
      "id": "T-06",
      "category": "secrets",
      "scenario": "A credential is committed, logged, exposed to the model, or reused beyond its intended workload.",
      "asset_ids": [
        "A-06"
      ],
      "trust_boundary_ids": [
        "B-02",
        "B-03",
        "B-04",
        "B-05"
      ],
      "likelihood": "medium",
      "impact": "high",
      "inherent_risk": "high",
      "control_ids": [
        "C-08",
        "C-09",
        "C-10"
      ],
      "verification_evidence_ids": [
        "E-IAM-02",
        "E-OBS-01",
        "E-ENV-01"
      ],
      "owner": "AI Platform Lead",
      "residual_risk": "low",
      "disposition": "MITIGATE"
    },
    {
      "id": "T-07",
      "category": "transaction_integrity",
      "scenario": "A timeout, retry, or partial failure creates a duplicate action or leaves an uncertain claims-system write.",
      "asset_ids": [
        "A-04",
        "A-05"
      ],
      "trust_boundary_ids": [
        "B-04",
        "B-05"
      ],
      "likelihood": "high",
      "impact": "high",
      "inherent_risk": "high",
      "control_ids": [
        "C-05",
        "C-06",
        "C-09",
        "C-12"
      ],
      "verification_evidence_ids": [
        "E-GRD-03",
        "E-REL-01",
        "E-OBS-01",
        "E-REL-03"
      ],
      "owner": "Claims Platform Owner",
      "residual_risk": "medium",
      "disposition": "MITIGATE"
    },
    {
      "id": "T-08",
      "category": "audit",
      "scenario": "A protected recommendation, approval, version, or action result is missing from the audit record or can be altered.",
      "asset_ids": [
        "A-03",
        "A-04",
        "A-05"
      ],
      "trust_boundary_ids": [
        "B-05"
      ],
      "likelihood": "medium",
      "impact": "high",
      "inherent_risk": "high",
      "control_ids": [
        "C-09",
        "C-12"
      ],
      "verification_evidence_ids": [
        "E-OBS-01",
        "E-OPS-01"
      ],
      "owner": "Security Operations Lead",
      "residual_risk": "low",
      "disposition": "MITIGATE"
    },
    {
      "id": "T-09",
      "category": "change_management",
      "scenario": "An unapproved model, prompt, retrieval index, schema, or tool version reaches production without matching evaluation evidence.",
      "asset_ids": [
        "A-02",
        "A-03",
        "A-04",
        "A-05"
      ],
      "trust_boundary_ids": [
        "B-02",
        "B-03",
        "B-04"
      ],
      "likelihood": "medium",
      "impact": "high",
      "inherent_risk": "high",
      "control_ids": [
        "C-03",
        "C-10",
        "C-12"
      ],
      "verification_evidence_ids": [
        "E-DATA-02",
        "E-ENV-01",
        "E-REL-03"
      ],
      "owner": "Release Engineering Lead",
      "residual_risk": "low",
      "disposition": "MITIGATE"
    },
    {
      "id": "T-10",
      "category": "denial_of_service",
      "scenario": "Large documents, repeated retries, or abusive traffic exhaust latency, capacity, or model-cost budgets and block adjuster work.",
      "asset_ids": [
        "A-03",
        "A-06"
      ],
      "trust_boundary_ids": [
        "B-01",
        "B-02",
        "B-03"
      ],
      "likelihood": "high",
      "impact": "medium",
      "inherent_risk": "high",
      "control_ids": [
        "C-09",
        "C-11",
        "C-12"
      ],
      "verification_evidence_ids": [
        "E-OBS-01",
        "E-REL-02",
        "E-REL-03"
      ],
      "owner": "Site Reliability Engineering Lead",
      "residual_risk": "medium",
      "disposition": "MITIGATE"
    }
  ],
  "risk_policy": {
    "production_blockers": [
      "critical residual risk",
      "high residual risk without approved exception",
      "unowned threat",
      "unverified blocking control"
    ],
    "allowed_residual_risk_for_pilot": [
      "low",
      "medium"
    ],
    "exception_requires": [
      "named risk owner",
      "business approval",
      "security approval",
      "expiration date",
      "compensating control"
    ]
  }
}
```

The model begins with the exact business decision boundary, not a generic list of AI risks. Each threat crosses a named trust boundary, affects known assets, maps to enforcing controls and evidence, has a named risk owner, and ends with an explicit residual-risk disposition.

The ten categories deliberately cover the production concerns most likely to matter for this case: indirect prompt injection, tool abuse, data exfiltration, retrieval integrity, tenant isolation, secret exposure, duplicate or uncertain writes, audit failure, uncontrolled change, and availability or cost exhaustion.

### Verification checkpoint

- **Expected result:** The file contains 6 assets, 5 trust boundaries, 12 controls, and 10 owned threats.
- **Acceptable variation:** You may add scenario-specific threats, but preserve every required category and all protected-action boundaries.
- **Failure indicator:** Threats are generic one-line concerns without assets, trust boundaries, owners, controls, evidence, or residual risk.
- **Corrective action:** Turn each concern into a concrete abuse or failure scenario and map it to enforceable controls and verification evidence.

## Step 3 — Build the Production-Readiness Checklist

Create `production_readiness_checklist.json`:

```json
{
  "metadata": {
    "lab_id": "lab_06",
    "customer": "Northstar Mutual",
    "initiative": "Enterprise AI Claims Assistant",
    "candidate": "claims-assistant-0.6.0",
    "review_date": "2026-08-16",
    "target_environment": "production bounded pilot"
  },
  "version_manifest": {
    "application": "claims-assistant-0.6.0",
    "model": "approved-managed-llm-2026-07",
    "prompt": "claims-review-v6",
    "retrieval": "effective-policy-retrieval-v3",
    "output_schema": "claims-assist-schema-v1",
    "evaluation_dataset": "claims-pilot-eval-v1",
    "infrastructure": "claims-assistant-infra-v4"
  },
  "checklist": {
    "identity_access": [
      {
        "id": "IAM-01",
        "requirement": "SSO identity, tenant scope, role checks, and least-privilege service permissions are enforced.",
        "owner": "Identity Engineering",
        "evidence_id": "E-IAM-01",
        "evidence": "Negative authorization suite passed for cross-tenant, wrong-role, and expired-session access.",
        "control_ids": [
          "C-01"
        ],
        "status": "PASS",
        "blocking": true
      },
      {
        "id": "IAM-02",
        "requirement": "Workload identity replaces embedded credentials and managed secrets rotate on schedule.",
        "owner": "AI Platform",
        "evidence_id": "E-IAM-02",
        "evidence": "Secret scan is clean; workload identity and rotation test passed in staging.",
        "control_ids": [
          "C-08"
        ],
        "status": "PASS",
        "blocking": true
      }
    ],
    "data_protection": [
      {
        "id": "DATA-01",
        "requirement": "Only minimum necessary claim data crosses encrypted approved boundaries and logs redact PII.",
        "owner": "Data Protection",
        "evidence_id": "E-DATA-01",
        "evidence": "Data-flow review, private-endpoint check, retention policy, and PII log scan approved.",
        "control_ids": [
          "C-07"
        ],
        "status": "PASS",
        "blocking": true
      },
      {
        "id": "DATA-02",
        "requirement": "Retrieval enforces tenant, authorization, effective-date, jurisdiction, and signed index version.",
        "owner": "Policy Operations",
        "evidence_id": "E-DATA-02",
        "evidence": "Representative and adversarial retrieval tests passed against index effective-policy-retrieval-v3.",
        "control_ids": [
          "C-03"
        ],
        "status": "PASS",
        "blocking": true
      }
    ],
    "model_tool_guardrails": [
      {
        "id": "GRD-01",
        "requirement": "Retrieved and uploaded content is treated as untrusted; injection attempts cannot change system policy or expose hidden context.",
        "owner": "AI Security",
        "evidence_id": "E-GRD-01",
        "evidence": "Prompt-injection and indirect-injection suite blocked all protected-action and exfiltration attempts.",
        "control_ids": [
          "C-02"
        ],
        "status": "PASS",
        "blocking": true
      },
      {
        "id": "GRD-02",
        "requirement": "Assistant output is schema-valid and limited to request_evidence, continue_review, or escalate.",
        "owner": "FDE Team",
        "evidence_id": "E-GRD-02",
        "evidence": "Schema and recommendation allowlist gates passed for the pinned candidate.",
        "control_ids": [
          "C-04"
        ],
        "status": "PASS",
        "blocking": true
      },
      {
        "id": "GRD-03",
        "requirement": "Every protected action requires a fresh approver-bound token and an explicit licensed-adjuster confirmation.",
        "owner": "Claims Platform",
        "evidence_id": "E-GRD-03",
        "evidence": "Bypass, replay, expired-token, wrong-approver, and missing-approval tests all failed closed.",
        "control_ids": [
          "C-05"
        ],
        "status": "PASS",
        "blocking": true
      }
    ],
    "environments_delivery": [
      {
        "id": "ENV-01",
        "requirement": "Dev, test, staging, and production promotion uses signed artifacts, separation of duties, and the exact version manifest.",
        "owner": "Release Engineering",
        "evidence_id": "E-ENV-01",
        "evidence": "Promotion record links approvals, evaluation evidence, infrastructure plan, and signed versions.",
        "control_ids": [
          "C-10"
        ],
        "status": "PASS",
        "blocking": true
      }
    ],
    "observability_audit": [
      {
        "id": "OBS-01",
        "requirement": "Logs and traces capture identity, tenant, versions, retrieved evidence, recommendation, approval, action, latency, cost, and errors without raw PII.",
        "owner": "Security Operations",
        "evidence_id": "E-OBS-01",
        "evidence": "Audit completeness and immutability tests passed; failed audit delivery blocks protected actions.",
        "control_ids": [
          "C-09"
        ],
        "status": "PASS",
        "blocking": true
      },
      {
        "id": "OBS-02",
        "requirement": "Dashboards and alerts cover safety, authorization, retrieval quality, latency, error, capacity, and cost SLOs.",
        "owner": "Site Reliability Engineering",
        "evidence_id": "E-OBS-02",
        "evidence": "Staging alert drill paged the on-call owner with version and correlation identifiers.",
        "control_ids": [
          "C-09",
          "C-11"
        ],
        "status": "PASS",
        "blocking": true
      }
    ],
    "reliability_recovery": [
      {
        "id": "REL-01",
        "requirement": "Retries are bounded and protected writes use idempotency keys with an uncertain-write reconciliation path.",
        "owner": "Claims Platform",
        "evidence_id": "E-REL-01",
        "evidence": "Timeout, duplicate-submit, and partial-failure tests produced one action or a reconciliation task.",
        "control_ids": [
          "C-06"
        ],
        "status": "PASS",
        "blocking": true
      },
      {
        "id": "REL-02",
        "requirement": "Timeouts, circuit breakers, concurrency limits, and cost budgets preserve the manual workflow.",
        "owner": "Site Reliability Engineering",
        "evidence_id": "E-REL-02",
        "evidence": "Load and dependency-failure tests stayed within the approved blast radius and budget.",
        "control_ids": [
          "C-11"
        ],
        "status": "PASS",
        "blocking": true
      },
      {
        "id": "REL-03",
        "requirement": "Feature-flag rollback disables AI assistance without disabling manual claims handling.",
        "owner": "Operations Lead",
        "evidence_id": "E-REL-03",
        "evidence": "Rollback drill disabled the pilot in under 10 minutes and preserved audit evidence.",
        "control_ids": [
          "C-12"
        ],
        "status": "PASS",
        "blocking": true
      }
    ],
    "operations_governance": [
      {
        "id": "OPS-01",
        "requirement": "Incident runbook names severity, triage, containment, evidence preservation, notification, and recovery owners.",
        "owner": "Operations Lead",
        "evidence_id": "E-OPS-01",
        "evidence": "Tabletop exercise completed for prompt injection, PII exposure, and uncertain protected write.",
        "control_ids": [
          "C-12"
        ],
        "status": "PASS",
        "blocking": true
      },
      {
        "id": "OPS-02",
        "requirement": "Business, technical, security, and operations owners approve the bounded pilot with no open unaccepted exception.",
        "owner": "Technical Deployment Lead",
        "evidence_id": "E-OPS-02",
        "evidence": "Signed readiness record contains all four approvals and an empty open-exception register.",
        "control_ids": [
          "C-10",
          "C-12"
        ],
        "status": "PASS",
        "blocking": true
      }
    ]
  },
  "slo_and_capacity": {
    "availability_target_percent": 99.5,
    "p95_latency_seconds": 12,
    "protected_action_audit_completeness_percent": 100,
    "unauthorized_protected_actions": 0,
    "monthly_model_cost_budget_usd": 12000,
    "pilot_concurrency_limit": 25
  },
  "pilot_boundary": {
    "cohort": "25 licensed claims adjusters",
    "maximum_claims": 500,
    "duration_days": 14,
    "feature_flag": "claims_ai_assist_pilot",
    "manual_workflow_available": true
  },
  "rollback_triggers": [
    "Any unauthorized protected action",
    "Any confirmed cross-tenant or approved-boundary data exposure",
    "Missing audit evidence for a protected recommendation, approval, or action",
    "Prompt injection changes system policy or reaches a protected tool",
    "p95 latency exceeds 12 seconds for two consecutive monitoring windows",
    "Model cost exceeds the approved daily burn-rate alert"
  ],
  "rollback_action": "Disable claims_ai_assist_pilot, preserve evidence, reconcile uncertain writes by idempotency key, notify accountable owners, and continue the manual claims workflow.",
  "exceptions": [],
  "approvers": [
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
  "decision_options": [
    "READY_FOR_BOUNDED_PILOT",
    "HOLD_FOR_REMEDIATION",
    "REJECT_RELEASE"
  ]
}
```

A readiness checklist is evidence, not optimism. Every item is blocking, names an accountable owner, records a concrete evidence statement, and maps back to one or more threat controls. The four accountable approvers and the empty exception register prevent a technically passing script from becoming an unowned release decision.

### Verification checkpoint

- **Expected result:** The checklist contains all seven categories, 15 unique evidence IDs, a pinned version manifest, four approvals, a bounded pilot, and explicit rollback triggers.
- **Acceptable variation:** A real review may contain `HOLD` or `FAIL` items; the correct outcome is then to hold the release and document remediation.
- **Failure indicator:** Items say only "done," lack owners, lack test or review evidence, or do not map to threat controls.
- **Corrective action:** Replace assertions with specific evidence from a test, configuration review, drill, signed record, or measured result.

## Step 4 — Create the Executable Readiness Review

Create `readiness_review.py`:

```python
#!/usr/bin/env python3
"""Validate a threat model and generate an auditable production-readiness decision."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
THREAT_MODEL_FILE = ROOT / "threat_model.json"
CHECKLIST_FILE = ROOT / "production_readiness_checklist.json"
REPORT_FILE = ROOT / "production_readiness_report.md"

REQUIRED_THREAT_CATEGORIES = {
    "prompt_injection", "tool_abuse", "data_exfiltration", "retrieval_integrity",
    "identity_tenant_isolation", "secrets", "transaction_integrity", "audit",
    "change_management", "denial_of_service",
}
REQUIRED_CHECKLIST_CATEGORIES = {
    "identity_access", "data_protection", "model_tool_guardrails",
    "environments_delivery", "observability_audit", "reliability_recovery",
    "operations_governance",
}


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON artifact with a useful file-specific error."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot load {path.name}: {exc}") from exc


def unique_index(items: list[dict[str, Any]], label: str) -> dict[str, dict[str, Any]]:
    """Index records by unique, non-empty ID."""
    identifiers = [item.get("id") for item in items]
    if any(not identifier for identifier in identifiers):
        raise ValueError(f"{label} must have non-empty IDs")
    if len(identifiers) != len(set(identifiers)):
        raise ValueError(f"{label} IDs must be unique")
    return {item["id"]: item for item in items}


def flatten_checklist(checklist: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    """Return every readiness item while preserving its category."""
    return [
        {**item, "category": category}
        for category, items in checklist.items()
        for item in items
    ]


def validate_inputs(
    model: dict[str, Any], readiness: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    """Validate traceability, ownership, evidence, and release boundaries."""
    errors: list[str] = []
    required_model_sections = {
        "metadata", "decision_boundary", "assets", "trust_boundaries",
        "controls", "threats", "risk_policy",
    }
    missing_model_sections = required_model_sections - set(model)
    if missing_model_sections:
        errors.append("Missing threat-model sections: " + ", ".join(sorted(missing_model_sections)))

    checklist_doc = readiness.get("checklist", {})
    missing_checklist_categories = REQUIRED_CHECKLIST_CATEGORIES - set(checklist_doc)
    extra_checklist_categories = set(checklist_doc) - REQUIRED_CHECKLIST_CATEGORIES
    if missing_checklist_categories:
        errors.append("Missing checklist categories: " + ", ".join(sorted(missing_checklist_categories)))
    if extra_checklist_categories:
        errors.append("Unknown checklist categories: " + ", ".join(sorted(extra_checklist_categories)))

    try:
        assets = unique_index(model.get("assets", []), "Asset")
        boundaries = unique_index(model.get("trust_boundaries", []), "Trust boundary")
        controls = unique_index(model.get("controls", []), "Control")
        threats = list(unique_index(model.get("threats", []), "Threat").values())
        checklist_items = flatten_checklist(checklist_doc)
        unique_index(checklist_items, "Checklist item")
    except ValueError as exc:
        errors.append(str(exc))
        assets, boundaries, controls, threats, checklist_items = {}, {}, {}, [], []

    observed_categories = {threat.get("category") for threat in threats}
    missing_threat_categories = REQUIRED_THREAT_CATEGORIES - observed_categories
    if missing_threat_categories:
        errors.append("Missing threat categories: " + ", ".join(sorted(missing_threat_categories)))

    evidence_ids = [item.get("evidence_id") for item in checklist_items]
    if any(not evidence_id for evidence_id in evidence_ids):
        errors.append("Every checklist item must have an evidence_id")
    if len(evidence_ids) != len(set(evidence_ids)):
        errors.append("Checklist evidence IDs must be unique")
    evidence_set = set(evidence_ids)

    for control in controls.values():
        if control.get("status") != "implemented":
            errors.append(f"{control['id']} is not implemented")
        if not control.get("owner"):
            errors.append(f"{control['id']} has no owner")
        unknown_evidence = set(control.get("evidence_ids", [])) - evidence_set
        if unknown_evidence:
            errors.append(f"{control['id']} references unknown evidence: " + ", ".join(sorted(unknown_evidence)))

    for threat in threats:
        if set(threat.get("asset_ids", [])) - set(assets):
            errors.append(f"{threat['id']} references unknown assets")
        if set(threat.get("trust_boundary_ids", [])) - set(boundaries):
            errors.append(f"{threat['id']} references unknown trust boundaries")
        if set(threat.get("control_ids", [])) - set(controls):
            errors.append(f"{threat['id']} references unknown controls")
        if set(threat.get("verification_evidence_ids", [])) - evidence_set:
            errors.append(f"{threat['id']} references unknown verification evidence")
        if not threat.get("owner"):
            errors.append(f"{threat['id']} has no risk owner")
        if threat.get("residual_risk") in {"critical", "high"}:
            errors.append(f"{threat['id']} retains blocking residual risk")
        if threat.get("disposition") != "MITIGATE":
            errors.append(f"{threat['id']} lacks a MITIGATE disposition")

    mapped_controls = {control_id for item in checklist_items for control_id in item.get("control_ids", [])}
    if mapped_controls - set(controls):
        errors.append("Checklist references unknown controls: " + ", ".join(sorted(mapped_controls - set(controls))))
    if set(controls) - mapped_controls:
        errors.append("Controls without readiness evidence: " + ", ".join(sorted(set(controls) - mapped_controls)))

    for item in checklist_items:
        if item.get("status") not in {"PASS", "HOLD", "FAIL"}:
            errors.append(f"{item.get('id')} has an invalid status")
        if item.get("blocking") is not True:
            errors.append(f"{item.get('id')} must be an explicit blocking check")
        if not item.get("owner") or not item.get("evidence"):
            errors.append(f"{item.get('id')} needs an owner and concrete evidence")

    decision_boundary = model.get("decision_boundary", {})
    if decision_boundary.get("autonomous_protected_actions_allowed") is not False:
        errors.append("Autonomous protected actions must be prohibited")
    if len(decision_boundary.get("protected_actions", [])) < 3:
        errors.append("Protected action boundary is incomplete")

    pilot = readiness.get("pilot_boundary", {})
    if pilot.get("manual_workflow_available") is not True:
        errors.append("The manual claims workflow must remain available")
    if not pilot.get("feature_flag"):
        errors.append("The bounded pilot requires a feature flag")

    expected_roles = {"Business Owner", "Technical Owner", "Security Approver", "Operations Owner"}
    if {item.get("role") for item in readiness.get("approvers", [])} != expected_roles:
        errors.append("Business, technical, security, and operations approvers are required")

    open_exceptions = [
        item for item in readiness.get("exceptions", [])
        if item.get("status") == "OPEN" and item.get("risk_acceptance") != "APPROVED"
    ]
    if open_exceptions:
        errors.append("Open unaccepted production exceptions remain")

    if errors:
        raise ValueError("\n".join(f"- {error}" for error in errors))
    return threats, checklist_items, sorted(mapped_controls)


def decision_for(
    threats: list[dict[str, Any]],
    checklist_items: list[dict[str, Any]],
    approvers: list[dict[str, Any]],
) -> str:
    """Fail closed unless every blocking item and required approval passes."""
    checks_pass = all(item["status"] == "PASS" for item in checklist_items if item["blocking"])
    risks_acceptable = all(threat["residual_risk"] in {"low", "medium"} for threat in threats)
    approvals_complete = bool(approvers) and all(item.get("approved") is True for item in approvers)
    return "READY_FOR_BOUNDED_PILOT" if checks_pass and risks_acceptable and approvals_complete else "HOLD_FOR_REMEDIATION"


def build_report(
    model: dict[str, Any],
    readiness: dict[str, Any],
    threats: list[dict[str, Any]],
    checklist_items: list[dict[str, Any]],
    mapped_controls: list[str],
    decision: str,
) -> str:
    """Render the auditable threat and readiness review."""
    risk_counts = Counter(threat["inherent_risk"] for threat in threats)
    lines = [
        "# Enterprise AI Claims Assistant — Threat Model and Production Readiness",
        "",
        f"- **Decision:** {decision}",
        f"- **Candidate:** {readiness['metadata']['candidate']}",
        f"- **Target:** {readiness['metadata']['target_environment']}",
        f"- **Review date:** {readiness['metadata']['review_date']}",
        "",
        "## Decision Boundary",
        "",
        f"- Primary user: {model['decision_boundary']['primary_user']}",
        "- The assistant may retrieve policy evidence, summarize with citations, and recommend an allowed next step.",
        "- Claim adjudication, payment, reserve changes, customer communication, and claims-system writes remain protected human actions.",
        "",
        "## Threat Summary",
        "",
        f"- Threats reviewed: {len(threats)}",
        f"- Inherent risk: {risk_counts.get('critical', 0)} critical, {risk_counts.get('high', 0)} high, {risk_counts.get('medium', 0)} medium",
        f"- Controls traced to readiness evidence: {len(mapped_controls)}/{len(model['controls'])}",
        "",
        "| Threat | Category | Inherent | Residual | Owner | Controls |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for threat in threats:
        lines.append(
            f"| {threat['id']} | {threat['category']} | {threat['inherent_risk']} | "
            f"{threat['residual_risk']} | {threat['owner']} | {', '.join(threat['control_ids'])} |"
        )

    lines.extend([
        "", "## Production-Readiness Checklist", "",
        "| Category | Check | Status | Owner | Evidence ID |",
        "| --- | --- | --- | --- | --- |",
    ])
    for item in checklist_items:
        lines.append(
            f"| {item['category']} | {item['id']} | {item['status']} | "
            f"{item['owner']} | {item['evidence_id']} |"
        )

    lines.extend(["", "## Version Manifest", "", "| Artifact | Version |", "| --- | --- |"])
    for name, version in readiness["version_manifest"].items():
        lines.append(f"| {name.replace('_', ' ').title()} | {version} |")

    lines.extend(["", "## Required Approvals", ""])
    for approver in readiness["approvers"]:
        state = "Approved" if approver["approved"] else "Pending"
        lines.append(f"- {state} — {approver['role']}: {approver['name']}")

    pilot = readiness["pilot_boundary"]
    lines.extend([
        "", "## Bounded Pilot and Recovery", "",
        f"- Cohort: {pilot['cohort']}",
        f"- Maximum volume: {pilot['maximum_claims']} claims",
        f"- Duration: {pilot['duration_days']} days",
        f"- Feature flag: {pilot['feature_flag']}",
        "- Manual workflow remains available: yes",
        "", "### Rollback triggers", "",
    ])
    lines.extend(f"- {trigger}" for trigger in readiness["rollback_triggers"])
    lines.extend(["", f"**Rollback action:** {readiness['rollback_action']}", ""])
    return "\n".join(lines)


def main() -> int:
    try:
        model = load_json(THREAT_MODEL_FILE)
        readiness = load_json(CHECKLIST_FILE)
        threats, checklist_items, mapped_controls = validate_inputs(model, readiness)

        blocking_failures = [
            item["id"] for item in checklist_items
            if item["blocking"] and item["status"] != "PASS"
        ]
        if blocking_failures:
            raise ValueError("Blocking checks not passed: " + ", ".join(blocking_failures))

        pending_approvals = [
            item["role"] for item in readiness["approvers"]
            if item.get("approved") is not True
        ]
        if pending_approvals:
            raise ValueError("Pending approvals: " + ", ".join(pending_approvals))

        decision = decision_for(threats, checklist_items, readiness["approvers"])
        report = build_report(model, readiness, threats, checklist_items, mapped_controls, decision)
        REPORT_FILE.write_text(report, encoding="utf-8")
    except (KeyError, TypeError, ValueError) as exc:
        print(f"LAB 06 FAILED\n{exc}")
        return 1

    blocking_count = sum(item["blocking"] for item in checklist_items)
    print("LAB 06 PASSED")
    print(f"- Decision: {decision}")
    print(f"- Threats reviewed: {len(threats)}")
    print(f"- Controls traced: {len(mapped_controls)}/{len(model['controls'])}")
    print(f"- Blocking checks passed: {blocking_count}/{blocking_count}")
    print(f"- Report: {REPORT_FILE.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

The program checks both the shape and the meaning of the review. It detects missing threat categories, broken asset or boundary references, unmapped controls, duplicate evidence IDs, non-implemented controls, blocking residual risk, open exceptions, missing approver roles, unpassed checks, and absent pilot safeguards. It then produces a review record from the validated evidence rather than relying on a manually typed decision.

### Verification checkpoint

- **Expected result:** The script reads the two JSON files, validates all cross-references, fails closed on incomplete evidence, and generates `production_readiness_report.md`.
- **Acceptable variation:** You may split the code into additional learner-built modules if your guide and final repository teach every file.
- **Failure indicator:** The code approves based only on a count, ignores unknown IDs, or treats human approvals and rollback as optional.
- **Corrective action:** Restore explicit references, blocking gates, all four approver roles, and fail-closed validation before continuing.

## Step 5 — Run the Production-Readiness Review

Compile and execute the review:

```bash
python3 -m py_compile readiness_review.py
python3 readiness_review.py
```

Expected terminal output:

```text
LAB 06 PASSED
- Decision: READY_FOR_BOUNDED_PILOT
- Threats reviewed: 10
- Controls traced: 12/12
- Blocking checks passed: 15/15
- Report: production_readiness_report.md
```

Inspect the generated report:

```bash
sed -n '1,260p' production_readiness_report.md
```

On Windows PowerShell, use:

```powershell
Get-Content production_readiness_report.md
```

Confirm that the report includes the protected-action boundary, all ten threats, all fifteen readiness checks, the exact version manifest, four approvals, the 25-adjuster/500-claim/14-day pilot boundary, the feature flag, the manual workflow, and all rollback triggers.

### Verification checkpoint

- **Expected result:** The command exits successfully, prints `READY_FOR_BOUNDED_PILOT`, and generates a complete report.
- **Acceptable variation:** If you intentionally change a blocking check to `HOLD`, a failed command is the correct control outcome. Restore the passing reference state afterward.
- **Failure indicator:** The command prints `LAB 06 FAILED`, a control is untraced, an evidence ID is unknown, or the generated report omits a release boundary.
- **Corrective action:** Read the exact validation message, repair the named ownership, reference, evidence, approval, or pilot-boundary issue, and rerun both commands.

## Step 6 — Review the Decision Like an FDE Lead

Before accepting the result, answer these release questions in your own notes:

1. Does the protected-action boundary match what the system technically enforces?
2. Does every high-impact threat have a preventive, detective, or corrective control with evidence?
3. Can the team identify the exact user, tenant, model, prompt, retrieval index, evidence, approval, and action for a protected decision?
4. Can operators disable AI assistance without disabling manual claims work?
5. Does every rollback trigger have observable evidence and a named responder?
6. Would a version change invalidate the evidence that justified this decision?

Why this matters: the executable check verifies internal consistency. Accountable reviewers still judge whether the evidence is credible, current, and sufficient for the actual customer environment.

### Verification checkpoint

- **Expected result:** You can defend the decision using concrete control evidence and operational boundaries.
- **Acceptable variation:** You may narrow the pilot further if evidence supports a smaller blast radius.
- **Failure indicator:** Your defense depends on "the model should behave" or an undocumented manual workaround.
- **Corrective action:** Add an enforcing control, measurable evidence, accountable owner, or narrower release boundary.

## Step 7 — Commit Your Evidence

Initialize and commit your own completed project:

```bash
git init -b main
git add .gitignore threat_model.json production_readiness_checklist.json readiness_review.py production_readiness_report.md
git commit -m "Complete AI threat model and production readiness review"
git status --short --branch
```

### Verification checkpoint

- **Expected result:** Git reports branch `main` with no uncommitted changes.
- **Acceptable variation:** Another clear commit message is acceptable.
- **Failure indicator:** The report is missing, Python caches are tracked, or the working tree is dirty.
- **Corrective action:** Run the review again, confirm `.gitignore`, stage the five intended project files, and commit.

## Map the Completed Workflow

1. Bound the assistant's allowed decisions and protected human actions.
2. Identify assets and trust boundaries across the user, retrieval, model, claims-system, and audit paths.
3. Describe concrete abuse and failure scenarios with inherent and residual risk.
4. Map each threat to owned preventive, detective, or corrective controls.
5. Bind every control to production-readiness evidence.
6. Validate identity, data, model, tool, environment, audit, reliability, recovery, and governance checks.
7. Require business, technical, security, and operations approvals.
8. Release only to a feature-flagged, time-, volume-, and cohort-limited pilot with a manual path.
9. Monitor explicit rollback triggers and preserve evidence for incident response and reevaluation.

## Troubleshooting Cheatsheet

| Symptom | Likely cause | Corrective action |
| --- | --- | --- |
| `Cannot load ...` | Missing file, malformed JSON, or wrong working directory | Run from the project root and validate the named JSON file |
| Unknown asset, boundary, control, or evidence | A cross-reference is misspelled or absent | Compare the exact IDs and restore one traceable record |
| Missing threat categories | A required production risk was omitted | Add the named category with a concrete scenario and controls |
| Control has no readiness evidence | Checklist mapping is incomplete | Add the control ID to the relevant evidenced readiness item |
| Blocking residual risk | A threat still has high or critical residual risk | Add and verify controls, narrow the pilot, or hold the release |
| Blocking check not passed | Evidence is incomplete or a control failed | Remediate and rerun; do not change the status without evidence |
| Pending approvals | An accountable owner has not accepted the evidence | Keep the release on hold until the named approval is recorded |
| Report is stale | JSON inputs changed after the last run | Run `python3 readiness_review.py` again and review the generated report |

## Cleanup

This lab creates no cloud resources and makes no network calls. To remove only Python cache files from your project:

```bash
python3 -c "import shutil; shutil.rmtree('__pycache__', ignore_errors=True)"
```

Keep the four learner-built artifacts, `.gitignore`, and Git history as portfolio evidence.

## Completion Check

- [ ] I defined the allowed assistance and protected human actions.
- [ ] I identified all six assets and five trust boundaries.
- [ ] I modeled all ten required threat categories.
- [ ] Every threat has an owner, controls, evidence, and acceptable residual risk.
- [ ] All twelve controls trace to readiness evidence.
- [ ] All fifteen blocking checks pass across seven categories.
- [ ] I pinned the application, model, prompt, retrieval, schema, dataset, and infrastructure versions.
- [ ] I preserved four accountable approvals and an empty unaccepted-exception register.
- [ ] I limited the pilot by cohort, volume, time, feature flag, and manual fallback.
- [ ] I generated and reviewed `production_readiness_report.md`.
- [ ] I committed the completed evidence in my own repository.

## Reflection

1. Which threat should force an immediate rollback even if no customer harm is yet confirmed?
2. Which control is most important for preventing a recommendation from becoming an unauthorized action?
3. What new evidence must be collected if the model or retrieval index changes?
4. Which medium residual risk would you narrow through pilot scope rather than additional engineering?
5. What would make you reject the release instead of holding it for remediation?

