# Lab 03 — Create a Customer Discovery Brief and AI Value Case

## Goal

Assess the Enterprise AI Claims Assistant as a measurable, bounded opportunity and recommend whether Northstar Mutual should pilot, prototype, pause, or stop.

## What You'll Build or Produce

In your own project directory, you will create:

- `claims_assistant_discovery_packet.md` — the verified discovery evidence, stakeholders, data readiness, and constraints.
- `discovery_brief.json` — the qualified problem, AI fit, bounded pilot, governance, risks, exit criteria, and recommendation.
- `value_hypothesis.csv` — baselines, targets, sources, owners, and decision use.
- `run_lab.py` — the learner-built validator that checks the completed value case and prints the pilot decision evidence.

The completed course repository contains the finished version of these same four project files. Use it only when stuck or comparing your result.

## Estimated Time

45–60 minutes.

## Cost Guardrails

This lab runs locally and costs $0. Do not upload claim data, call a model API, use customer credentials, or provision cloud resources.

## Completion Evidence

You are finished when `run_lab.py` compiles and passes, the brief clearly separates facts from assumptions, the recommendation is a bounded pilot with named prerequisites, human approval remains 100%, and your own Git working tree is clean.

## Prerequisites

- Python 3.10 or later for local JSON and CSV checks.
- Git, a terminal, and a text editor.
- Basic JSON and CSV familiarity.
- An understanding of discovery, AI fit, data readiness, ownership, and human approval.

## Where This Lab Fits

This lab uses the problem framing from Lab 01 and the ownership boundaries from Lab 02. You will test assumptions, assess AI and data readiness, define measurable value, and recommend a bounded next step. Its output becomes the decision evidence used by the architecture lab.

## Step 1 — Create Your Independent Project

```bash
mkdir fde_lab_03
cd fde_lab_03
```

Do not edit the completed reference repository. Build the project from this guide and consult the reference only if needed.

### Verification checkpoint

- **Expected result:** You are inside an empty `fde_lab_03` directory.
- **Acceptable variation:** Another directory name is acceptable.
- **Failure indicator:** You are changing files inside `lab_03_customer_discovery_brief_ai_value_case`.
- **Corrective action:** Leave the reference repository and create your own directory.

## Step 2 — Create the Discovery Packet

Create `claims_assistant_discovery_packet.md`:

```markdown
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
```

Why this matters: discovery begins with evidence. The 28-minute effort estimate is explicitly unvalidated and must not be presented as confirmed ROI.

### Verification checkpoint

- **Expected result:** The packet contains five baseline rows, five named owners, four data sources, a bounded pilot, and protected actions.
- **Acceptable variation:** Markdown formatting may differ; evidence and uncertainty labels must not.
- **Failure indicator:** Assumptions are presented as verified facts or protected actions become automated.
- **Corrective action:** Restore evidence sources, ownership, uncertainty, and the human approval boundary.

## Step 3 — Build the Discovery Brief

Create `discovery_brief.json`:

