# Capstone Workshop 5 — Decide Reusability and Measure Business Outcomes

## Goal

Complete the Enterprise AI Claims Assistant capstone by classifying reusable capabilities, defining the adoption and business-outcome scorecard, integrating all five workshop artifacts, and producing an evidence-based executive rollout decision.

Continue in the learner-owned project from Workshops 1–4. The completed repository is a reference, not your workspace.

## What You'll Build or Produce

- `reuse_scorecard.json` — reuse decisions, ownership boundaries, baselines, targets, cadence, and decision policy.
- `pilot_results.csv` — four weeks of adoption, outcome, quality, safety, latency, cost, and audit evidence.
- `capstone_review.py` — the executable integration and decision review.
- `executive_deployment_decision.md` — the generated steering-committee decision memo.
- `README.md` — the shared project handoff.
- The final Workshop 5 Git commit.

## Estimated Time

80–110 minutes.

## Cost Guardrails

This workshop uses Python's standard library and local files only. It creates no external services or cost.

## Completion Evidence

- `python3 -m json.tool reuse_scorecard.json` succeeds.
- Six capabilities have product, platform, configuration, or custom-extension decisions, owners, and boundaries.
- The scorecard contains 11 adoption, outcome, quality, safety, value, latency, and audit gates.
- `python3 -m py_compile capstone_review.py` succeeds.
- `python3 capstone_review.py` prints `LAB 11 PASSED` and `APPROVE_PHASED_PRODUCTION_ROLLOUT`.
- The review connects 10/10 capstone decisions and generates the executive memo.
- Git is clean on `main`.

## Prerequisites

- Completed Workshops 1–4 in the same project directory
- Python 3.10 or later
- Familiarity with productization, adoption, ROI, rollout decisions, and executive communication

## Where This Workshop Fits

This workshop combines **Identify Reusable Product Capabilities** and **Create the Adoption and Business-Outcome Scorecard**. It completes the shared project and provides the evidence used in the separate executive role-play and final-rubric lectures.

## Step 1 — Create the Reuse and Scorecard Artifact

