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
