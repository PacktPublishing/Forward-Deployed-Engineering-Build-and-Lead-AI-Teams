# Lab 07 — Build an Integrated Deployment Plan and Risk Register

## Goal

Build an integrated delivery plan for Northstar Mutual's Enterprise AI Claims Assistant that connects scope, workstreams, milestones, dependencies, decision rights, cutover, hypercare, operational handoff, and an owned risk register. Then run an executable review that fails closed when the plan or risk evidence is incomplete.

Create this lab in your own new project directory. Use the completed reference repository only for comparison when you are stuck; do not edit it to perform the exercise.

## What You'll Build or Produce

- `deployment_plan.json` — the integrated workstream, milestone, governance, cutover, hypercare, and handoff plan.
- `risk_register.csv` — an eight-risk register with scoring, owners, triggers, responses, contingencies, and status.
- `delivery_review.py` — the executable plan and risk review.
- `deployment_review.md` — the generated delivery-readiness record.
- `.gitignore` — Git hygiene for the Python workflow.

## Estimated Time

75–100 minutes.

## Cost Guardrails

This lab uses local JSON, CSV, and Python standard-library code only. It creates no cloud resources, makes no network calls, and requires no paid services.

## Completion Evidence

- `python3 -m py_compile delivery_review.py` succeeds.
- `python3 delivery_review.py` prints `LAB 07 PASSED` and `PLAN_READY_FOR_EXECUTION`.
- Seven milestones have dependencies, DRIs, dates, and exit evidence.
- Six workstreams connect customer and internal owners to the delivery path.
- Eight risks have valid probability × impact scores and actionable contingencies.
- Cutover, rollback, hypercare, decision rights, and handoff acceptance are explicit.
- `deployment_review.md` is generated and reviewed.
- Your Git repository is clean on `main`.

## Prerequisites

- Python 3.10 or later
- Git
- A text editor
- Familiarity with delivery milestones, RACI/DRI concepts, risk scoring, and production cutover
- The approved case boundary from earlier labs: a 25-adjuster, 500-claim, 14-day feature-flagged pilot with human control over protected actions.

## Where This Lab Fits

This lab begins the customer-delivery stage after production readiness. You will connect the approved technical release to customer actions, milestones, dependencies, decision rights, risk responses, cutover, hypercare, and operational handoff. The output is the execution plan that produces the pilot evidence analyzed in Lab 08.

## Step 1 — Create Your Project

Create and enter a new directory:

```bash
mkdir lab_07_integrated_deployment_plan_risk_register
cd lab_07_integrated_deployment_plan_risk_register
```

Create `.gitignore`:

```gitignore
__pycache__/
*.py[cod]
.DS_Store
```

Why this matters: the learner project and completed reference must have the same small, runnable shape.

### Verification checkpoint

- **Expected result:** Your directory contains only `.gitignore`.
- **Acceptable variation:** You may use another directory name.
- **Failure indicator:** You are editing Lab 06 or the completed Lab 07 reference repository.
- **Corrective action:** Create a separate learner-owned directory and continue there.

## Step 2 — Build the Integrated Deployment Plan

Create `deployment_plan.json`:

```json
{
  "metadata": {
    "lab_id": "lab_07",
    "customer": "Northstar Mutual",
    "initiative": "Enterprise AI Claims Assistant",
    "plan_stage": "bounded pilot delivery",
    "prepared_date": "2026-08-16",
    "target_go_live": "2026-09-21"
  },
  "scope": {
    "objective": "Deliver a controlled claims-assistant pilot to 25 licensed adjusters with measurable exit evidence and an operational handoff.",
    "in_scope": [
      "Policy retrieval and cited claim summaries",
      "Allowed recommendations: request_evidence continue_review or escalate",
      "Human-approved claims-system action path",
      "Pilot observability support training and rollback"
    ],
    "out_of_scope": [
      "Autonomous claim approval or denial",
      "Autonomous payments reserve changes or customer communication",
      "Enterprise-wide rollout beyond the approved pilot cohort"
    ]
  },
  "workstreams": [
    {
      "id": "W-01",
      "name": "Solution and integration",
      "owner": "FDE Lead",
      "milestone_ids": [
        "M-01",
        "M-03",
        "M-05"
      ]
    },
    {
      "id": "W-02",
      "name": "Data and policy readiness",
      "owner": "Claims Data Lead",
      "milestone_ids": [
        "M-01",
        "M-02"
      ]
    },
    {
      "id": "W-03",
      "name": "Security and production controls",
      "owner": "Security Lead",
      "milestone_ids": [
        "M-02",
        "M-04"
      ]
    },
    {
      "id": "W-04",
      "name": "Evaluation and release evidence",
      "owner": "AI Quality Lead",
      "milestone_ids": [
        "M-03",
        "M-04"
      ]
    },
    {
      "id": "W-05",
      "name": "Adoption and change",
      "owner": "Claims Operations Lead",
      "milestone_ids": [
        "M-05",
        "M-06"
      ]
    },
    {
      "id": "W-06",
      "name": "Go-live and operational transition",
      "owner": "Technical Deployment Lead",
      "milestone_ids": [
        "M-06",
        "M-07"
      ]
    }
  ],
  "milestones": [
    {
      "id": "M-01",
      "name": "Scope and interfaces baselined",
      "target_date": "2026-08-21",
      "depends_on": [],
      "dri": "FDE Lead",
      "exit_evidence": [
        "Signed scope boundary",
        "Interface inventory",
        "Named customer and internal owners"
      ]
    },
    {
      "id": "M-02",
      "name": "Data and security controls approved",
      "target_date": "2026-08-28",
      "depends_on": [
        "M-01"
      ],
      "dri": "Security Lead",
      "exit_evidence": [
        "Approved data-flow review",
        "Tenant and role authorization tests",
        "Threat-model control evidence"
      ]
    },
    {
      "id": "M-03",
      "name": "End-to-end staging slice complete",
      "target_date": "2026-09-04",
      "depends_on": [
        "M-01",
        "M-02"
      ],
      "dri": "FDE Lead",
      "exit_evidence": [
        "Staging workflow demo",
        "Version manifest",
        "Integration failure-path evidence"
      ]
    },
    {
      "id": "M-04",
      "name": "Production-readiness gates passed",
      "target_date": "2026-09-10",
      "depends_on": [
        "M-03"
      ],
      "dri": "AI Quality Lead",
      "exit_evidence": [
        "Evaluation decision",
        "Production-readiness report",
        "Business technical security and operations approvals"
      ]
    },
    {
      "id": "M-05",
      "name": "Pilot users and operations prepared",
      "target_date": "2026-09-14",
      "depends_on": [
        "M-03"
      ],
      "dri": "Claims Operations Lead",
      "exit_evidence": [
        "Named 25-adjuster cohort",
        "Training completion",
        "Support and escalation roster"
      ]
    },
    {
      "id": "M-06",
      "name": "Cutover rehearsal accepted",
      "target_date": "2026-09-18",
      "depends_on": [
        "M-04",
        "M-05"
      ],
      "dri": "Technical Deployment Lead",
      "exit_evidence": [
        "Timed cutover rehearsal",
        "Rollback under 10 minutes",
        "Reconciled test actions"
      ]
    },
    {
      "id": "M-07",
      "name": "Go-live decision recorded",
      "target_date": "2026-09-21",
      "depends_on": [
        "M-06"
      ],
      "dri": "Executive Sponsor",
      "exit_evidence": [
        "Signed go-live record",
        "Feature flag and cohort confirmed",
        "Hypercare owners on duty"
      ]
    }
  ],
  "critical_path": [
    "M-01",
    "M-02",
    "M-03",
    "M-04",
    "M-06",
    "M-07"
  ],
  "decision_rights": [
    {
      "decision": "scope",
      "dri": "Technical Deployment Lead",
      "approver": "Business Owner",
      "consulted": [
        "FDE Lead",
        "Claims Operations Lead"
      ]
    },
    {
      "decision": "architecture",
      "dri": "FDE Lead",
      "approver": "Technical Owner",
      "consulted": [
        "Security Lead",
        "Claims Platform Lead"
      ]
    },
    {
      "decision": "security",
      "dri": "Security Lead",
      "approver": "Security Approver",
      "consulted": [
        "Data Protection Officer",
        "FDE Lead"
      ]
    },
    {
      "decision": "go_live",
      "dri": "Technical Deployment Lead",
      "approver": "Executive Sponsor",
      "consulted": [
        "Business Owner",
        "Technical Owner",
        "Security Approver",
        "Operations Owner"
      ]
    },
    {
      "decision": "incident",
      "dri": "Operations Owner",
      "approver": "Business Owner",
      "consulted": [
        "Security Lead",
        "Claims Platform Lead",
        "FDE Lead"
      ]
    }
  ],
  "delivery_cadence": [
    {
      "meeting": "Delivery review",
      "frequency": "twice weekly",
      "purpose": "Milestones dependencies blockers and customer actions",
      "owner": "Technical Deployment Lead"
    },
    {
      "meeting": "Technical review",
      "frequency": "weekly",
      "purpose": "Architecture evaluation security reliability and cost evidence",
      "owner": "FDE Lead"
    },
    {
      "meeting": "Executive checkpoint",
      "frequency": "weekly during cutover",
      "purpose": "Scope risk decisions and go-live recommendation",
      "owner": "Executive Sponsor"
    }
  ],
  "cutover": {
    "change_window": "2026-09-21 07:00-09:00 CT",
    "steps": [
      "Confirm signed release record and on-call roster",
      "Enable claims_ai_assist_pilot for the named cohort",
      "Run synthetic smoke claim and verify audit evidence",
      "Release the cohort and monitor first ten assisted claims"
    ],
    "abort_conditions": [
      "Any unauthorized protected action",
      "Cross-tenant or approved-boundary data exposure",
      "Missing audit evidence",
      "Smoke claim fails a blocking control"
    ],
    "rollback_action": "Disable the feature flag preserve evidence reconcile uncertain writes and continue the manual workflow."
  },
  "hypercare": {
    "duration_days": 14,
    "coverage": "Business-hours command center with 24x7 severity-one escalation",
    "daily_review": [
      "Adoption and assisted-claim volume",
      "Quality safety latency cost and incident metrics",
      "Open support cases and rollback triggers"
    ],
    "exit_criteria": [
      "No open severity-one or severity-two incident",
      "All uncertain writes reconciled",
      "SLOs met for five consecutive business days",
      "Operations accepts runbook dashboard and support ownership"
    ]
  },
  "handoff": {
    "receiving_owner": "Claims AI Operations",
    "deliverables": [
      "Architecture and version manifest",
      "Runbook dashboard alerts and audit queries",
      "Known issues risk register and accepted exceptions",
      "Support model training record and escalation tree"
    ],
    "acceptance_criteria": [
      "Receiving owner completes an observed operating shift",
      "Rollback and reconciliation drills pass",
      "Artifact links and accountable owners are current"
    ],
    "engagement_exit_rule": "FDE remains escalation support only after written operational acceptance."
  }
}
```