```json
{
  "engagement": {
    "lab_id": "lab_03",
    "customer": "Northstar Mutual",
    "initiative": "Enterprise AI Claims Assistant",
    "prepared_by": "FDE Discovery Team",
    "decision_date": "2026-08-16"
  },
  "problem": {
    "problem_statement": "Licensed claims adjusters wait too long for complete, evidence-linked intake summaries, contributing to an 18-hour median intake-to-assignment time, 22% intake rework, and incomplete audit evidence.",
    "primary_user": "Licensed Claims Adjuster",
    "business_owner": "Elena Ruiz, VP of Claims Operations",
    "current_workflow": [
      "Receive claim intake forms and supporting documents.",
      "Verify policy, claimant, and loss details across systems.",
      "Read documents and assemble a source-linked evidence summary.",
      "Identify missing information and select a routing queue.",
      "Record the rationale and assign the claim for adjuster review."
    ],
    "frictions": [
      "Evidence is fragmented across email, scans, policy systems, and the claims platform.",
      "Intake summaries are written manually and vary by specialist.",
      "Incorrect or missing intake information causes 22% rework.",
      "Only 71% of audit records contain complete source citations."
    ],
    "non_goals": [
      "Autonomously approve or deny a claim.",
      "Authorize payment or change reserves.",
      "Send customer communications or update the system of record without human approval."
    ]
  },
  "decision_contract": {
    "user": "Licensed Claims Adjuster",
    "decision": "Choose whether to request evidence, continue review, or escalate the claim.",
    "assistant_action": "Present a source-linked summary, identify missing information, and recommend one allowed workflow action.",
    "expected_outcome": "Reduce intake delay and avoidable rework while improving citation completeness.",
    "human_authority": "A licensed claims adjuster approves, changes, or rejects every recommendation before any downstream action."
  },
  "ai_fit": {
    "is_ai_appropriate": true,
    "reasons": [
      "The workflow requires summarizing variable free text and semi-structured documents.",
      "Recommendations can be evaluated against reviewed historical claims and cited sources.",
      "A licensed adjuster remains accountable for the final claim decision and action."
    ],
    "deterministic_alternatives": [
      "Use field-level rules for completeness checks on structured intake forms.",
      "Fix policy-document version metadata and improve the existing intake checklist."
    ]
  },
  "data_readiness": {
    "sources": [
      {
        "name": "Claim intake forms",
        "owner": "Claims Data",
        "readiness": "conditional",
        "constraint": "Profile the 3% missing structured fields by claim type."
      },
      {
        "name": "Policy documents",
        "owner": "Policy Administration",
        "readiness": "not_ready",
        "constraint": "Normalize version and effective-date labels before retrieval evaluation."
      },
      {
        "name": "Adjuster notes",
        "owner": "Claims Operations",
        "readiness": "conditional",
        "constraint": "Review abbreviations, sensitive text, and access rules."
      }
    ],
    "gaps": [
      "Create a reviewed evaluation set representing claim types, missing evidence, and escalation conditions.",
      "Resolve policy-document version and effective-date metadata before pilot ingestion."
    ],
    "security_constraints": [
      "Keep personally identifiable information inside Northstar's approved environment.",
      "Exclude restricted fraud indicators from the first pilot.",
      "Audit source retrieval, recommendation, human decision, and downstream action."
    ]
  },
  "pilot": {
    "duration_weeks": 8,
    "teams": 3,
    "maximum_claims": 1500,
    "included_actions": [
      "Recommend request evidence.",
      "Recommend continue review.",
      "Recommend escalate."
    ],
    "excluded_actions": [
      "Approve or deny a claim.",
      "Authorize payment or change reserves.",
      "Send customer communications or update the claims system."
    ]
  },
  "governance": {
    "owners": {
      "business_owner": "Elena Ruiz, VP of Claims Operations",
      "user_representative": "Marcus Lee, Senior Claims Adjuster",
      "data_owner": "Priya Shah, Director of Claims Data",
      "technical_owner": "Jordan Kim, Forward Deployed Engineering Lead",
      "security_approver": "Dana Brooks, Information Security Director"
    },
    "human_approval": {
      "required": true,
      "role": "Licensed Claims Adjuster",
      "protected_actions": [
        "Approve or deny a claim.",
        "Authorize payment or change reserves.",
        "Send customer communications or update the claims system of record."
      ]
    },
    "scale_gate": {
      "status": "pending",
      "owner": "Elena Ruiz, VP of Claims Operations",
      "evidence_required": [
        "Quality results by claim type on a reviewed evaluation set.",
        "Zero unauthorized protected actions and complete audit records.",
        "Pilot targets for cycle time, rework, citations, and adoption."
      ]
    }
  },
  "risks": [
    {
      "risk": "The assistant cites the wrong policy version.",
      "owner": "Priya Shah",
      "mitigation": "Normalize effective-date metadata and test retrieval by policy version."
    },
    {
      "risk": "Users over-trust a plausible summary.",
      "owner": "Marcus Lee",
      "mitigation": "Display source links, require an explicit adjuster decision, and review overrides."
    },
    {
      "risk": "PII leaves the approved boundary.",
      "owner": "Dana Brooks",
      "mitigation": "Use approved hosting, least privilege, redaction tests, and audit logging."
    },
    {
      "risk": "Pilot results overrepresent simple claims.",
      "owner": "Jordan Kim",
      "mitigation": "Stratify evaluation and pilot samples by claim type and complexity."
    }
  ],
  "discovery_exit_criteria": [
    {
      "criterion": "Business owner confirms the problem, baseline, and pilot scope.",
      "owner": "Elena Ruiz",
      "status": "met"
    },
    {
      "criterion": "User representative confirms the workflow and human approval boundary.",
      "owner": "Marcus Lee",
      "status": "met"
    },
    {
      "criterion": "Data owner accepts the source inventory and remediation plan.",
      "owner": "Priya Shah",
      "status": "met"
    },
    {
      "criterion": "Security approver accepts the pilot data boundary and audit requirements.",
      "owner": "Dana Brooks",
      "status": "pending"
    },
    {
      "criterion": "Steering committee accepts measurable pilot targets and stop conditions.",
      "owner": "Elena Ruiz",
      "status": "pending"
    }
  ],
  "recommendation": {
    "decision": "pilot",
    "rationale": "Proceed only with a bounded, human-approved pilot after policy-version metadata and the representative evaluation set are ready; do not authorize autonomous claim decisions or production scale-up during discovery.",
    "prerequisites": [
      "Normalize policy version and effective-date metadata.",
      "Build and approve a representative evaluation set.",
      "Obtain Security approval for the pilot data boundary and audit design."
    ]
  }
}
```