Create `reuse_scorecard.json`:

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
  "reusable_capabilities": [
    {
      "capability": "Prompt-injection evaluation pack",
      "decision": "PRODUCT",
      "owner": "AI Quality Product Owner",
      "boundary": "Versioned test contract with deployment-specific fixtures"
    },
    {
      "capability": "Effective-policy retrieval pattern",
      "decision": "PRODUCT",
      "owner": "Knowledge Platform Product Owner",
      "boundary": "Shared retrieval contract with configured jurisdiction and source connectors"
    },
    {
      "capability": "Protected-action audit schema",
      "decision": "PRODUCT",
      "owner": "Security Product Owner",
      "boundary": "Shared identity, evidence, approval, action, and result schema"
    },
    {
      "capability": "Enterprise identity adapter framework",
      "decision": "PLATFORM",
      "owner": "Identity Platform Owner",
      "boundary": "Shared adapter interface with customer-specific identity configuration"
    },
    {
      "capability": "Tenant claim-field mapping",
      "decision": "CONFIGURATION",
      "owner": "Implementation Configuration Owner",
      "boundary": "Declarative mapping that cannot fork shared source"
    },
    {
      "capability": "Northstar legacy mainframe adapter",
      "decision": "CUSTOM_EXTENSION",
      "owner": "Northstar Integration Owner",
      "boundary": "Customer-funded isolated extension with review date 2027-03-31"
    }
  ],
  "adoption_and_outcome_scorecard": {
    "baselines": {
      "average_handling_minutes": 42,
      "rework_rate_percent": 14,
      "quality_score_percent": 86
    },
    "targets": [
      {
        "metric": "active_adoption_percent",
        "operator": "min",
        "threshold": 80,
        "owner": "Claims Operations Lead"
      },
      {
        "metric": "assisted_claim_rate_percent",
        "operator": "min",
        "threshold": 70,
        "owner": "Claims Operations Lead"
      },
      {
        "metric": "recommendation_acceptance_percent",
        "operator": "min",
        "threshold": 75,
        "owner": "Claims Quality Lead"
      },
      {
        "metric": "handling_time_reduction_percent",
        "operator": "min",
        "threshold": 25,
        "owner": "Business Owner"
      },
      {
        "metric": "rework_reduction_percent",
        "operator": "min",
        "threshold": 25,
        "owner": "Claims Quality Lead"
      },
      {
        "metric": "quality_score_percent",
        "operator": "min",
        "threshold": 92,
        "owner": "Claims Quality Lead"
      },
      {
        "metric": "citation_completeness_percent",
        "operator": "min",
        "threshold": 95,
        "owner": "Claims Quality Lead"
      },
      {
        "metric": "p95_latency_seconds",
        "operator": "max",
        "threshold": 12,
        "owner": "Site Reliability Lead"
      },
      {
        "metric": "benefit_cost_ratio",
        "operator": "min",
        "threshold": 3,
        "owner": "Finance Partner"
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
    "review_cadence": "Weekly during rollout with a formal day-30 continue, repair, pause, or expand decision"
  },
  "decision_policy": {
    "approve": "All scorecard gates pass, safety evidence passes, blocking readiness controls pass, approvals are complete, and no risk is OPEN.",
    "hold": "Safety passes but a value, adoption, readiness, approval, or delivery condition fails.",
    "pause": "Any unauthorized protected action, quality below the safety floor, cross-tenant exposure, or missing protected-action audit occurs."
  }
}
```

The reuse decisions distinguish stable shared contracts from customer-specific implementation. Product and platform capabilities need repeated demand and durable ownership. Configuration must avoid source forks. A custom extension must remain isolated, funded, and reviewable.

### Verification checkpoint

- **Expected result:** At least five capabilities have a supported decision, owner, and explicit reuse boundary.
- **Acceptable variation:** Add or remove capabilities when deployment evidence supports the portfolio decision.
- **Failure indicator:** “Reusable” means copying customer code into a shared repository without a contract or owner.
- **Corrective action:** Choose product, platform, configuration, custom extension, or retirement and state the supported boundary.

## Step 2 — Add the Pilot Evidence

Create `pilot_results.csv`:

```csv
week,eligible_adjusters,active_adjusters,eligible_claims,assisted_claims,recommendations_shown,recommendations_accepted,average_handling_minutes,rework_rate_percent,quality_score_percent,citation_completeness_percent,p95_latency_seconds,model_cost_usd,unauthorized_protected_actions,audit_completeness_percent
1,25,14,100,48,45,30,38,12.5,88.5,96.0,11.8,80,0,100
2,25,18,110,70,65,51,34,10.5,91.0,97.0,11.4,105,0,100
3,25,21,115,90,85,70,31,9.2,93.2,98.0,10.7,135,0,100
4,25,22,120,105,100,82,29,8.5,94.5,99.0,10.2,165,0,100
```

The latest week is evaluated against 11 gates. Adoption alone cannot approve scale. The evidence must also show workflow coverage, handling-time and rework improvement, quality, citation completeness, latency, benefit relative to cost, zero unauthorized protected actions, and complete audit records.

### Verification checkpoint

- **Expected result:** Weeks 1–4 are sequential and every row satisfies `accepted ≤ shown ≤ assisted ≤ eligible`.
- **Acceptable variation:** Different pilot values are acceptable when they are internally consistent and lead to an honest decision.
- **Failure indicator:** Safety, latency, audit, or cost data is missing because adoption looks strong.
- **Corrective action:** Restore the complete measurement contract before calculating a rollout decision.

## Step 3 — Build the Integrated Capstone Review

Create `capstone_review.py`:

```python
#!/usr/bin/env python3
"""Validate an integrated enterprise AI deployment and write its decision memo."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
PLAN_FILES = [
    ROOT / "problem_value.json",
    ROOT / "team_decisions.json",
    ROOT / "architecture_approval.json",
    ROOT / "readiness_deployment.json",
    ROOT / "reuse_scorecard.json",
]
RISK_FILE = ROOT / "risk_register.csv"
PILOT_FILE = ROOT / "pilot_results.csv"
REPORT_FILE = ROOT / "executive_deployment_decision.md"

CAPSTONE_SECTIONS = {
    "customer_problem",
    "discovery_and_value",
    "forward_deployed_team",
    "decision_rights",
    "architecture",
    "evaluation_and_human_approval",
    "security_and_readiness",
    "deployment_plan",
    "reusable_capabilities",
    "adoption_and_outcome_scorecard",
}


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot load {path.name}: {exc}") from exc


def load_csv(path: Path) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))
    except OSError as exc:
        raise ValueError(f"Cannot load {path.name}: {exc}") from exc


def load_plan(paths: list[Path]) -> dict[str, Any]:
    """Combine the five workshop artifacts into one coherent capstone plan."""
    documents = [load_json(path) for path in paths]
    metadata = documents[0].get("metadata") if documents else None
    if not metadata:
        raise ValueError("Workshop 1 must define capstone metadata")
    plan: dict[str, Any] = {"metadata": metadata}
    for path, document in zip(paths, documents):
        if document.get("metadata") != metadata:
            raise ValueError(f"{path.name} metadata does not match Workshop 1")
        for key, value in document.items():
            if key == "metadata":
                continue
            if key in plan:
                raise ValueError(f"Duplicate capstone section {key} in {path.name}")
            plan[key] = value
    return plan


def percent(numerator: float, denominator: float) -> float:
    return round(100 * numerator / denominator, 2) if denominator else 0.0


def target_passed(target: dict[str, Any], actual: float) -> bool:
    threshold = float(target["threshold"])
    if target["operator"] == "min":
        return actual >= threshold
    if target["operator"] == "max":
        return actual <= threshold
    raise ValueError(f"Unsupported operator for {target['metric']}: {target['operator']}")


def validate_plan(plan: dict[str, Any]) -> None:
    errors: list[str] = []
    missing = CAPSTONE_SECTIONS - set(plan)
    if missing:
        errors.append("Missing capstone sections: " + ", ".join(sorted(missing)))

    problem = plan.get("customer_problem", {})
    baseline = problem.get("baseline", {})
    if not problem.get("primary_user") or not problem.get("problem_statement"):
        errors.append("Customer problem needs a primary user and evidence-based statement")
    if set(baseline) != {
        "average_handling_minutes", "rework_rate_percent", "quality_score_percent"
    }:
        errors.append("Customer baseline must define time, rework, and quality")
    if not problem.get("business_outcome") or not problem.get("scope"):
        errors.append("Customer problem needs a measurable outcome and bounded scope")
    if len(problem.get("non_goals", [])) < 3:
        errors.append("At least three protected non-goals are required")

    discovery = plan.get("discovery_and_value", {})
    value = discovery.get("value_hypothesis", {})
    if len(discovery.get("evidence", [])) < 4 or len(discovery.get("assumptions", [])) < 2:
        errors.append("Discovery must separate evidence from owned testable assumptions")
    if not value.get("statement") or not value.get("benefit_formula"):
        errors.append("Value hypothesis needs a statement and calculation contract")

    required_roles = {
        "Technical Deployment Lead", "Forward Deployed Engineer", "AI Engineer",
        "Platform Engineer", "Security Engineer", "Product Partner",
        "Claims Subject-Matter Expert",
    }
    team = plan.get("forward_deployed_team", [])
    roles = [item.get("role") for item in team]
    if set(roles) != required_roles or len(roles) != len(set(roles)):
        errors.append("Forward deployed team must contain seven unique required roles")
    for member in team:
        if not member.get("name") or not member.get("accountability"):
            errors.append(f"{member.get('role')} needs a named person and accountability")
        if float(member.get("allocation_fte", 0)) <= 0:
            errors.append(f"{member.get('role')} needs a positive allocation")

    decisions = plan.get("decision_rights", [])
    required_decisions = {
        "Business outcome and rollout scope", "Architecture and technical exceptions",
        "Security risk acceptance", "Protected claim action", "Go-live or rollback",
        "Productization investment",
    }
    decision_names = [item.get("decision") for item in decisions]
    if set(decision_names) != required_decisions or len(decision_names) != len(set(decision_names)):
        errors.append("Decision rights must cover six unique enterprise decisions")
    for decision in decisions:
        if not decision.get("responsible") or not decision.get("accountable"):
            errors.append(f"{decision.get('decision')} needs responsible and accountable ownership")

    architecture = plan.get("architecture", {})
    components = architecture.get("components", [])
    component_types = {item.get("type") for item in components}
    if not {"human_interface", "probabilistic_ai", "deterministic_control", "protected_action"} <= component_types:
        errors.append("Architecture must separate human, probabilistic, deterministic, and protected-action components")
    if len(architecture.get("trust_boundaries", [])) < 4:
        errors.append("Architecture needs at least four explicit trust boundaries")
    workflow = architecture.get("workflow", [])
    try:
        approval_index = next(i for i, item in enumerate(workflow) if "explicit licensed-adjuster approval" in item)
        execution_index = next(i for i, item in enumerate(workflow) if item.startswith("Execute"))
        audit_index = next(i for i, item in enumerate(workflow) if item.startswith("Write identity"))
        if not approval_index < execution_index < audit_index:
            errors.append("Workflow must approve before execution and audit the result")
    except StopIteration:
        errors.append("Workflow is missing approval, execution, or audit ordering")

    evaluation = plan.get("evaluation_and_human_approval", {})
    segments = evaluation.get("required_segments", [])
    gates = evaluation.get("release_gates", [])
    results = evaluation.get("latest_results", {})
    if len(segments) < 9:
        errors.append("Evaluation must cover representative and adversarial segments")
    if {item.get("metric") for item in gates} != set(results):
        errors.append("Every release gate needs a latest result and no ungoverned result")
    approval = evaluation.get("human_approval", {})
    if approval.get("required") is not True or approval.get("role") != "Licensed Claims Adjuster":
        errors.append("Licensed-adjuster approval must be mandatory")
    if len(approval.get("protected_actions", [])) < 3 or len(approval.get("approval_evidence", [])) < 5:
        errors.append("Protected actions and approval evidence are incomplete")

    readiness = plan.get("security_and_readiness", {})
    controls = readiness.get("controls", [])
    required_categories = {
        "identity_access", "data_protection", "model_guardrail", "human_approval",
        "observability_audit", "reliability_recovery", "operations",
    }
    if {item.get("category") for item in controls} != required_categories:
        errors.append("Security review must cover all seven readiness categories")
    for control in controls:
        if not all(control.get(field) for field in ("id", "owner", "evidence", "status")):
            errors.append("Every readiness control needs ID, owner, evidence, and status")
    approval_roles = {item.get("role") for item in readiness.get("approvals", [])}
    if approval_roles != {"Business Owner", "Technical Owner", "Security Approver", "Operations Owner"}:
        errors.append("Business, technical, security, and operations approvals are required")
    if not readiness.get("rollback_action"):
        errors.append("Readiness review needs a concrete rollback action")

    deployment = plan.get("deployment_plan", {})
    boundary = deployment.get("rollout_boundary", {})
    if not boundary.get("feature_flag") or boundary.get("manual_workflow_available") is not True:
        errors.append("Rollout must have a feature flag and preserve the manual workflow")
    milestones = deployment.get("milestones", [])
    milestone_ids = [item.get("id") for item in milestones]
    if len(milestone_ids) < 7 or len(milestone_ids) != len(set(milestone_ids)):
        errors.append("Deployment needs at least seven unique milestones")
    known_ids = set(milestone_ids)
    for milestone in milestones:
        if not all(milestone.get(field) for field in ("id", "name", "owner", "exit_evidence")):
            errors.append("Every milestone needs an ID, name, owner, and exit evidence")
        unknown = set(milestone.get("depends_on", [])) - known_ids
        if unknown:
            errors.append(f"{milestone.get('id')} has unknown dependencies: {sorted(unknown)}")
    visiting: set[str] = set()
    visited: set[str] = set()
    index = {item["id"]: item for item in milestones if item.get("id")}

    def visit(milestone_id: str) -> None:
        if milestone_id in visiting:
            errors.append(f"Deployment dependency cycle includes {milestone_id}")
            return
        if milestone_id in visited or milestone_id not in index:
            return
        visiting.add(milestone_id)
        for dependency in index[milestone_id].get("depends_on", []):
            visit(dependency)
        visiting.remove(milestone_id)
        visited.add(milestone_id)

    for milestone_id in index:
        visit(milestone_id)

    capabilities = plan.get("reusable_capabilities", [])
    allowed_decisions = {"PRODUCT", "PLATFORM", "CONFIGURATION", "CUSTOM_EXTENSION", "RETIRE"}
    if len(capabilities) < 5:
        errors.append("At least five capabilities must be reviewed for reuse")
    for capability in capabilities:
        if capability.get("decision") not in allowed_decisions:
            errors.append(f"{capability.get('capability')} has an invalid reuse decision")
        if not capability.get("owner") or not capability.get("boundary"):
            errors.append(f"{capability.get('capability')} needs an owner and reuse boundary")

    scorecard = plan.get("adoption_and_outcome_scorecard", {})
    targets = scorecard.get("targets", [])
    target_names = [item.get("metric") for item in targets]
    if len(target_names) != 11 or len(target_names) != len(set(target_names)):
        errors.append("Scorecard must contain eleven unique adoption, outcome, quality, safety, and operations gates")
    if scorecard.get("baselines") != baseline:
        errors.append("Problem baseline and scorecard baseline must match exactly")

    if errors:
        raise ValueError("\n".join(f"- {error}" for error in errors))


def validate_pilot(rows: list[dict[str, str]]) -> None:
    expected_columns = {
        "week", "eligible_adjusters", "active_adjusters", "eligible_claims",
        "assisted_claims", "recommendations_shown", "recommendations_accepted",
        "average_handling_minutes", "rework_rate_percent", "quality_score_percent",
        "citation_completeness_percent", "p95_latency_seconds", "model_cost_usd",
        "unauthorized_protected_actions", "audit_completeness_percent",
    }
    errors: list[str] = []
    if not rows or set(rows[0]) != expected_columns:
        errors.append("Pilot-results columns do not match the required schema")
    try:
        weeks = [int(row["week"]) for row in rows]
    except (KeyError, ValueError):
        weeks = []
    if weeks != list(range(1, len(rows) + 1)):
        errors.append("Pilot weeks must be sequential starting at 1")
    for row in rows:
        try:
            eligible_users = int(row["eligible_adjusters"])
            active_users = int(row["active_adjusters"])
            eligible_claims = int(row["eligible_claims"])
            assisted_claims = int(row["assisted_claims"])
            shown = int(row["recommendations_shown"])
            accepted = int(row["recommendations_accepted"])
            percentages = [
                float(row["rework_rate_percent"]), float(row["quality_score_percent"]),
                float(row["citation_completeness_percent"]),
                float(row["audit_completeness_percent"]),
            ]
            handling = float(row["average_handling_minutes"])
            latency = float(row["p95_latency_seconds"])
            cost = float(row["model_cost_usd"])
            unauthorized = int(row["unauthorized_protected_actions"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"Week {row.get('week')} contains invalid numeric data")
            continue
        if not 0 <= active_users <= eligible_users:
            errors.append(f"Week {row['week']} has invalid user counts")
        if not 0 <= accepted <= shown <= assisted_claims <= eligible_claims:
            errors.append(f"Week {row['week']} has invalid claim or recommendation counts")
        if any(not 0 <= value <= 100 for value in percentages):
            errors.append(f"Week {row['week']} has an invalid percentage")
        if min(handling, latency) <= 0 or cost < 0 or unauthorized < 0:
            errors.append(f"Week {row['week']} has invalid time, cost, or incident data")
    if errors:
        raise ValueError("\n".join(f"- {error}" for error in errors))


def validate_risks(rows: list[dict[str, str]]) -> None:
    expected_columns = {
        "risk_id", "category", "description", "probability", "impact", "score",
        "owner", "response", "trigger", "contingency", "status",
    }
    errors: list[str] = []
    if not rows or set(rows[0]) != expected_columns:
        errors.append("Risk-register columns do not match the required schema")
    risk_ids = [row.get("risk_id") for row in rows]
    if len(risk_ids) < 8 or len(risk_ids) != len(set(risk_ids)):
        errors.append("Risk register needs at least eight unique risks")
    for row in rows:
        try:
            probability = int(row["probability"])
            impact = int(row["impact"])
            score = int(row["score"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"{row.get('risk_id')} has invalid scoring")
            continue
        if probability not in range(1, 6) or impact not in range(1, 6):
            errors.append(f"{row['risk_id']} probability and impact must be 1 through 5")
        if score != probability * impact:
            errors.append(f"{row['risk_id']} score must equal probability times impact")
        if row.get("response") not in {"AVOID", "MITIGATE", "TRANSFER", "ACCEPT"}:
            errors.append(f"{row['risk_id']} has an invalid response")
        if row.get("status") not in {"OPEN", "MONITORED", "MITIGATED", "CLOSED"}:
            errors.append(f"{row['risk_id']} has an invalid status")
        if not all(row.get(field) for field in ("owner", "trigger", "contingency")):
            errors.append(f"{row['risk_id']} needs owner, trigger, and contingency")
    if errors:
        raise ValueError("\n".join(f"- {error}" for error in errors))


def calculate_metrics(plan: dict[str, Any], row: dict[str, str]) -> dict[str, float]:
    baseline = plan["adoption_and_outcome_scorecard"]["baselines"]
    value = plan["discovery_and_value"]["value_hypothesis"]
    eligible_users = int(row["eligible_adjusters"])
    active_users = int(row["active_adjusters"])
    eligible_claims = int(row["eligible_claims"])
    assisted_claims = int(row["assisted_claims"])
    shown = int(row["recommendations_shown"])
    accepted = int(row["recommendations_accepted"])
    handling = float(row["average_handling_minutes"])
    rework = float(row["rework_rate_percent"])
    cost = float(row["model_cost_usd"])
    time_saved_hours = assisted_claims * (baseline["average_handling_minutes"] - handling) / 60
    avoided_rework = assisted_claims * (baseline["rework_rate_percent"] - rework) / 100
    gross_benefit = (
        time_saved_hours * value["loaded_adjuster_hourly_cost_usd"]
        + avoided_rework * value["avoided_rework_value_usd"]
    )
    return {
        "active_adoption_percent": percent(active_users, eligible_users),
        "assisted_claim_rate_percent": percent(assisted_claims, eligible_claims),
        "recommendation_acceptance_percent": percent(accepted, shown),
        "handling_time_reduction_percent": percent(
            baseline["average_handling_minutes"] - handling,
            baseline["average_handling_minutes"],
        ),
        "rework_reduction_percent": percent(
            baseline["rework_rate_percent"] - rework,
            baseline["rework_rate_percent"],
        ),
        "quality_score_percent": float(row["quality_score_percent"]),
        "citation_completeness_percent": float(row["citation_completeness_percent"]),
        "p95_latency_seconds": float(row["p95_latency_seconds"]),
        "gross_benefit_usd": round(gross_benefit, 2),
        "benefit_cost_ratio": round(gross_benefit / cost, 2) if cost else 0.0,
        "unauthorized_protected_actions": float(row["unauthorized_protected_actions"]),
        "audit_completeness_percent": float(row["audit_completeness_percent"]),
    }


def build_report(
    plan: dict[str, Any],
    risks: list[dict[str, str]],
    metrics: dict[str, float],
    scorecard_gates: list[dict[str, Any]],
    release_gates: list[dict[str, Any]],
    decision: str,
) -> str:
    problem = plan["customer_problem"]
    readiness = plan["security_and_readiness"]
    rollout = plan["deployment_plan"]["rollout_boundary"]
    lines = [
        "# Enterprise AI Claims Assistant — Executive Deployment Decision", "",
        f"- **Decision:** {decision}",
        f"- **Customer:** {plan['metadata']['customer']}",
        f"- **Candidate:** {plan['metadata']['candidate']}",
        f"- **Approved boundary:** {rollout['cohort']}; maximum {rollout['maximum_claims']} claims over {rollout['duration_days']} days",
        f"- **Business outcome:** {problem['business_outcome']}", "",
        "## Decision Rationale", "",
        f"The four-week pilot passed {sum(item['passed'] for item in scorecard_gates)}/{len(scorecard_gates)} adoption, outcome, quality, safety, and operations gates. "
        f"The pinned release candidate passed {sum(item['passed'] for item in release_gates)}/{len(release_gates)} evaluation and human-approval gates. "
        f"All {len(readiness['controls'])} readiness controls and all {len(readiness['approvals'])} required approvals are complete.", "",
        "## Latest-Week Scorecard", "",
        "| Metric | Rule | Actual | Owner | Result |",
        "| --- | --- | ---: | --- | --- |",
    ]
    for gate in scorecard_gates:
        symbol = ">=" if gate["operator"] == "min" else "<="
        lines.append(
            f"| {gate['metric']} | {symbol} {gate['threshold']} | {gate['actual']:.2f} | "
            f"{gate['owner']} | {'PASS' if gate['passed'] else 'FAIL'} |"
        )
    lines.extend([
        "", "## Release and Human-Approval Evidence", "",
        "| Metric | Rule | Actual | Owner | Result |",
        "| --- | --- | ---: | --- | --- |",
    ])
    for gate in release_gates:
        symbol = ">=" if gate["operator"] == "min" else "<="
        lines.append(
            f"| {gate['metric']} | {symbol} {gate['threshold']} | {gate['actual']:.2f} | "
            f"{gate['owner']} | {'PASS' if gate['passed'] else 'FAIL'} |"
        )
    lines.extend([
        "", "## Rollout and Rollback", "",
        f"- Feature flag: `{rollout['feature_flag']}`",
        f"- Manual workflow available: {str(rollout['manual_workflow_available']).lower()}",
        f"- Rollback: {readiness['rollback_action']}", "",
        "## Highest Risks", "",
        "| Risk | Score | Owner | Status | Trigger | Contingency |",
        "| --- | ---: | --- | --- | --- | --- |",
    ])
    for risk in sorted(risks, key=lambda item: int(item["score"]), reverse=True)[:5]:
        lines.append(
            f"| {risk['risk_id']}: {risk['description']} | {risk['score']} | {risk['owner']} | "
            f"{risk['status']} | {risk['trigger']} | {risk['contingency']} |"
        )
    lines.extend(["", "## Reusable Capability Decisions", ""])
    for capability in plan["reusable_capabilities"]:
        lines.append(
            f"- **{capability['decision']} — {capability['capability']}:** "
            f"{capability['boundary']} Owner: {capability['owner']}."
        )
    lines.extend([
        "", "## Next Governance Decision", "",
        "At day 30, the Business Owner, Claims Operations Owner, Technical Owner, Security Approver, and Product Owner review the scorecard, incidents, open risks, support load, and reusable-capability evidence before expanding, repairing, pausing, or ending the rollout.", "",
    ])
    return "\n".join(lines)


def main() -> int:
    try:
        plan = load_plan(PLAN_FILES)
        risks = load_csv(RISK_FILE)
        pilot_rows = load_csv(PILOT_FILE)
        validate_plan(plan)
        validate_risks(risks)
        validate_pilot(pilot_rows)

        metrics = calculate_metrics(plan, pilot_rows[-1])
        scorecard_gates = []
        for target in plan["adoption_and_outcome_scorecard"]["targets"]:
            actual = metrics[target["metric"]]
            scorecard_gates.append({**target, "actual": actual, "passed": target_passed(target, actual)})

        evaluation = plan["evaluation_and_human_approval"]
        release_gates = []
        for target in evaluation["release_gates"]:
            actual = float(evaluation["latest_results"][target["metric"]])
            release_gates.append({**target, "actual": actual, "passed": target_passed(target, actual)})

        baseline_quality = float(plan["customer_problem"]["baseline"]["quality_score_percent"])
        safety_pass = (
            metrics["unauthorized_protected_actions"] == 0
            and metrics["quality_score_percent"] >= baseline_quality
            and metrics["audit_completeness_percent"] == 100
        )
        readiness = plan["security_and_readiness"]
        controls_pass = all(item["status"] == "PASS" for item in readiness["controls"])
        approvals_pass = all(item["approved"] is True for item in readiness["approvals"])
        risks_ready = all(item["status"] != "OPEN" for item in risks)

        if not safety_pass:
            decision = "PAUSE_AND_INVESTIGATE"
        elif (
            all(item["passed"] for item in scorecard_gates)
            and all(item["passed"] for item in release_gates)
            and controls_pass
            and approvals_pass
            and risks_ready
            and not readiness["open_exceptions"]
        ):
            decision = "APPROVE_PHASED_PRODUCTION_ROLLOUT"
        else:
            decision = "HOLD_FOR_REMEDIATION"

        REPORT_FILE.write_text(
            build_report(plan, risks, metrics, scorecard_gates, release_gates, decision),
            encoding="utf-8",
        )
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        print(f"LAB 11 FAILED\n{exc}")
        return 1

    print("LAB 11 PASSED")
    print(f"- Decision: {decision}")
    print(f"- Capstone decisions connected: {len(CAPSTONE_SECTIONS)}/10")
    print(f"- Latest-week scorecard gates: {sum(item['passed'] for item in scorecard_gates)}/{len(scorecard_gates)}")
    print(f"- Release gates: {sum(item['passed'] for item in release_gates)}/{len(release_gates)}")
    print(f"- Readiness controls: {sum(item['status'] == 'PASS' for item in readiness['controls'])}/{len(readiness['controls'])}")
    print(f"- Risks with owners and responses: {len(risks)}/{len(risks)}")
    print(f"- Report: {REPORT_FILE.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

The program loads the five workshop JSON artifacts and rejects mismatched metadata or duplicated sections. It then verifies the problem, value, team, decisions, architecture, evaluation, approval, readiness, deployment, risks, reuse boundaries, and scorecard before calculating the latest-week business results.

### Verification checkpoint

- **Expected result:** `python3 -m py_compile capstone_review.py` returns to the prompt without output.
- **Acceptable variation:** Use `python` instead of `python3` when it points to Python 3.10 or later.
- **Failure indicator:** Python prints a syntax or indentation error.
- **Corrective action:** Repair the first reported line using the complete source above and compile again.

## Step 4 — Run the Final Deployment Decision

```bash
python3 -m json.tool reuse_scorecard.json
python3 -m py_compile capstone_review.py
python3 capstone_review.py
```

Expected output:

```text
LAB 11 PASSED
- Decision: APPROVE_PHASED_PRODUCTION_ROLLOUT
- Capstone decisions connected: 10/10
- Latest-week scorecard gates: 11/11
- Release gates: 6/6
- Readiness controls: 7/7
- Risks with owners and responses: 8/8
- Report: executive_deployment_decision.md
```

`LAB 11 PASSED` means the five artifacts are structurally coherent. The business decision is separate: unsafe evidence produces `PAUSE_AND_INVESTIGATE`, while incomplete non-safety evidence produces `HOLD_FOR_REMEDIATION`.

### Verification checkpoint

- **Expected result:** The exact decision and gate counts above print, and `executive_deployment_decision.md` is created.
- **Acceptable variation:** A different valid dataset may correctly produce hold or pause.
- **Failure indicator:** The program reports a schema error, mismatched metadata, a failed safety floor, or no report.
- **Corrective action:** Fix the first source error or failed evidence condition; do not weaken a gate simply to obtain approval.

## Step 5 — Inspect the Executive Decision

```bash
sed -n '1,260p' executive_deployment_decision.md
```

Confirm that the memo includes:

- the candidate and phased rollout boundary;
- business outcome and decision rationale;
- 11 scorecard gates and six release gates;
- feature flag, manual fallback, and rollback action;
- the five highest delivery risks;
- all reusable-capability decisions; and
- the day-30 governance decision.

This memo becomes the evidence source for **Role Play: Present the Executive Go-Live Recommendation**. The role play should defend a bounded rollout, not claim that pilot success removes uncertainty.

### Verification checkpoint

- **Expected result:** Every executive claim traces to one workshop artifact, a CSV result, or a calculated gate.
- **Acceptable variation:** Your presentation may emphasize different risks while preserving the evidence and boundary.
- **Failure indicator:** The recommendation relies on confidence or stakeholder excitement without measurable evidence, rollback, or ownership.
- **Corrective action:** Replace unsupported statements with exact evidence, owners, triggers, or rollout constraints.

## Step 6 — Apply the Final Delivery Rubric

Before committing, score the capstone across five dimensions:

| Dimension | Evidence of readiness |
| --- | --- |
| Customer and value clarity | Problem, baseline, outcome, scope, assumptions, and value formula agree |
| Authority and ownership | Team capacity and decision rights preserve customer authority |
| Technical and safety design | Architecture, evaluation, approval, security, audit, and recovery are enforceable |
| Delivery control | Milestones, dependencies, risks, cutover, rollback, hypercare, and handoff are executable |
| Product and outcome learning | Reuse boundaries and the scorecard support a day-30 portfolio and scale decision |

A strong submission is not the one with the most content. It is the one where each decision has evidence, ownership, a boundary, and a next action.

### Verification checkpoint

- **Expected result:** You can identify at least one artifact and one decision owner for every rubric dimension.
- **Acceptable variation:** Use the course's numeric rubric if provided; preserve these five evidence dimensions.
- **Failure indicator:** A dimension receives a high score because a document exists, even though its decisions conflict with another artifact.
- **Corrective action:** Resolve the conflict and rerun the integrated review before scoring.

## Step 7 — Add the Handoff and Commit

Create `README.md`:

```markdown
# Lab 11 — Capstone: Lead an Enterprise AI Deployment

One shared Enterprise AI Claims Assistant capstone completed through five progressive workshops.

## Workshop guides

1. [Workshop 1: Problem and Value](WORKSHOP_01_problem_value.md) / [HTML](WORKSHOP_01_problem_value.html)
2. [Workshop 2: Team and Decisions](WORKSHOP_02_team_decisions.md) / [HTML](WORKSHOP_02_team_decisions.html)
3. [Workshop 3: Architecture and Approval](WORKSHOP_03_architecture_approval.md) / [HTML](WORKSHOP_03_architecture_approval.html)
4. [Workshop 4: Readiness and Delivery](WORKSHOP_04_readiness_delivery.md) / [HTML](WORKSHOP_04_readiness_delivery.html)
5. [Workshop 5: Reuse and Outcomes](WORKSHOP_05_reuse_outcomes.md) / [HTML](WORKSHOP_05_reuse_outcomes.html)

## Project artifacts

- Five workshop JSON decision artifacts
- `risk_register.csv` and `pilot_results.csv`
- `capstone_review.py`
- Generated `executive_deployment_decision.md`

Run `python3 -m py_compile capstone_review.py`, then `python3 capstone_review.py`.

Requires Python 3.10 or later and only the Python standard library.
```

```bash
git add .
git commit -m "Complete enterprise AI deployment capstone"
git status --short --branch
```

### Verification checkpoint

- **Expected result:** Git reports `main` with no changed or untracked files.
- **Acceptable variation:** Additional earlier workshop commits are expected.
- **Failure indicator:** The generated report is missing, caches are tracked, or source files remain uncommitted.
- **Corrective action:** Rerun the review, confirm `.gitignore`, stage the intended files, commit, and check status again.

## Map the Completed Workflow

| Workshop | Artifact | Capstone decisions completed |
| --- | --- | --- |
| 1 | `problem_value.json` | Customer problem, business outcome, discovery brief, and value hypothesis |
| 2 | `team_decisions.json` | Forward deployed team, ownership, and decision rights |
| 3 | `architecture_approval.json` | Production architecture, evaluation, and human approval |
| 4 | `readiness_deployment.json`, `risk_register.csv` | Security, readiness, deployment plan, and risks |
| 5 | `reuse_scorecard.json`, `pilot_results.csv` | Reusable capabilities, adoption, outcomes, and rollout decision |
| Integration | `capstone_review.py`, generated memo | Executive recommendation and final rubric evidence |

## Troubleshooting Cheatsheet

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Metadata mismatch | Workshop files describe different case versions | Copy the complete metadata object from Workshop 1 into all five JSON files. |
| Duplicate capstone section | The same decision section appears in two JSON files | Keep each section only in its assigned workshop artifact. |
| Pilot columns do not match | A CSV header was renamed or omitted | Restore the exact Step 2 header. |
| Risk score fails | Probability, impact, and score disagree | Recalculate score as probability × impact. |
| `HOLD_FOR_REMEDIATION` | A non-safety evidence condition failed | Repair the evidence or reduce scope without weakening the threshold. |
| `PAUSE_AND_INVESTIGATE` | A safety floor failed | Stop rollout, preserve evidence, use manual handling, and follow rollback. |
| Report did not update | The review was not rerun | Run `python3 capstone_review.py` again. |

## Cleanup

The capstone creates no cloud resources. Remove local Python caches while keeping all completion evidence:

```bash
find . -type d -name __pycache__ -prune -exec rm -rf {} +
```

## Completion Check

- [ ] All five workshop JSON files use identical metadata.
- [ ] Ten capstone decisions are present and connected.
- [ ] Reuse decisions have owners and explicit boundaries.
- [ ] Eleven scorecard gates cover adoption, outcomes, quality, safety, value, latency, and audit.
- [ ] The integrated review passes and generates the executive memo.
- [ ] I can defend the phased boundary, top risks, rollback, and day-30 decision.
- [ ] I applied the final rubric to evidence, not document count.
- [ ] My capstone repository is clean on `main`.

## Reflection

1. Which pilot metric could look healthy while masking a poor employee or customer outcome?
2. Which capability should remain customer-specific even if another customer asks for something similar?
3. What exact evidence would cause you to expand, repair, pause, or end the rollout at day 30?
4. Which conflict between two artifacts would be most dangerous to miss in an executive review?