Why this matters: delivery leadership connects technical work to customer actions, evidence-based exit criteria, accountable decisions, and an accepted operating model. A list of engineering tasks alone is not an integrated deployment plan.

### Verification checkpoint

- **Expected result:** The plan contains 6 workstreams, 7 milestones, a critical path, five decision domains, delivery cadences, cutover, hypercare, and operational handoff.
- **Acceptable variation:** Dates and owner titles may reflect another organization if every dependency and decision remains owned.
- **Failure indicator:** Milestones lack exit evidence, customer actions are absent, or go-live and incident decisions have no approver.
- **Corrective action:** Add the missing DRI, dependency, accountable decision, or measurable evidence before continuing.

## Step 3 — Create the Risk Register

Create `risk_register.csv`:

```csv
risk_id,category,description,probability,impact,score,owner,response,trigger,contingency,status
R-01,dependency,Claims-system write API misses the cutover window,4,5,20,Claims Platform Lead,MITIGATE,API certification slips beyond M-03,Launch read-only assistance and defer protected writes,MITIGATED
R-02,security,Cross-tenant authorization defect appears in staging,4,4,16,Security Lead,MITIGATE,Any negative authorization test succeeds,Hold promotion and repair tenant enforcement,MITIGATED
R-03,data,Policy metadata is incomplete for a pilot jurisdiction,3,5,15,Claims Data Lead,MITIGATE,Coverage falls below 100 percent for pilot policies,Remove affected jurisdiction from cohort and repair metadata,MONITORED
R-04,adoption,Adjuster training completion falls below 90 percent,3,4,12,Claims Operations Lead,MITIGATE,Completion below target three days before cutover,Reduce cohort to trained adjusters and add office hours,MONITORED
R-05,reliability,p95 latency exceeds 12 seconds in staging load test,3,4,12,Site Reliability Lead,MITIGATE,Two consecutive windows exceed the SLO,Tune retrieval limit concurrency and timeouts,MITIGATED
R-06,scope,Executive sponsor requests enterprise rollout before pilot evidence,3,4,12,Technical Deployment Lead,AVOID,Request exceeds cohort volume or duration boundary,Require a new scope decision and release review,MONITORED
R-07,operations,On-call coverage is incomplete for the first weekend,2,5,10,Operations Owner,MITIGATE,Any severity-one slot lacks primary and backup,Delay go-live or add approved coverage,MITIGATED
R-08,vendor,Managed model endpoint has a regional service disruption,2,4,8,AI Platform Lead,TRANSFER,Provider health alert or circuit breaker opens,Disable AI assistance and continue manual claims handling,MONITORED
```

