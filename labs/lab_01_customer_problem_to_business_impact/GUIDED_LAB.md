# Lab 01 — Map a Customer Problem from Discovery to Business Impact

## Goal

Turn Northstar Mutual’s request for an AI claims assistant into a measurable Discover–Design–Build–Run–Impact map, then use pilot evidence to make a scale, repair, continue, or exit decision.

## What You'll Build or Produce

In your own project directory, you will create:

- `customer_scenario.json` — the supplied customer evidence, targets, and constraints.
- `lifecycle_map.json` — your completed problem-to-impact map.
- `pilot_results.json` — the supplied pilot evidence used for the deployment decision.
- `run_lab.py` — the learner-built validator and pilot decision program.

The completed course repository contains the finished version of these same four project files. Use it only when you are stuck or comparing your result.

## Estimated Time

35–50 minutes.

## Cost Guardrails

This lab runs locally and costs $0. It uses no cloud resources, credentials, model APIs, or third-party packages.

## Completion Evidence

You are finished when `run_lab.py` compiles, all three JSON files parse successfully, the lifecycle map preserves the customer’s baseline and guardrails, the pilot decision is `repair_and_retest`, and your own Git working tree is clean after committing.

## Prerequisites

- Python 3.10 or later for JSON syntax checks and small verification commands.
- Git, a terminal, and a text editor.
- Basic JSON familiarity.

## Where This Lab Fits

This is the foundation for the Enterprise AI Claims Assistant case study. You will turn a feature request into a verified customer problem, a decision boundary, measurable outcomes, and an evidence-based pilot decision. Later labs reuse this problem-to-impact logic instead of treating deployment as the finish line.

## Step 1 — Create Your Independent Project

Create a new directory. Do not build the exercise by editing the completed reference repository.

```bash
mkdir fde_lab_01
cd fde_lab_01
```

Why this matters: your directory should contain the project you build from this guide; the course repository is only the completed comparison point.

### Verification checkpoint

- **Expected result:** Your terminal is inside an empty `fde_lab_01` directory.
- **Acceptable variation:** You may choose another directory name.
- **Failure indicator:** You are inside the completed `lab_01_customer_problem_to_business_impact` repository.
- **Corrective action:** Leave the reference repository and create a separate working directory.

## Step 2 — Record the Customer Evidence

Create `customer_scenario.json` with the supplied discovery evidence:

```json
{
  "organization": "Northstar Mutual",
  "weekly_eligible_claims": 1200,
  "claims_adjusters": 48,
  "current_workflow": [
    "Open a new property claim",
    "Review the claim form",
    "Locate the applicable policy and endorsements",
    "Review photographs and prior notes",
    "Decide whether to fast-track or manually review the claim",
    "Record the rationale and route the claim"
  ],
  "observations": {
    "average_handling_time_minutes": 18,
    "incorrect_fast_track_rate": 0.012,
    "claims_completed_within_24_hours": 0.82,
    "primary_friction": "Evidence is distributed across multiple systems"
  },
  "business_request": "Build an AI claims assistant",
  "targets": {
    "average_handling_time_minutes": 11,
    "maximum_incorrect_fast_track_rate": 0.015,
    "measurement_window": "30 days after pilot launch",
    "minimum_pilot_sample_size": 200
  },
  "constraints": [
    "The adjuster retains the final routing decision",
    "The system cannot deny claims autonomously",
    "The system cannot issue payments",
    "Customer information must remain inside the approved environment",
    "Recommendations must cite supporting policy evidence",
    "Missing or conflicting evidence must trigger manual review"
  ]
}
```

Why this matters: the requested feature is not the problem definition. This file preserves the verified workflow, baseline, target, quality guardrail, and prohibited actions.

### Verification checkpoint

- **Expected result:** The file identifies the 18-minute baseline, 11-minute target, 1.5% maximum incorrect fast-track rate, and adjuster authority.
- **Acceptable variation:** Formatting and indentation may differ; the evidence values must not.
- **Failure indicator:** The file describes only “build an AI claims assistant” or removes a protected boundary.
- **Corrective action:** Restore the scenario evidence exactly before designing the lifecycle map.

## Step 3 — Build the Lifecycle Map

Create `lifecycle_map.json`:

```json
{
  "schema_version": "1.0",
  "customer_context": {
    "organization": "Northstar Mutual",
    "user": "Claims adjuster",
    "business_owner": "VP of Claims Operations",
    "current_workflow": "Adjusters manually inspect claim forms, policies, endorsements, photographs, and prior notes across multiple systems.",
    "problem_statement": "Eligible property claims take an average of 18 minutes to assess because the evidence needed for routing decisions is distributed across multiple systems."
  },
  "decision": {
    "user_decision": "Decide whether an eligible claim can be fast-tracked or requires manual review.",
    "action_after_decision": "Route the claim to the appropriate queue and record the supporting rationale."
  },
  "scope": {
    "in_scope": [
      "Surface policy evidence relevant to the claim",
      "Recommend fast-track or manual review",
      "Record evidence supporting the recommendation",
      "Escalate missing or conflicting evidence to manual review"
    ],
    "out_of_scope": [
      "Deny claims autonomously",
      "Issue customer payments",
      "Change policy terms",
      "Remove the adjuster's final decision authority"
    ]
  },
  "baseline": {
    "metric": "average_handling_time_minutes",
    "current_value": 18,
    "target_value": 11,
    "unit": "minutes_per_claim",
    "direction": "decrease",
    "measurement_window": "30 days after pilot launch",
    "minimum_pilot_sample_size": 200,
    "weekly_volume": 1200
  },
  "lifecycle": {
    "discover": {
      "owner": "Forward Deployed Engineer and Claims Operations Lead",
      "deliverable": "Observed workflow, bounded problem statement, and measurement baseline",
      "evidence": "Twenty sampled claim journeys and confirmed handling-time data",
      "exit_criterion": "The user, decision, action, friction, scope, baseline, and business owner are confirmed."
    },
    "design": {
      "owner": "Forward Deployed Architect and Claims Operations Lead",
      "deliverable": "Bounded AI-assisted claims workflow with human decision points",
      "evidence": "Approved workflow showing recommendation, evidence citation, manual review, and prohibited actions",
      "exit_criterion": "The customer approves system boundaries, human authority, success criteria, and guardrails."
    },
    "build": {
      "owner": "AI Forward Deployed Engineer and Customer Integration Engineer",
      "deliverable": "Smallest valuable evidence-to-recommendation slice",
      "evidence": "Representative claims produce traceable recommendations without executing prohibited actions",
      "exit_criterion": "The end-to-end slice passes functional checks and routes missing evidence to manual review."
    },
    "run": {
      "owner": "Technical Deployment Lead and Claims Operations Manager",
      "deliverable": "Controlled pilot with selected claims adjusters",
      "evidence": "Usage, handling time, override, availability, and incorrect-routing telemetry",
      "exit_criterion": "At least 200 eligible claims produce sufficient operational and quality evidence."
    },
    "impact": {
      "owner": "VP of Claims Operations",
      "deliverable": "Scale, repair, pause, or exit recommendation",
      "evidence": "Pilot results compared with the handling-time target and incorrect-fast-track guardrail",
      "exit_criterion": "Leadership records an evidence-based deployment decision and accountable next action."
    }
  },
  "outcomes": {
    "technical_output": "A claims-assistant workflow is deployed to the controlled pilot environment.",
    "customer_outcome": "Adjusters receive relevant policy evidence and a traceable routing recommendation before making the final decision.",
    "business_impact": "Average handling time for eligible claims decreases from 18 minutes to 11 minutes.",
    "guardrail": {
      "metric": "incorrect_fast_track_rate",
      "maximum_value": 0.015,
      "unit": "ratio"
    }
  },
  "assumptions": [
    "The 1,200 weekly claims are eligible for the bounded workflow.",
    "The 18-minute baseline was measured consistently.",
    "Policy and endorsement evidence is available in approved systems."
  ],
  "trade_offs": [
    "Manual review protects claim quality but limits maximum automation.",
    "Evidence citation may increase latency but improves trust and auditability."
  ]
}
```

Why this matters: the map connects the customer problem to owned deliverables, exit criteria, and measurable impact instead of treating deployment as the finish line.

Review the five stages:

| Stage | Evidence question |
| --- | --- |
| Discover | Are the user, decision, friction, scope, baseline, and owner confirmed? |
| Design | Are human authority, success criteria, and guardrails explicit? |
| Build | Is the smallest valuable end-to-end slice defined? |
| Run | Is the pilot bounded and instrumented? |
| Impact | Is the scale, repair, pause, or exit decision evidence-based? |

### Verification checkpoint

- **Expected result:** Every stage has an owner, deliverable, evidence, and exit criterion; technical output, customer outcome, and business impact are distinct.
- **Acceptable variation:** You may improve wording while preserving the same evidence and authority boundaries.
- **Failure indicator:** A stage has no owner or exit criterion, or business impact is stated only as “deploy the assistant.”
- **Corrective action:** Tie each stage to a decision, accountable owner, observable evidence, and measurable exit.

## Step 4 — Add the Pilot Evidence

Create `pilot_results.json`:

```json
{
  "pilot_name": "Northstar Claims Assistant - Pilot 1",
  "sample_size": 320,
  "average_handling_time_minutes": 12.5,
  "incorrect_fast_track_rate": 0.024,
  "recommendation_acceptance_rate": 0.68,
  "availability": 0.994,
  "most_common_failure": "Missing policy endorsements caused unsupported fast-track recommendations",
  "affected_claims": 14
}
```

Why this matters: a lifecycle map becomes operational only when the team can compare observed pilot evidence with the target and guardrail.

### Verification checkpoint

- **Expected result:** The pilot contains 320 claims, 12.5-minute handling time, and a 2.4% incorrect fast-track rate.
- **Acceptable variation:** None for supplied evidence; do not improve pilot results to make the decision easier.
- **Failure indicator:** The pilot data is missing, speculative, or changed to meet the target.
- **Corrective action:** Restore the supplied measurements.

## Step 5 — Build the Python Validator

Create `run_lab.py` with this complete source:

