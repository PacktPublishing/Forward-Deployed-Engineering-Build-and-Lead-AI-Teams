# Lab 02 — Build a Forward Deployed Role Charter and RACI Matrix

## Goal

Define a clear Forward Deployed Lead operating contract and assign accountable ownership for the Enterprise AI Claims Assistant without taking over customer business-policy authority.

## What You'll Build or Produce

In your own project directory, you will create:

- `claims_assistant_brief.md` — the engagement evidence and operating boundaries.
- `role_charter.json` — the Forward Deployed Lead’s mission, outcomes, decision rights, escalation paths, metrics, and limits.
- `raci_matrix.csv` — responsibility and accountability across nine delivery decisions.
- `run_lab.py` — the learner-built charter and RACI validator.

The completed course repository contains the finished version of these same four project files. Consult it only when stuck or comparing your result.

## Estimated Time

40–55 minutes.

## Cost Guardrails

This local analysis lab costs $0. It uses no cloud resources, credentials, model calls, or third-party packages.

## Completion Evidence

You are finished when `run_lab.py` compiles, the JSON and CSV parse successfully, the charter preserves customer authority, every RACI row has exactly one Accountable role and at least one Responsible role, Claims Operations owns go-live, and your own Git working tree is clean.

## Prerequisites

- Python 3.10 or later for local JSON and CSV checks.
- Git, a terminal, and a text editor.
- Basic JSON, CSV, and RACI familiarity.

## Where This Lab Fits

This lab builds on Lab 01's lifecycle map. You are not redesigning the customer problem; you are defining who owns delivery decisions, who holds customer business authority, and when escalation is required. Clear ownership must exist before discovery, architecture, and release work becomes complex.

## Step 1 — Create Your Independent Project

```bash
mkdir fde_lab_02
cd fde_lab_02
```

Do not edit the completed course repository. Your directory should become the project you build from this guide.

### Verification checkpoint

- **Expected result:** You are inside an empty `fde_lab_02` directory.
- **Acceptable variation:** Another directory name is fine.
- **Failure indicator:** You are changing files inside `lab_02_forward_deployed_role_charter_raci`.
- **Corrective action:** Leave the reference repository and create a separate working directory.

## Step 2 — Create the Engagement Brief

Create `claims_assistant_brief.md`:

```markdown
# Enterprise AI Claims Assistant — Engagement Brief

Northstar Mutual processes property claims through email, scanned forms, policy systems, and a claims platform. Intake specialists manually summarize each submission, find policy evidence, identify missing information, and assign the claim to an adjuster queue.

## Current baseline

- Median intake-to-assignment time: 18 hours
- Claims returned for missing or incorrect intake information: 22%
- Audit records containing complete source citations: 71%
- Claim denials or payments requiring human approval: 100%

## Pilot scope

The assistant may summarize submissions, retrieve policy evidence, identify missing information, recommend a routing queue, and draft an adjuster work note. It may not approve or deny a claim, authorize payment, change a policy record, or send a customer-facing decision without human approval.

## Target outcomes

- Reduce median intake-to-assignment time to 6 hours or less
- Reduce intake rework to 10% or less
- Achieve at least 95% complete evidence-and-citation records
- Preserve 100% human approval for claim denials and payments

## Operating constraints

- Claims Operations owns business-policy decisions and go-live approval.
- Security and Compliance owns interpretation of regulatory controls.
- The Forward Deployed Lead owns end-to-end technical delivery and evidence.
- Customer production access requires named, least-privilege service accounts.
- Unresolved safety, regulatory, or production-readiness risk must be escalated before release.
```

Why this matters: a role charter must be tied to specific customer outcomes, protected actions, and decision owners rather than a generic job description.

### Verification checkpoint

- **Expected result:** The brief identifies four baselines, four targets, protected claim actions, and Claims Operations go-live authority.
- **Acceptable variation:** Markdown wrapping may differ; facts and boundaries must not.
- **Failure indicator:** The Forward Deployed Lead can approve claims, payments, regulatory risk, or customer go-live.
- **Corrective action:** Restore the ownership and human-approval constraints.