Why this matters: the brief turns raw discovery into a decision contract, AI-fit assessment, data-remediation plan, bounded experiment, governance model, and recommendation.

### Verification checkpoint

- **Expected result:** The brief defines the user, decision, assistant action, expected outcome, human authority, AI-fit rationale, deterministic alternatives, data gaps, pilot boundary, owners, risks, exit criteria, and recommendation.
- **Acceptable variation:** A prototype or pause recommendation is acceptable only if the evidence and prerequisites support it.
- **Failure indicator:** The recommendation has no prerequisites, owners are missing, or AI is assumed to be the answer without alternatives.
- **Corrective action:** Connect the recommendation to verified evidence, unresolved gaps, accountable owners, and explicit exit criteria.

## Step 4 — Build the Value Hypothesis

Create `value_hypothesis.csv`:

```csv
metric_id,metric_name,baseline,target,direction,unit,source,owner,decision_use
median_intake_to_assignment_hours,Median intake-to-assignment time,18,6,lower,hours,Claims platform,Elena Ruiz,Scale gate
intake_rework_rate_percent,Intake rework rate,22,10,lower,percent,Quality review,Marcus Lee,Scale gate
citation_completeness_percent,Citation completeness,71,95,higher,percent,Audit log,Dana Brooks,Scale gate
human_approval_rate_percent,Human approval for protected actions,100,100,equal,percent,Claims platform,Elena Ruiz,Safety stop
weekly_active_adjusters_percent,Weekly active adjusters,0,75,higher,percent,Usage telemetry,Marcus Lee,Adoption review
```

Why this matters: model quality is not the business outcome. This artifact ties cycle time, rework, evidence quality, safety, and adoption to baselines, targets, sources, owners, and decisions.

### Verification checkpoint

- **Expected result:** Five metrics are present and human approval remains 100% from baseline through target.
- **Acceptable variation:** You may add a metric if its source, owner, and decision use are explicit.
- **Failure indicator:** A metric has no baseline or source, or a speed/adoption target weakens the safety boundary.
- **Corrective action:** Restore complete measurement contracts and 100% approval for protected actions.

## Step 5 — Build the Project Validator

Why this matters: discovery claims become decision-ready only when the artifacts can be checked consistently. You will build the same validator contained in the completed reference repository.

Create `run_lab.py`:

```python
#!/usr/bin/env python3
"""Run Lab 03: validate the discovery brief and AI value hypothesis."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
OWNER_ROLES = {
    "business_owner", "user_representative", "data_owner",
    "technical_owner", "security_approver",
}
METRICS = {
    "median_intake_to_assignment_hours",
    "intake_rework_rate_percent",
    "citation_completeness_percent",
    "human_approval_rate_percent",
    "weekly_active_adjusters_percent",
}


def incomplete(value: Any) -> bool:
    if isinstance(value, str):
        return not value.strip() or any(token in value.lower() for token in ("todo", "tbd"))
    if isinstance(value, list):
        return not value or any(incomplete(item) for item in value)
    if isinstance(value, dict):
        return not value or any(incomplete(item) for item in value.values())
    return value is None


def main() -> int:
    brief = json.loads((ROOT / "discovery_brief.json").read_text(encoding="utf-8"))
    with (ROOT / "value_hypothesis.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    errors: list[str] = []
    required = (
        "engagement", "problem", "decision_contract", "ai_fit", "data_readiness",
        "pilot", "governance", "risks", "discovery_exit_criteria", "recommendation",
    )
    for section in required:
        if section not in brief or incomplete(brief[section]):
            errors.append(f"Discovery section is incomplete: {section}")

    owners = brief.get("governance", {}).get("owners", {})
    if set(owners) != OWNER_ROLES:
        errors.append("All five governance owners are required")
    approval = brief.get("governance", {}).get("human_approval", {})
    if approval.get("required") is not True:
        errors.append("Human approval must remain required")
    protected = " ".join(approval.get("protected_actions", [])).lower()
    if "approve or deny" not in protected or "payment" not in protected:
        errors.append("Protected claim decisions and payment must remain human-controlled")

    ids = {row.get("metric_id", "") for row in rows}
    if ids != METRICS:
        errors.append("The value hypothesis must contain the five required metrics")
    human = next((row for row in rows if row.get("metric_id") == "human_approval_rate_percent"), {})
    if human.get("baseline") != "100" or human.get("target") != "100":
        errors.append("Human approval baseline and target must both be 100 percent")
    for row in rows:
        try:
            baseline = float(row["baseline"])
            target = float(row["target"])
        except (KeyError, ValueError):
            errors.append(f"{row.get('metric_id', 'metric')}: baseline and target must be numeric")
            continue
        direction = row.get("direction")
        if direction == "lower" and target >= baseline:
            errors.append(f"{row['metric_id']}: target must be lower than baseline")
        if direction == "higher" and target <= baseline:
            errors.append(f"{row['metric_id']}: target must be higher than baseline")
        if direction == "equal" and target != baseline:
            errors.append(f"{row['metric_id']}: target must equal baseline")

    if errors:
        print(f"LAB 03 FAILED — {len(errors)} issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print("LAB 03 PASSED")
    print(f"- Recommendation: {brief['recommendation']['decision']}")
    print(f"- Metrics: {len(rows)}")
    print(f"- Risks: {len(brief['risks'])}")
    print(f"- Pilot: {brief['pilot']['duration_weeks']} weeks, {brief['pilot']['teams']} teams, {brief['pilot']['maximum_claims']} claims maximum")
    print("- Human approval for protected actions: 100%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### Verification checkpoint

- **Expected result:** `run_lab.py` contains the complete validator above.
- **Acceptable variation:** Comments or formatting may differ if validation behavior and printed evidence remain equivalent.
- **Failure indicator:** The file is missing, truncated, or references different artifact names.
- **Corrective action:** Replace it with the complete source above and save it beside the three project artifacts.

## Step 6 — Compile and Run the Completed Project

Why this matters: compilation catches Python syntax errors; the main run verifies the discovery brief, value hypothesis, approval boundary, pilot scope, and recommendation together.

Run:

```bash
python3 -m py_compile run_lab.py
python3 run_lab.py
```

Expected output:

```text
LAB 03 PASSED
- Recommendation: pilot
- Metrics: 5
- Risks: 4
- Pilot: 8 weeks, 3 teams, 1500 claims maximum
- Human approval for protected actions: 100%
```

### Verification checkpoint

- **Expected result:** Compilation is silent and the validator prints `LAB 03 PASSED` with the five evidence lines.
- **Acceptable variation:** Your Python executable may be named `python` instead of `python3`.
- **Failure indicator:** A traceback, `LAB 03 FAILED`, missing evidence, or a nonzero exit status.
- **Corrective action:** Read the reported error, compare the named field with the guide, repair the artifact or validator, and rerun both commands.

## Step 7 — Inspect the Pilot Recommendation

Why this matters: passing syntax is not enough. A forward deployed leader must be able to explain why the evidence supports a bounded pilot rather than an unrestricted launch.

Review the generated terminal evidence and confirm:

- the recommendation is `pilot`;
- the pilot lasts eight weeks;
- three teams and no more than 1,500 claims are in scope;
- the five metrics cover approval safety, quality, speed, rework, and adoption;
- all four risks have owners and mitigations;
- protected actions require 100% human approval.

### Verification checkpoint

- **Expected result:** Every statement above is supported by `discovery_brief.json`, `value_hypothesis.csv`, and the validator output.
- **Acceptable variation:** You may describe the decision in your own words without changing the numeric boundaries.
- **Failure indicator:** A claim lacks a source, an owner, a threshold, or a bounded pilot constraint.
- **Corrective action:** Return to the relevant artifact, add evidence-backed detail, and rerun `python3 run_lab.py`.

## Step 8 — Commit Your Completed Project

Why this matters: a clean commit creates reviewable evidence of the exact discovery decision package you completed.

Run in your own project directory:

```bash
printf '__pycache__/\n*.py[cod]\n.DS_Store\n' > .gitignore
git init -b main
git add .gitignore claims_assistant_discovery_packet.md discovery_brief.json value_hypothesis.csv run_lab.py
git commit -m "Complete customer discovery brief and AI value case"
git status
```

### Verification checkpoint

- **Expected result:** Git creates a commit on `main` and reports a clean working tree.
- **Acceptable variation:** An existing repository may already be initialized; commit the same four project files and `.gitignore`.
- **Failure indicator:** A cache or unintended file is staged, or Git reports uncommitted changes.
- **Corrective action:** Remove transient files, stage only `.gitignore` and the four learner-built files, commit, and rerun `git status`.

## Map the Completed Workflow

1. The discovery packet separates verified evidence from assumptions and identifies owners.
2. The discovery brief qualifies the problem, AI fit, data readiness, governance, risks, and pilot.
3. The value hypothesis defines how safety, quality, speed, rework, and adoption will be measured.
4. Your Python validator checks the artifacts and prints the decision evidence.
5. The steering committee receives a bounded pilot recommendation with explicit prerequisites.

## Troubleshooting Cheatsheet

| Symptom | Likely cause | Corrective action |
| --- | --- | --- |
| JSON line/column error | Invalid JSON punctuation | Repair the location reported by `json.tool` |
| Missing discovery section | Required object is absent or empty | Add the named evidence-supported section |
| Validator fails | Missing field, metric, risk, or pilot boundary | Use the reported message to repair the named artifact |

## Cleanup

Keep `claims_assistant_discovery_packet.md`, `discovery_brief.json`, `value_hypothesis.csv`, `run_lab.py`, `.gitignore`, and your Git history. No additional cleanup is required after the project passes and the working tree is clean.

## Completion Check

- [ ] I created the packet, discovery brief, value hypothesis, and Python validator from this guide.
- [ ] `run_lab.py` compiles and prints `LAB 03 PASSED`.
- [ ] The value hypothesis contains five complete metrics.
- [ ] Human approval remains exactly 100% for protected actions.
- [ ] The recommendation is bounded and prerequisite-driven.
- [ ] My own Git working tree is clean.

## Reflection

Which discovery finding would most likely change the recommendation from pilot to prototype or pause, and what evidence would you request?