```python
#!/usr/bin/env python3
"""Run Lab 01: validate the customer-to-impact map and evaluate pilot evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
STAGES = ("discover", "design", "build", "run", "impact")


def load_json(name: str) -> dict[str, Any]:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def validate(data: dict[str, Any], scenario: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = ("customer_context", "decision", "scope", "baseline", "lifecycle", "outcomes")
    for field in required:
        if field not in data:
            errors.append(f"Missing section: {field}")

    lifecycle = data.get("lifecycle", {})
    for stage in STAGES:
        details = lifecycle.get(stage, {})
        for field in ("owner", "deliverable", "evidence", "exit_criterion"):
            if not details.get(field):
                errors.append(f"{stage}.{field} is required")

    baseline = data.get("baseline", {})
    current = baseline.get("current_value")
    target = baseline.get("target_value")
    if baseline.get("direction") == "decrease" and isinstance(current, (int, float)) and isinstance(target, (int, float)):
        if target >= current:
            errors.append("Target must be lower than the current value")
    expected_target = scenario.get("targets", {}).get("average_handling_time_minutes")
    if target != expected_target:
        errors.append(f"Target must match the customer evidence: {expected_target}")

    boundaries = " ".join(data.get("scope", {}).get("out_of_scope", [])).lower()
    if "deny claims" not in boundaries or "payments" not in boundaries:
        errors.append("Scope must prohibit autonomous denial and payment")

    outcomes = data.get("outcomes", {})
    values = [outcomes.get(key, "") for key in ("technical_output", "customer_outcome", "business_impact")]
    if not all(values) or len({value.lower() for value in values}) != 3:
        errors.append("Technical output, customer outcome, and business impact must be distinct")
    return errors


def evaluate(data: dict[str, Any], pilot: dict[str, Any]) -> tuple[str, list[str]]:
    baseline = data["baseline"]
    guardrail = data["outcomes"]["guardrail"]
    reasons: list[str] = []
    if pilot["sample_size"] < baseline["minimum_pilot_sample_size"]:
        reasons.append("Pilot sample is too small")
        return "continue_pilot", reasons
    if pilot["average_handling_time_minutes"] > baseline["target_value"]:
        reasons.append("Handling-time target was not met")
    if pilot["incorrect_fast_track_rate"] > guardrail["maximum_value"]:
        reasons.append("Incorrect fast-track guardrail was breached")
    return ("scale" if not reasons else "repair_and_retest"), reasons


def main() -> int:
    scenario = load_json("customer_scenario.json")
    lifecycle_map = load_json("lifecycle_map.json")
    pilot = load_json("pilot_results.json")
    errors = validate(lifecycle_map, scenario)
    if errors:
        print(f"LAB 01 FAILED — {len(errors)} issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    decision, reasons = evaluate(lifecycle_map, pilot)
    print("LAB 01 PASSED")
    print(f"- Customer problem: {lifecycle_map['customer_context']['problem_statement']}")
    print(f"- Lifecycle stages: {', '.join(STAGES)}")
    print(f"- Target: {lifecycle_map['baseline']['current_value']} -> {lifecycle_map['baseline']['target_value']} minutes")
    print(f"- Pilot decision: {decision}")
    for reason in reasons:
        print(f"  - {reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Why this matters: the program turns the lifecycle and pilot rules into repeatable evidence. It validates the map, protects the target and scope boundaries, and calculates the deployment decision.

### Verification checkpoint

- **Expected result:** `run_lab.py` loads the three JSON files, validates all five stages, and evaluates the pilot.
- **Acceptable variation:** Comments and formatting may differ; validation behavior and output evidence must remain equivalent.
- **Failure indicator:** The program does not check the target, protected actions, lifecycle completeness, or pilot guardrail.
- **Corrective action:** Restore the complete source and confirm every referenced JSON filename matches your project.

## Step 6 — Compile and Run the Lab

```bash
python3 -m py_compile run_lab.py
python3 run_lab.py
```

Expected output begins with:

```text
LAB 01 PASSED
```

It must report five lifecycle stages, the 18-to-11-minute target, and `repair_and_retest`.

### Verification checkpoint

- **Expected result:** Compilation succeeds and the program reports `LAB 01 PASSED` with `repair_and_retest`.
- **Acceptable variation:** Python may create an ignored `__pycache__` directory.
- **Failure indicator:** A syntax error, missing-file error, JSON error, or `LAB 01 FAILED` message appears.
- **Corrective action:** Repair the named code or data file and rerun both commands.

## Step 7 — Commit Your Completed Project

```bash
printf '__pycache__/\n*.py[cod]\n.DS_Store\n' > .gitignore
git init -b main
git add .gitignore run_lab.py customer_scenario.json lifecycle_map.json pilot_results.json
git commit -m "Complete customer problem-to-impact lab"
git status --short
```

### Verification checkpoint

- **Expected result:** Git creates a commit and `git status --short` prints nothing.
- **Acceptable variation:** If `git init -b main` is unsupported, run `git init` followed by `git branch -M main`.
- **Failure indicator:** Caches, course-reference files, or unrelated files are staged.
- **Corrective action:** Remove transient files and stage only the code and data files created in this guide.
## Map the Completed Workflow

1. Customer evidence establishes the real workflow, baseline, target, constraints, and owner.
2. The lifecycle map converts that evidence into owned Discover–Design–Build–Run–Impact gates.
3. Pilot results are compared with both the business target and quality guardrail.
4. Leadership chooses `repair_and_retest` because the pilot does not yet satisfy both.

## Troubleshooting Cheatsheet

| Symptom | Likely cause | Corrective action |
| --- | --- | --- |
| JSON line/column error | Missing comma, quote, brace, or bracket | Repair the location reported by `json.tool` |
| Target assertion fails in the completed state | Baseline or target differs from supplied evidence | Restore 18 as current and 11 as target |
| Decision prints `scale` | Pilot or guardrail values were changed | Restore the supplied pilot evidence and 1.5% guardrail |

## Cleanup

Keep `run_lab.py`, `customer_scenario.json`, `lifecycle_map.json`, `pilot_results.json`, `.gitignore`, and your Git history. No additional cleanup is required after the project passes and the working tree is clean.

## Completion Check

- [ ] I created the Python validator and three JSON files from this guide.
- [ ] `run_lab.py` compiles and the completed project reports `LAB 01 PASSED`.
- [ ] The map connects the problem to five owned lifecycle stages.
- [ ] The adjuster retains final authority and prohibited actions remain excluded.
- [ ] The pilot decision is `repair_and_retest`.
- [ ] My own Git working tree is clean.

## Reflection

Why would scaling a faster pilot still be irresponsible when the incorrect fast-track rate exceeds the agreed guardrail?