## Step 3 — Build the Role Charter

Create `role_charter.json`:

```json
{
  "role_id": "fde_lead",
  "role_name": "Forward Deployed Lead",
  "mission": "Lead Northstar Mutual from a validated claims-intake problem to a secure, measurable, and supportable AI deployment while preserving customer decision rights.",
  "primary_customer": "Claims Operations Owner",
  "owned_outcomes": [
    "A production decision supported by architecture, evaluation, security, and operational evidence",
    "A clear owner and acceptance criterion for every delivery workstream",
    "A controlled transition from the deployment team to Claims Operations"
  ],
  "key_activities": [
    "Translate the claims workflow into delivery workstreams and acceptance evidence",
    "Coordinate AI, platform, security, operations, and adjuster stakeholders",
    "Maintain the integrated decision log, risk view, and readiness evidence",
    "Present evidence-based proceed, repair, pause, or escalate recommendations"
  ],
  "decision_rights": [
    "Approve the technical delivery baseline and changes within agreed scope",
    "Reject incomplete technical evidence and require remediation before review",
    "Pause deployment activity when a safety, security, reliability, or customer-control threshold is breached",
    "Recommend go-live; final production authorization remains with the Claims Operations Owner"
  ],
  "escalation_paths": [
    {
      "trigger": "A proposed capability could approve or deny a claim, authorize payment, or send a customer decision without human approval",
      "escalate_to": "Claims Operations Owner and Security FDE",
      "evidence_required": "Affected workflow, proposed permission, control gap, user impact, and safer options"
    },
    {
      "trigger": "A security, regulatory, or data-boundary control cannot be met before the release date",
      "escalate_to": "Security and Compliance Lead",
      "evidence_required": "Control requirement, current gap, exposure, compensating controls, owner, and decision deadline"
    },
    {
      "trigger": "A critical dependency threatens the agreed outcome or milestone",
      "escalate_to": "Customer Sponsor and Technical Deployment Lead",
      "evidence_required": "Dependency, impact, attempted resolution, options, recommendation, and decision needed"
    }
  ],
  "success_metrics": [
    {
      "metric": "Median intake-to-assignment time",
      "target": "6 hours or less during the pilot",
      "measurement_source": "Claims platform event timestamps"
    },
    {
      "metric": "Claims returned for intake rework",
      "target": "10% or less during the pilot",
      "measurement_source": "Claims operations quality report"
    },
    {
      "metric": "Complete evidence-and-citation records",
      "target": "95% or more of evaluated claims",
      "measurement_source": "AI evaluation and audit report"
    },
    {
      "metric": "Human approval for claim denials and payments",
      "target": "100%",
      "measurement_source": "Claims decision audit log"
    }
  ],
  "out_of_scope": [
    "Owning Northstar Mutual business policy",
    "Approving claim denials or payments",
    "Accepting regulatory risk on behalf of the customer",
    "Serving as the permanent production operations owner"
  ]
}
```

Why this matters: the charter defines what the Forward Deployed Lead owns, what evidence supports decisions, when escalation is mandatory, and where customer authority begins.

### Verification checkpoint

- **Expected result:** The charter contains a mission, three owned outcomes, four activities, four decision rights, three escalation paths, four success metrics, and explicit out-of-scope boundaries.
- **Acceptable variation:** Wording may improve if the same outcomes, evidence, and authority boundaries remain clear.
- **Failure indicator:** The role owns Northstar business policy, approves protected claim actions, or accepts regulatory risk for the customer.
- **Corrective action:** Separate technical delivery responsibility from customer authorization and policy ownership.

## Step 4 — Build the RACI Matrix

Create `raci_matrix.csv`:

```csv
work_item,fde_lead,ai_fde,platform_fde,security_fde,deployment_strategist,claims_owner,adjuster_lead
Approve discovery exit,R,C,I,C,C,A,C
Approve architecture baseline,A,R,C,C,I,C,I
Create evaluation dataset,C,R,I,C,I,C,A
Approve AI release criteria,A,R,I,C,I,C,C
Approve security readiness,A,C,C,R,I,C,I
Authorize production go-live,R,C,C,C,I,A,C
Own adoption and workflow change,C,I,I,I,R,A,C
Lead production incident response,A,C,R,C,I,I,I
Review business outcomes,C,I,I,I,R,A,C
```

Use these meanings:

- `R` — performs the work.
- `A` — owns the final decision; exactly one per row.
- `C` — provides input before the decision.
- `I` — is informed after the decision.

Why this matters: the charter explains the role; the RACI makes ownership testable at each delivery decision.

### Verification checkpoint

- **Expected result:** Nine work items are mapped, every row has one `A` and at least one `R`, and `claims_owner` is `A` for production go-live.
- **Acceptable variation:** Additional Consulted roles are acceptable when they do not create duplicate accountability.
- **Failure indicator:** A row has zero or multiple `A` values, no `R`, or the FDE Lead authorizes customer go-live.
- **Corrective action:** Assign one final decision owner and at least one delivery owner per row.

## Step 5 — Build the Python Validator

Create `run_lab.py` with this complete source:

```python
#!/usr/bin/env python3
"""Run Lab 02: validate the Forward Deployed role charter and RACI matrix."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
ROLES = {
    "fde_lead", "ai_fde", "platform_fde", "security_fde",
    "deployment_strategist", "claims_owner", "adjuster_lead",
}


def incomplete(value: Any) -> bool:
    if isinstance(value, str):
        return not value.strip() or "todo" in value.lower()
    if isinstance(value, list):
        return not value or any(incomplete(item) for item in value)
    if isinstance(value, dict):
        return not value or any(incomplete(item) for item in value.values())
    return value is None


def main() -> int:
    charter = json.loads((ROOT / "role_charter.json").read_text(encoding="utf-8"))
    with (ROOT / "raci_matrix.csv").open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        headers = list(reader.fieldnames or [])
        rows = list(reader)

    errors: list[str] = []
    required = (
        "role_id", "role_name", "mission", "primary_customer", "owned_outcomes",
        "key_activities", "decision_rights", "escalation_paths",
        "success_metrics", "out_of_scope",
    )
    for field in required:
        if field not in charter or incomplete(charter[field]):
            errors.append(f"Role charter field is incomplete: {field}")

    if charter.get("role_id") != "fde_lead":
        errors.append("role_id must be fde_lead")
    if len(charter.get("decision_rights", [])) < 4:
        errors.append("At least four decision rights are required")
    boundaries = " ".join(charter.get("out_of_scope", [])).lower()
    if "claim denials" not in boundaries or "payments" not in boundaries:
        errors.append("The charter must preserve human claim-denial and payment authority")

    if not headers or headers[0] != "work_item" or set(headers[1:]) != ROLES:
        errors.append("RACI headers do not match the required roles")
    if len(rows) != 9:
        errors.append("RACI must contain nine delivery decisions")
    for row in rows:
        values = [row.get(role, "").upper() for role in headers[1:]]
        if values.count("A") != 1:
            errors.append(f"{row.get('work_item')}: exactly one Accountable role is required")
        if "R" not in values:
            errors.append(f"{row.get('work_item')}: at least one Responsible role is required")
        if any(value not in {"R", "A", "C", "I"} for value in values):
            errors.append(f"{row.get('work_item')}: invalid RACI code")
    go_live = next((row for row in rows if "go-live" in row.get("work_item", "").lower()), {})
    if go_live.get("claims_owner") != "A":
        errors.append("Claims owner must be Accountable for production go-live")

    if errors:
        print(f"LAB 02 FAILED — {len(errors)} issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print("LAB 02 PASSED")
    print(f"- Role: {charter['role_name']}")
    print(f"- Owned outcomes: {len(charter['owned_outcomes'])}")
    print(f"- Delivery decisions mapped: {len(rows)}")
    print("- Production go-live authority: Claims Operations Owner")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Why this matters: the program converts role-boundary and RACI rules into repeatable checks, including complete charter fields, one Accountable role per decision, at least one Responsible role, and Claims Operations go-live authority.

### Verification checkpoint

- **Expected result:** The program reads `role_charter.json` and `raci_matrix.csv` and reports actionable ownership errors.
- **Acceptable variation:** Comments and formatting may differ; the same decision rules must be enforced.
- **Failure indicator:** The program allows duplicate accountability, missing responsibility, or FDE-owned customer go-live.
- **Corrective action:** Restore the complete source and matching filenames.

## Step 6 — Compile and Run the Lab

```bash
python3 -m py_compile run_lab.py
python3 run_lab.py
```

Expected output:

```text
LAB 02 PASSED
- Role: Forward Deployed Lead
- Owned outcomes: 3
- Delivery decisions mapped: 9
- Production go-live authority: Claims Operations Owner
```

### Verification checkpoint

- **Expected result:** Compilation succeeds and the program prints the five-line passing summary.
- **Acceptable variation:** Python may create an ignored `__pycache__` directory.
- **Failure indicator:** A syntax, file, JSON, CSV, charter, or RACI error appears.
- **Corrective action:** Repair the named code or artifact and rerun both commands.

## Step 7 — Commit Your Completed Project

```bash
printf '__pycache__/\n*.py[cod]\n.DS_Store\n' > .gitignore
git init -b main
git add .gitignore run_lab.py claims_assistant_brief.md role_charter.json raci_matrix.csv
git commit -m "Complete role charter and RACI lab"
git status --short
```

### Verification checkpoint

- **Expected result:** Git creates a commit and `git status --short` prints nothing.
- **Acceptable variation:** If `git init -b main` is unsupported, run `git init` followed by `git branch -M main`.
- **Failure indicator:** Caches, reference files, or unrelated content are staged.
- **Corrective action:** Remove transient files and stage only the code and artifacts created in this guide.
## Map the Completed Workflow

1. The engagement brief establishes outcomes and protected decision boundaries.
2. The role charter assigns delivery outcomes, decision rights, escalation evidence, and limits.
3. The RACI maps each decision to one Accountable role and at least one Responsible role.
4. Native JSON and CSV checks confirm the artifacts are structurally usable.
5. The duplicate-accountability exercise demonstrates why one `A` per decision matters.

## Troubleshooting Cheatsheet

| Symptom | Likely cause | Corrective action |
| --- | --- | --- |
| JSON line/column error | Invalid JSON punctuation | Repair the location reported by `json.tool` |
| Missing charter field | Required section is absent or empty | Add the named evidence-supported section |
| Invalid RACI row | Zero/multiple `A` values or no `R` | Assign exactly one `A` and at least one `R` |
| Wrong go-live owner | `claims_owner` is not `A` | Restore Claims Operations accountability |

## Cleanup

Keep `run_lab.py`, `claims_assistant_brief.md`, `role_charter.json`, `raci_matrix.csv`, `.gitignore`, and your Git history. No additional cleanup is required after the project passes and the working tree is clean.

## Completion Check

- [ ] I created the Python validator, engagement brief, charter, and RACI from this guide.
- [ ] `run_lab.py` compiles and the completed project reports `LAB 02 PASSED`.
- [ ] Every RACI row has exactly one `A` and at least one `R`.
- [ ] Claims Operations owns production go-live.
- [ ] Protected claim decisions remain with authorized humans.
- [ ] My own Git working tree is clean.

## Reflection

Which decision right most clearly prevents the Forward Deployed Lead from becoming an unbounded owner of customer business policy?
