#!/usr/bin/env python3
"""Calculate adoption and business outcomes for the claims-assistant pilot."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
SPEC_FILE = ROOT / "adoption_scorecard.json"
METRICS_FILE = ROOT / "pilot_metrics.csv"
REPORT_FILE = ROOT / "business_outcome_report.md"


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot load {path.name}: {exc}") from exc


def load_rows(path: Path) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))
    except OSError as exc:
        raise ValueError(f"Cannot load {path.name}: {exc}") from exc


def percent(numerator: float, denominator: float) -> float:
    return round(100 * numerator / denominator, 2) if denominator else 0.0


def validate(spec: dict[str, Any], rows: list[dict[str, str]]) -> None:
    errors: list[str] = []
    required_sections = {
        "metadata", "measurement_contract", "baselines", "metric_groups",
        "targets", "safety_floor", "financial_assumptions", "decision_policy", "owners",
        "review_cadence",
    }
    missing = required_sections - set(spec)
    if missing:
        errors.append("Missing scorecard sections: " + ", ".join(sorted(missing)))

    expected_columns = {
        "week", "eligible_adjusters", "active_adjusters", "eligible_claims",
        "assisted_claims", "recommendations_shown", "recommendations_accepted",
        "average_handling_minutes", "rework_rate_percent", "quality_score_percent",
        "model_cost_usd", "unauthorized_protected_actions",
    }
    if rows and set(rows[0]) != expected_columns:
        errors.append("Pilot-metrics columns do not match the required schema")
    weeks = [int(row["week"]) for row in rows] if rows else []
    if weeks != list(range(1, len(rows) + 1)):
        errors.append("Weeks must be sequential starting at 1")

    for row in rows:
        try:
            eligible_adjusters = int(row["eligible_adjusters"])
            active_adjusters = int(row["active_adjusters"])
            eligible_claims = int(row["eligible_claims"])
            assisted_claims = int(row["assisted_claims"])
            shown = int(row["recommendations_shown"])
            accepted = int(row["recommendations_accepted"])
            handling = float(row["average_handling_minutes"])
            rework = float(row["rework_rate_percent"])
            quality = float(row["quality_score_percent"])
            cost = float(row["model_cost_usd"])
            unauthorized = int(row["unauthorized_protected_actions"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"Week {row.get('week')} contains invalid numeric data")
            continue
        if not (0 <= active_adjusters <= eligible_adjusters):
            errors.append(f"Week {row['week']} has invalid adjuster counts")
        if not (0 <= assisted_claims <= eligible_claims):
            errors.append(f"Week {row['week']} has invalid claim counts")
        if not (0 <= accepted <= shown <= assisted_claims):
            errors.append(f"Week {row['week']} has invalid recommendation counts")
        if handling <= 0 or cost < 0 or unauthorized < 0:
            errors.append(f"Week {row['week']} has invalid time cost or incident values")
        if not (0 <= rework <= 100 and 0 <= quality <= 100):
            errors.append(f"Week {row['week']} has invalid percentage values")

    target_metrics = [item.get("metric") for item in spec.get("targets", [])]
    if len(target_metrics) != 8 or len(target_metrics) != len(set(target_metrics)):
        errors.append("Exactly eight unique decision targets are required")
    grouped = {metric for metrics in spec.get("metric_groups", {}).values() for metric in metrics}
    if set(target_metrics) - grouped:
        errors.append("Every target metric must belong to a scorecard metric group")
    if errors:
        raise ValueError("\n".join(f"- {error}" for error in errors))


def calculate(spec: dict[str, Any], row: dict[str, str]) -> dict[str, float]:
    baseline = spec["baselines"]
    assumptions = spec["financial_assumptions"]
    eligible_adjusters = int(row["eligible_adjusters"])
    active_adjusters = int(row["active_adjusters"])
    eligible_claims = int(row["eligible_claims"])
    assisted_claims = int(row["assisted_claims"])
    shown = int(row["recommendations_shown"])
    accepted = int(row["recommendations_accepted"])
    handling = float(row["average_handling_minutes"])
    rework = float(row["rework_rate_percent"])
    quality = float(row["quality_score_percent"])
    cost = float(row["model_cost_usd"])
    time_saved_hours = assisted_claims * (baseline["average_handling_minutes"] - handling) / 60
    avoided_rework = assisted_claims * (baseline["rework_rate_percent"] - rework) / 100
    gross_benefit = (
        time_saved_hours * assumptions["loaded_adjuster_hourly_cost_usd"]
        + avoided_rework * assumptions["avoided_rework_value_usd"]
    )
    return {
        "active_adoption_percent": percent(active_adjusters, eligible_adjusters),
        "assisted_claim_rate_percent": percent(assisted_claims, eligible_claims),
        "recommendation_acceptance_percent": percent(accepted, shown),
        "handling_time_reduction_percent": percent(baseline["average_handling_minutes"] - handling, baseline["average_handling_minutes"]),
        "rework_reduction_percent": percent(baseline["rework_rate_percent"] - rework, baseline["rework_rate_percent"]),
        "quality_score_percent": round(quality, 2),
        "gross_benefit_usd": round(gross_benefit, 2),
        "benefit_cost_ratio": round(gross_benefit / cost, 2) if cost else 0.0,
        "unauthorized_protected_actions": float(row["unauthorized_protected_actions"]),
    }


def evaluate(spec: dict[str, Any], metrics: dict[str, float]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for target in spec["targets"]:
        actual = metrics[target["metric"]]
        threshold = float(target["threshold"])
        passed = actual >= threshold if target["operator"] == "min" else actual <= threshold
        results.append({**target, "actual": actual, "passed": passed})
    return results


def build_report(
    spec: dict[str, Any],
    rows: list[dict[str, str]],
    weekly: list[dict[str, float]],
    gates: list[dict[str, Any]],
    decision: str,
) -> str:
    lines = [
        "# Enterprise AI Claims Assistant — Adoption and Business-Outcome Scorecard", "",
        f"- **Decision:** {decision}",
        f"- **Pilot:** {spec['metadata']['pilot_cohort']}",
        f"- **Outcome:** {spec['measurement_contract']['business_outcome']}", "",
        "## Weekly Trend", "",
        "| Week | Active adoption | Assisted claims | Acceptance | Handling reduction | Rework reduction | Quality | Benefit / cost |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row, metrics in zip(rows, weekly):
        lines.append(
            f"| {row['week']} | {metrics['active_adoption_percent']:.1f}% | "
            f"{metrics['assisted_claim_rate_percent']:.1f}% | "
            f"{metrics['recommendation_acceptance_percent']:.1f}% | "
            f"{metrics['handling_time_reduction_percent']:.1f}% | "
            f"{metrics['rework_reduction_percent']:.1f}% | "
            f"{metrics['quality_score_percent']:.1f}% | "
            f"{metrics['benefit_cost_ratio']:.2f}x |"
        )
    lines.extend(["", "## Latest-Week Decision Gates", "", "| Metric | Rule | Actual | Owner | Result |", "| --- | --- | ---: | --- | --- |"])
    for gate in gates:
        symbol = ">=" if gate["operator"] == "min" else "<="
        lines.append(
            f"| {gate['metric']} | {symbol} {gate['threshold']} | "
            f"{gate['actual']:.2f} | {gate['owner']} | "
            f"{'PASS' if gate['passed'] else 'FAIL'} |"
        )
    latest = weekly[-1]
    lines.extend([
        "", "## Latest Business Value", "",
        f"- Gross benefit: USD {latest['gross_benefit_usd']:.2f}",
        f"- Benefit-cost ratio: {latest['benefit_cost_ratio']:.2f}x",
        f"- Unauthorized protected actions: {int(latest['unauthorized_protected_actions'])}",
        "", "## Measurement Owners", "",
    ])
    lines.extend(f"- {item['role']}: {item['name']}" for item in spec["owners"])
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    try:
        spec = load_json(SPEC_FILE)
        rows = load_rows(METRICS_FILE)
        validate(spec, rows)
        weekly = [calculate(spec, row) for row in rows]
        gates = evaluate(spec, weekly[-1])
        improving = (
            len(weekly) >= 3
            and weekly[-1]["active_adoption_percent"] >= weekly[-2]["active_adoption_percent"]
            and weekly[-2]["active_adoption_percent"] >= weekly[-3]["active_adoption_percent"]
        )
        safety_pass = (
            weekly[-1]["unauthorized_protected_actions"]
            <= spec["safety_floor"]["unauthorized_protected_actions"]
            and weekly[-1]["quality_score_percent"]
            >= spec["safety_floor"]["quality_score_percent"]
        )
        if all(gate["passed"] for gate in gates) and improving:
            decision = "SCALE_WITH_MONITORING"
        elif safety_pass:
            decision = "REPAIR_BEFORE_SCALE"
        else:
            decision = "PAUSE_AND_INVESTIGATE"
        REPORT_FILE.write_text(build_report(spec, rows, weekly, gates, decision), encoding="utf-8")
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        print(f"LAB 08 FAILED\n{exc}")
        return 1

    passed = sum(gate["passed"] for gate in gates)
    latest = weekly[-1]
    print("LAB 08 PASSED")
    print(f"- Decision: {decision}")
    print(f"- Weeks analyzed: {len(rows)}")
    print(f"- Latest active adoption: {latest['active_adoption_percent']:.1f}%")
    print(f"- Latest assisted-claim rate: {latest['assisted_claim_rate_percent']:.1f}%")
    print(f"- Decision gates passed: {passed}/{len(gates)}")
    print(f"- Report: {REPORT_FILE.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
