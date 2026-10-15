#!/usr/bin/env python3
"""Evaluate bounded-pilot evidence and produce a release decision report."""

from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import mean
from typing import Any

ROOT = Path(__file__).resolve().parent
PLAN_FILE = ROOT / "build_release_plan.json"
CASES_FILE = ROOT / "evaluation_cases.json"
RESULTS_FILE = ROOT / "evaluation_results.json"
REPORT_FILE = ROOT / "release_decision.md"


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON artifact and fail with a useful file-specific message."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot load {path.name}: {exc}") from exc


def percent(numerator: int, denominator: int) -> float:
    """Return a percentage, treating an empty required sample as zero."""
    return round(100 * numerator / denominator, 2) if denominator else 0.0


def nearest_rank_p95(values: list[float]) -> float:
    """Calculate p95 with the nearest-rank method."""
    if not values:
        return 0.0
    ordered = sorted(values)
    index = max(0, math.ceil(0.95 * len(ordered)) - 1)
    return round(ordered[index], 2)


def validate_inputs(
    plan: dict[str, Any], cases_doc: dict[str, Any], results_doc: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Validate evidence identity, coverage, and one-to-one case results."""
    errors: list[str] = []
    required_plan_sections = {
        "metadata",
        "decision_contract",
        "version_manifest",
        "build",
        "evaluation",
        "release_gates",
        "release",
    }
    missing = required_plan_sections - set(plan)
    if missing:
        errors.append("Missing plan sections: " + ", ".join(sorted(missing)))

    cases = cases_doc.get("cases", [])
    results = results_doc.get("results", [])
    case_ids = [item.get("case_id") for item in cases]
    result_ids = [item.get("case_id") for item in results]
    if not cases or len(case_ids) != len(set(case_ids)):
        errors.append("Evaluation case IDs must be present and unique")
    if not results or len(result_ids) != len(set(result_ids)):
        errors.append("Evaluation result IDs must be present and unique")
    if set(case_ids) != set(result_ids):
        errors.append("Every evaluation case must have exactly one matching result")

    allowed = set(plan.get("decision_contract", {}).get("allowed_recommendations", []))
    for case in cases:
        if case.get("expected_recommendation") not in allowed:
            errors.append(f"{case.get('case_id')} has an unsupported expected recommendation")
        if not case.get("segments"):
            errors.append(f"{case.get('case_id')} must name at least one segment")

    if cases_doc.get("dataset_id") != plan.get("version_manifest", {}).get(
        "evaluation_dataset"
    ):
        errors.append("Dataset ID does not match the version manifest")
    if results_doc.get("version_manifest") != plan.get("version_manifest"):
        errors.append("Evaluation results do not match the release version manifest")

    environments = [item.get("name") for item in plan.get("build", {}).get("environments", [])]
    if environments != ["dev", "test", "staging", "prod"]:
        errors.append("Promotion path must be dev, test, staging, then prod")
    if plan.get("decision_contract", {}).get("human_approval_required") is not True:
        errors.append("Protected actions must retain explicit human approval")
    if plan.get("release", {}).get("pilot", {}).get("manual_workflow_available") is not True:
        errors.append("The manual claims workflow must remain available")

    if errors:
        raise ValueError("\n".join(f"- {error}" for error in errors))
    return cases, results


def calculate_metrics(
    plan: dict[str, Any], cases: list[dict[str, Any]], results: list[dict[str, Any]]
) -> dict[str, float]:
    """Calculate the exact release metrics from case-level evidence."""
    result_by_id = {item["case_id"]: item for item in results}
    required_segments = set(plan["evaluation"]["required_segments"])
    observed_segments = {segment for case in cases for segment in case["segments"]}
    matching = sum(
        result_by_id[case["case_id"]]["recommendation"]
        == case["expected_recommendation"]
        for case in cases
    )
    injection_cases = [case for case in cases if case["prompt_injection"]]
    injection_blocks = sum(
        result_by_id[case["case_id"]]["injection_blocked"] is True
        for case in injection_cases
    )
    protected_results = [item for item in results if item["protected_action_attempted"]]

    return {
        "case_count": float(len(cases)),
        "segment_coverage_percent": percent(
            len(required_segments & observed_segments), len(required_segments)
        ),
        "recommendation_agreement_percent": percent(matching, len(cases)),
        "citation_completeness_percent": percent(
            sum(item["citation_complete"] is True for item in results), len(results)
        ),
        "schema_validity_percent": percent(
            sum(item["schema_valid"] is True for item in results), len(results)
        ),
        "prompt_injection_block_percent": percent(injection_blocks, len(injection_cases)),
        "protected_action_human_approval_percent": percent(
            sum(item["human_approval_recorded"] is True for item in protected_results),
            len(protected_results),
        ),
        "unauthorized_protected_actions": float(
            sum(item["unauthorized_action"] is True for item in results)
        ),
        "p95_latency_seconds": nearest_rank_p95(
            [float(item["latency_seconds"]) for item in results]
        ),
        "mean_cost_usd": round(mean(float(item["cost_usd"]) for item in results), 2),
        "audit_completeness_percent": percent(
            sum(item["audit_complete"] is True for item in results), len(results)
        ),
    }


def evaluate_gates(
    plan: dict[str, Any], metrics: dict[str, float]
) -> list[dict[str, Any]]:
    """Evaluate declarative min/max gates without hiding release policy in code."""
    evaluations: list[dict[str, Any]] = []
    for gate in plan["release_gates"]:
        metric = gate["metric"]
        if metric not in metrics:
            raise ValueError(f"No calculated value for release gate: {metric}")
        actual = metrics[metric]
        threshold = float(gate["threshold"])
        operator = gate["operator"]
        if operator == "min":
            passed = actual >= threshold
        elif operator == "max":
            passed = actual <= threshold
        else:
            raise ValueError(f"Unsupported gate operator for {metric}: {operator}")
        evaluations.append({**gate, "actual": actual, "passed": passed})
    return evaluations


def format_number(value: float) -> str:
    """Display integer-valued metrics without a trailing decimal."""
    return str(int(value)) if value.is_integer() else f"{value:.2f}"


def build_report(
    plan: dict[str, Any], metrics: dict[str, float], gates: list[dict[str, Any]]
) -> tuple[str, str]:
    """Create the auditable decision record and return its decision label."""
    approvers = plan["release"]["approvers"]
    approvals_complete = all(item.get("approved") is True for item in approvers)
    hard_gates_pass = all(item["passed"] for item in gates if item["hard_gate"])
    decision = (
        "APPROVE_BOUNDED_PILOT"
        if hard_gates_pass and approvals_complete
        else "HOLD_FOR_REMEDIATION"
    )

    lines = [
        "# Enterprise AI Claims Assistant — Release Decision",
        "",
        f"- **Decision:** {decision}",
        f"- **Evaluation run:** {plan['metadata']['decision_date']}",
        f"- **Release scope:** {plan['build']['smallest_valuable_slice']}",
        "",
        "## Version Manifest",
        "",
        "| Artifact | Version |",
        "| --- | --- |",
    ]
    lines.extend(
        f"| {name.replace('_', ' ').title()} | `{version}` |"
        for name, version in plan["version_manifest"].items()
    )
    lines.extend(
        [
            "",
            "## Release Gates",
            "",
            "| Metric | Rule | Actual | Result |",
            "| --- | --- | ---: | --- |",
        ]
    )
    for gate in gates:
        symbol = ">=" if gate["operator"] == "min" else "<="
        lines.append(
            f"| {gate['metric']} | {symbol} {gate['threshold']} | "
            f"{format_number(float(gate['actual']))} | "
            f"{'PASS' if gate['passed'] else 'FAIL'} |"
        )
    lines.extend(
        [
            "",
            "## Required Approvals",
            "",
        ]
    )
    lines.extend(
        f"- {'Approved' if item['approved'] else 'Pending'} — {item['role']}: {item['name']}"
        for item in approvers
    )
    pilot = plan["release"]["pilot"]
    lines.extend(
        [
            "",
            "## Bounded Pilot",
            "",
            f"- Cohort: {pilot['cohort']}",
            f"- Maximum volume: {pilot['maximum_claims']} claims",
            f"- Duration: {pilot['duration_days']} days",
            f"- Feature flag: `{pilot['feature_flag']}`",
            "- Manual workflow remains available: yes",
            "",
            "## Rollback",
            "",
        ]
    )
    lines.extend(f"- {trigger}" for trigger in plan["release"]["rollback_triggers"])
    lines.extend(["", f"**Action:** {plan['release']['rollback_action']}", ""])
    return "\n".join(lines), decision


def main() -> int:
    try:
        plan = load_json(PLAN_FILE)
        cases_doc = load_json(CASES_FILE)
        results_doc = load_json(RESULTS_FILE)
        cases, results = validate_inputs(plan, cases_doc, results_doc)
        metrics = calculate_metrics(plan, cases, results)
        gates = evaluate_gates(plan, metrics)
        report, decision = build_report(plan, metrics, gates)
        REPORT_FILE.write_text(report, encoding="utf-8")
    except (KeyError, TypeError, ValueError) as exc:
        print(f"LAB 05 FAILED\n{exc}")
        return 1

    failed = [item["metric"] for item in gates if item["hard_gate"] and not item["passed"]]
    print("LAB 05 PASSED")
    print(f"- Decision: {decision}")
    print(f"- Evaluation cases: {int(metrics['case_count'])}")
    print(f"- Release gates passed: {len(gates) - len(failed)}/{len(gates)}")
    print(f"- p95 latency: {metrics['p95_latency_seconds']:.2f} seconds")
    print(f"- Mean cost: ${metrics['mean_cost_usd']:.2f} per assist")
    print(f"- Report: {REPORT_FILE.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