Score each risk as probability × impact on a 1–5 scale. Treat scores of 15 or higher as blocking unless the risk is actively mitigated or monitored with a trigger and contingency.

### Verification checkpoint

- **Expected result:** Eight unique risks cover dependency, security, data, adoption, reliability, scope, operations, and vendor exposure.
- **Acceptable variation:** You may add risks, but keep the exact schema and do not delete uncomfortable risks to improve the summary.
- **Failure indicator:** A high risk is open, unowned, missing a trigger, or has a score that does not equal probability × impact.
- **Corrective action:** Assign an owner, choose a valid response, define an observable trigger and contingency, and correct the score.

## Step 4 — Create the Executable Delivery Review

Create `delivery_review.py`:

```python
#!/usr/bin/env python3
"""Validate an integrated deployment plan and generate its delivery review."""

from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
PLAN_FILE = ROOT / "deployment_plan.json"
RISK_FILE = ROOT / "risk_register.csv"
REPORT_FILE = ROOT / "deployment_review.md"


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot load {path.name}: {exc}") from exc


def load_risks(path: Path) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))
    except OSError as exc:
        raise ValueError(f"Cannot load {path.name}: {exc}") from exc


def validate(plan: dict[str, Any], risks: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    required_sections = {
        "metadata", "scope", "workstreams", "milestones", "critical_path",
        "decision_rights", "delivery_cadence", "cutover", "hypercare", "handoff",
    }
    missing = required_sections - set(plan)
    if missing:
        errors.append("Missing plan sections: " + ", ".join(sorted(missing)))

    milestones = plan.get("milestones", [])
    milestone_ids = [item.get("id") for item in milestones]
    if not milestone_ids or len(milestone_ids) != len(set(milestone_ids)):
        errors.append("Milestone IDs must be present and unique")
    milestone_index = {item["id"]: item for item in milestones if item.get("id")}
    positions = {milestone_id: index for index, milestone_id in enumerate(milestone_ids)}
    for milestone in milestones:
        try:
            date.fromisoformat(milestone["target_date"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"{milestone.get('id')} has an invalid target date")
        if not milestone.get("dri") or not milestone.get("exit_evidence"):
            errors.append(f"{milestone.get('id')} needs a DRI and exit evidence")
        for dependency in milestone.get("depends_on", []):
            if dependency not in milestone_index:
                errors.append(f"{milestone.get('id')} references unknown dependency {dependency}")
            elif positions[dependency] >= positions[milestone["id"]]:
                errors.append(f"{milestone['id']} dependency {dependency} is not earlier")

    workstreams = plan.get("workstreams", [])
    for workstream in workstreams:
        if not workstream.get("owner"):
            errors.append(f"{workstream.get('id')} has no owner")
        unknown = set(workstream.get("milestone_ids", [])) - set(milestone_ids)
        if unknown:
            errors.append(f"{workstream.get('id')} references unknown milestones")

    critical_path = plan.get("critical_path", [])
    if not critical_path or set(critical_path) - set(milestone_ids):
        errors.append("Critical path must use known milestones")

    required_decisions = {"scope", "architecture", "security", "go_live", "incident"}
    decisions = {item.get("decision") for item in plan.get("decision_rights", [])}
    if decisions != required_decisions:
        errors.append("Decision rights must cover scope architecture security go_live and incident")

    cutover = plan.get("cutover", {})
    if not cutover.get("steps") or not cutover.get("abort_conditions") or not cutover.get("rollback_action"):
        errors.append("Cutover requires steps abort conditions and rollback")
    handoff = plan.get("handoff", {})
    if not handoff.get("receiving_owner") or not handoff.get("acceptance_criteria"):
        errors.append("Handoff requires a receiving owner and acceptance criteria")

    required_risk_fields = {
        "risk_id", "category", "description", "probability", "impact", "score",
        "owner", "response", "trigger", "contingency", "status",
    }
    if risks and set(risks[0]) != required_risk_fields:
        errors.append("Risk-register columns do not match the required schema")
    risk_ids = [item.get("risk_id") for item in risks]
    if not risk_ids or len(risk_ids) != len(set(risk_ids)):
        errors.append("Risk IDs must be present and unique")
    for risk in risks:
        try:
            probability = int(risk["probability"])
            impact = int(risk["impact"])
            score = int(risk["score"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"{risk.get('risk_id')} has invalid numeric scoring")
            continue
        if probability not in range(1, 6) or impact not in range(1, 6):
            errors.append(f"{risk['risk_id']} probability and impact must be 1 through 5")
        if score != probability * impact:
            errors.append(f"{risk['risk_id']} score does not equal probability times impact")
        if not risk.get("owner") or not risk.get("trigger") or not risk.get("contingency"):
            errors.append(f"{risk['risk_id']} lacks ownership trigger or contingency")
        if risk.get("response") not in {"AVOID", "MITIGATE", "TRANSFER", "ACCEPT"}:
            errors.append(f"{risk['risk_id']} has an invalid response")
        if score >= 15 and risk.get("status") == "OPEN":
            errors.append(f"{risk['risk_id']} is an unresolved blocking risk")
    if errors:
        raise ValueError("\n".join(f"- {error}" for error in errors))
    return [risk["risk_id"] for risk in risks if int(risk["score"]) >= 15 and risk["status"] == "OPEN"]


def build_report(plan: dict[str, Any], risks: list[dict[str, str]], decision: str) -> str:
    lines = [
        "# Enterprise AI Claims Assistant — Integrated Deployment Review", "",
        f"- **Decision:** {decision}",
        f"- **Target go-live:** {plan['metadata']['target_go_live']}",
        f"- **Objective:** {plan['scope']['objective']}", "",
        "## Workstreams", "",
        "| Workstream | Owner | Milestones |", "| --- | --- | --- |",
    ]
    for item in plan["workstreams"]:
        lines.append(f"| {item['name']} | {item['owner']} | {', '.join(item['milestone_ids'])} |")
    lines.extend(["", "## Milestones", "", "| ID | Milestone | Target | DRI | Dependencies |", "| --- | --- | --- | --- | --- |"])
    for item in plan["milestones"]:
        dependencies = ", ".join(item["depends_on"]) or "None"
        lines.append(f"| {item['id']} | {item['name']} | {item['target_date']} | {item['dri']} | {dependencies} |")
    lines.extend(["", "## Critical Path", "", " → ".join(plan["critical_path"]), "", "## Risk Register", "", "| Risk | Score | Owner | Response | Status | Contingency |", "| --- | ---: | --- | --- | --- | --- |"])
    for risk in sorted(risks, key=lambda item: int(item["score"]), reverse=True):
        lines.append(f"| {risk['risk_id']} | {risk['score']} | {risk['owner']} | {risk['response']} | {risk['status']} | {risk['contingency']} |")
    lines.extend(["", "## Cutover and Rollback", ""])
    lines.extend(f"{index}. {step}" for index, step in enumerate(plan["cutover"]["steps"], start=1))
    lines.extend(["", "**Abort conditions:**", ""])
    lines.extend(f"- {item}" for item in plan["cutover"]["abort_conditions"])
    lines.extend(["", f"**Rollback:** {plan['cutover']['rollback_action']}", "", "## Handoff", "", f"- Receiving owner: {plan['handoff']['receiving_owner']}"])
    lines.extend(f"- Acceptance: {item}" for item in plan["handoff"]["acceptance_criteria"])
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    try:
        plan = load_json(PLAN_FILE)
        risks = load_risks(RISK_FILE)
        blocking = validate(plan, risks)
        decision = "PLAN_READY_FOR_EXECUTION" if not blocking else "HOLD_FOR_REMEDIATION"
        REPORT_FILE.write_text(build_report(plan, risks, decision), encoding="utf-8")
    except (KeyError, TypeError, ValueError) as exc:
        print(f"LAB 07 FAILED\n{exc}")
        return 1

    print("LAB 07 PASSED")
    print(f"- Decision: {decision}")
    print(f"- Milestones: {len(plan['milestones'])}")
    print(f"- Workstreams: {len(plan['workstreams'])}")
    print(f"- Risks: {len(risks)}")
    print(f"- Unresolved blocking risks: {len(blocking)}")
    print(f"- Report: {REPORT_FILE.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

The program validates plan structure, milestone ordering, workstream references, decision rights, cutover and handoff completeness, risk schema, scoring, ownership, and unresolved blocking risk. It then generates the review record from the evidence.

### Verification checkpoint

- **Expected result:** `delivery_review.py` reads both learner-created inputs and produces `deployment_review.md`.
- **Acceptable variation:** You may split the code into taught learner-built modules.
- **Failure indicator:** The script ignores unknown milestone references or approves an open risk scored 15 or higher.
- **Corrective action:** Restore fail-closed reference validation and blocking-risk logic.

## Step 5 — Run and Inspect the Plan

Compile and execute:

```bash
python3 -m py_compile delivery_review.py
python3 delivery_review.py
```

Expected output:

```text
LAB 07 PASSED
- Decision: PLAN_READY_FOR_EXECUTION
- Milestones: 7
- Workstreams: 6
- Risks: 8
- Unresolved blocking risks: 0
- Report: deployment_review.md
```

Inspect the generated record:

```bash
sed -n '1,260p' deployment_review.md
```

On Windows PowerShell:

```powershell
Get-Content deployment_review.md
```

### Verification checkpoint

- **Expected result:** The command exits successfully and the report shows the critical path, risk ranking, cutover controls, rollback, and handoff owner.
- **Acceptable variation:** A real engagement may correctly return a hold after you add blocking conditions.
- **Failure indicator:** The script prints `LAB 07 FAILED`, the report is stale, or a critical dependency is absent.
- **Corrective action:** Repair the exact named plan or risk evidence and rerun both commands.

## Step 6 — Conduct the Delivery Review

Use the generated report to answer:

1. Which customer-owned dependency can move the critical path?
2. Which risk requires a scope reduction rather than schedule pressure?
3. Who can approve go-live, and who can abort it?
4. What evidence proves operations can own the system after hypercare?
5. Can the manual workflow continue during rollback?

### Verification checkpoint

- **Expected result:** Each answer cites a milestone, risk, decision right, or acceptance criterion.
- **Acceptable variation:** You may recommend a narrower pilot when evidence supports it.
- **Failure indicator:** The review depends on informal ownership or unrecorded promises.
- **Corrective action:** Put the decision, owner, evidence, and trigger into the plan or risk register.

## Step 7 — Commit Your Evidence

```bash
git init -b main
git add .gitignore deployment_plan.json risk_register.csv delivery_review.py deployment_review.md
git commit -m "Complete integrated deployment plan and risk register"
git status --short --branch
```

### Verification checkpoint

- **Expected result:** Git reports `main` with no uncommitted changes.
- **Acceptable variation:** Another clear commit message is acceptable.
- **Failure indicator:** The generated report is missing or caches are tracked.
- **Corrective action:** Rerun the review, confirm `.gitignore`, stage the five project files, and commit.

## Map the Completed Workflow

1. Bound the pilot scope and protected actions.
2. Organize customer and internal work into owned workstreams.
3. Sequence milestones using dependencies and evidence-based exits.
4. Identify the critical path and decision rights.
5. Score delivery risks and define observable triggers and contingencies.
6. Rehearse cutover, rollback, hypercare, and handoff.
7. Generate an auditable execution-readiness record.

## Troubleshooting Cheatsheet

| Symptom | Likely cause | Corrective action |
| --- | --- | --- |
| Cannot load a file | Wrong directory or malformed JSON/CSV | Run from the project root and repair the named file |
| Unknown dependency | A milestone references a missing or later milestone | Correct the ID or sequence |
| Decision-right failure | A required decision lacks DRI or approver coverage | Add scope architecture security go-live and incident rights |
| Invalid score | Score differs from probability × impact | Recalculate using integers 1 through 5 |
| Blocking risk | A score of 15+ remains OPEN | Mitigate monitor narrow scope or hold execution |
| Stale report | Inputs changed after the last run | Run `python3 delivery_review.py` again |

## Cleanup

This lab creates no external resources. Remove only Python caches:

```bash
python3 -c "import shutil; shutil.rmtree('__pycache__', ignore_errors=True)"
```

Keep the four learner-built artifacts, `.gitignore`, and Git history as portfolio evidence.

## Completion Check

- [ ] I bounded the pilot scope and protected actions.
- [ ] I created six owned workstreams.
- [ ] I sequenced seven milestones with exit evidence.
- [ ] I identified the critical path and five decision domains.
- [ ] I scored and assigned all eight risks.
- [ ] I defined cutover abort and rollback conditions.
- [ ] I defined hypercare and operational handoff acceptance.
- [ ] I generated and reviewed `deployment_review.md`.
- [ ] I committed the project on a clean `main` branch.

## Reflection

1. Which risk would you escalate with options rather than merely report?
2. What evidence would justify moving the target go-live date?
3. Which handoff criterion best prevents permanent customer dependency?
