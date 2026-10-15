# Lab 08 — Build an AI Adoption and Business-Outcome Scorecard

## Goal

Build an evidence-based scorecard for Northstar Mutual's Enterprise AI Claims Assistant that separates user adoption, model and safety performance, and customer business outcomes. Calculate weekly trends and produce a scale, repair, or pause recommendation from the bounded-pilot evidence.

Work in your own new project directory. The completed reference repository is only for comparison when you are stuck.

## What You'll Build or Produce

- `adoption_scorecard.json` — the measurement contract, baselines, targets, owners, financial assumptions, and decision policy.
- `pilot_metrics.csv` — four weeks of traceable adoption, workflow, quality, cost, and safety evidence.
- `scorecard.py` — the executable metrics and decision calculation.
- `business_outcome_report.md` — the generated weekly scorecard and recommendation.
- `.gitignore` — Git hygiene.

## Estimated Time

70–95 minutes.

## Cost Guardrails

The lab runs locally with Python's standard library. It makes no API calls and creates no cloud or paid resources.

## Completion Evidence

- `python3 -m py_compile scorecard.py` succeeds.
- `python3 scorecard.py` prints `LAB 08 PASSED` and `SCALE_WITH_MONITORING`.
- Four weekly rows pass validation and preserve the original evidence.
- The scorecard evaluates eight owned decision gates.
- Adoption, model/safety, and business-outcome metrics remain separate.
- `business_outcome_report.md` shows trend, business value, owners, and the recommendation.
- Git is clean on `main`.

## Prerequisites

- Python 3.10 or later
- Git
- A text editor
- Basic percentages, baselines, operational KPIs, and ROI concepts
- The approved 25-adjuster claims-assistant pilot and its protected-action boundary.

## Where This Lab Fits

This lab evaluates what happened after the bounded pilot was delivered. You will keep adoption, model and safety performance, and business outcomes separate, then decide whether to scale, repair, pause, or exit. The evidence also helps Lab 09 distinguish reusable product signals from one-customer requests.

## Step 1 — Create Your Project

```bash
mkdir lab_08_ai_adoption_business_outcome_scorecard
cd lab_08_ai_adoption_business_outcome_scorecard
```

Create `.gitignore`:

```gitignore
__pycache__/
*.py[cod]
.DS_Store
```

### Verification checkpoint

- **Expected result:** Only `.gitignore` exists in your learner-owned directory.
- **Acceptable variation:** Another directory name is fine.
- **Failure indicator:** You are editing the completed reference repository.
- **Corrective action:** Create a separate directory and continue there.

## Step 2 — Define the Measurement Contract

Create `adoption_scorecard.json`:

```json
{
  "metadata": {
    "lab_id": "lab_08",
    "customer": "Northstar Mutual",
    "initiative": "Enterprise AI Claims Assistant",
    "pilot_cohort": "25 licensed claims adjusters",
    "measurement_window": "four weekly pilot reviews",
    "prepared_date": "2026-08-16"
  },
  "measurement_contract": {
    "primary_user": "Licensed Claims Adjuster",
    "assisted_decision": "Request evidence continue review or escalate",
    "expected_action": "Adjuster reviews cited evidence and accepts overrides or escalates the recommendation",
    "business_outcome": "Faster claim review with less rework and equal or better quality without unauthorized protected actions"
  },
  "baselines": {
    "average_handling_minutes": 42,
    "rework_rate_percent": 14,
    "quality_score_percent": 86
  },
  "safety_floor": {
    "quality_score_percent": 86,
    "unauthorized_protected_actions": 0
  },
  "metric_groups": {
    "adoption": [
      "active_adoption_percent",
      "assisted_claim_rate_percent",
      "recommendation_acceptance_percent"
    ],
    "model_and_safety": [
      "quality_score_percent",
      "unauthorized_protected_actions"
    ],
    "business_outcomes": [
      "handling_time_reduction_percent",
      "rework_reduction_percent",
      "gross_benefit_usd",
      "benefit_cost_ratio"
    ]
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
      "metric": "benefit_cost_ratio",
      "operator": "min",
      "threshold": 3,
      "owner": "Finance Partner"
    },
    {
      "metric": "unauthorized_protected_actions",
      "operator": "max",
      "threshold": 0,
      "owner": "Security Owner"
    }
  ],
  "financial_assumptions": {
    "loaded_adjuster_hourly_cost_usd": 85,
    "avoided_rework_value_usd": 120,
    "benefit_definition": "Time value plus avoided rework value",
    "cost_definition": "Recorded model and platform variable cost"
  },
  "decision_policy": {
    "scale_with_monitoring": "All eight latest-week gates pass and adoption improves for at least two consecutive weeks.",
    "repair_before_scale": "Safety gate passes but one or more adoption or business-outcome gates fail.",
    "pause_and_investigate": "Any unauthorized protected action occurs or quality falls below the approved safety floor."
  },
  "owners": [
    {
      "role": "Business Owner",
      "name": "Elena Ruiz"
    },
    {
      "role": "Claims Operations Lead",
      "name": "Priya Shah"
    },
    {
      "role": "Claims Quality Lead",
      "name": "Marcus Green"
    },
    {
      "role": "Finance Partner",
      "name": "Taylor Reed"
    },
    {
      "role": "Technical Owner",
      "name": "Jordan Kim"
    }
  ],
  "review_cadence": "Weekly pilot scorecard review with a day-14 scale repair pause or exit decision"
}
```

The measurement contract ties a user and assisted decision to an expected action and business outcome. It also prevents a strong model-quality score from being mistaken for adoption or ROI.

### Verification checkpoint

- **Expected result:** The file includes baselines, an explicit quality and protected-action safety floor, three metric groups, eight targets, financial assumptions, five owners, and scale/repair/pause rules.
- **Acceptable variation:** Customer-approved targets may differ if baselines and owners remain explicit.
- **Failure indicator:** Metrics lack baselines, definitions, owners, or a decision they influence.
- **Corrective action:** Restore the user-decision-action-outcome chain and measurable gates.

## Step 3 — Record Weekly Pilot Evidence

Create `pilot_metrics.csv`:

```csv
week,eligible_adjusters,active_adjusters,eligible_claims,assisted_claims,recommendations_shown,recommendations_accepted,average_handling_minutes,rework_rate_percent,quality_score_percent,model_cost_usd,unauthorized_protected_actions
1,25,14,100,48,45,30,38,12.5,88.5,80,0
2,25,18,110,70,65,51,34,10.5,91.0,105,0
3,25,21,115,90,85,70,31,9.2,93.2,135,0
4,25,22,120,105,100,82,29,8.5,94.5,165,0
```

Keep numerator and denominator evidence instead of storing only percentages. This makes adoption and acceptance rates independently reviewable and prevents denominator changes from hiding weak usage.

### Verification checkpoint

- **Expected result:** Weeks 1–4 contain eligible and active users, claim volume, recommendation behavior, handling time, rework, quality, cost, and protected-action incidents.
- **Acceptable variation:** You may add later weeks using the same schema.
- **Failure indicator:** Accepted recommendations exceed shown recommendations, assisted claims exceed eligible claims, or only favorable weeks remain.
- **Corrective action:** Repair the source evidence and preserve every reviewed week.

## Step 4 — Build the Executable Scorecard

Create `scorecard.py`:

```python
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
```

The program validates evidence identity and ranges, computes adoption and business-value metrics from raw counts, evaluates owned targets, checks adoption trend, and generates the decision record.

### Verification checkpoint

- **Expected result:** Calculations use the JSON baselines and financial assumptions rather than hidden constants.
- **Acceptable variation:** You may add metrics if they remain clearly assigned to adoption, model/safety, or business outcomes.
- **Failure indicator:** ROI ignores costs, percentages are manually typed, or a safety incident can still produce a scale decision.
- **Corrective action:** Reconnect calculations to raw evidence and retain fail-closed safety logic.

## Step 5 — Run and Inspect the Scorecard

```bash
python3 -m py_compile scorecard.py
python3 scorecard.py
```

Expected output:

```text
LAB 08 PASSED
- Decision: SCALE_WITH_MONITORING
- Weeks analyzed: 4
- Latest active adoption: 88.0%
- Latest assisted-claim rate: 87.5%
- Decision gates passed: 8/8
- Report: business_outcome_report.md
```

Inspect the report:

```bash
sed -n '1,240p' business_outcome_report.md
```

On Windows PowerShell:

```powershell
Get-Content business_outcome_report.md
```

### Verification checkpoint

- **Expected result:** The latest week passes eight gates and the report shows four-week improvement and positive business value.
- **Acceptable variation:** Real evidence may correctly return `REPAIR_BEFORE_SCALE` or `PAUSE_AND_INVESTIGATE`.
- **Failure indicator:** The report uses no baseline, omits costs, or combines adoption and quality into one opaque score.
- **Corrective action:** Fix the named evidence or target; do not lower a gate merely to obtain a scale recommendation.

## Step 6 — Conduct the Outcome Review

Answer from the report:

1. Are users active, and are they using AI on eligible claims?
2. Does acceptance represent trust or merely lack of alternatives?
3. Is handling-time improvement accompanied by stable or better quality?
4. Which benefit assumption would Finance challenge first?
5. What ongoing monitoring is required even after a scale decision?

### Verification checkpoint

- **Expected result:** Each answer distinguishes behavior, model performance, and business value.
- **Acceptable variation:** Recommend a narrower scale cohort where a segment needs repair.
- **Failure indicator:** The recommendation depends on a single average or ignores user workflow evidence.
- **Corrective action:** Segment the metric, add the responsible owner, or narrow the decision.

## Step 7 — Commit Your Evidence

```bash
git init -b main
git add .gitignore adoption_scorecard.json pilot_metrics.csv scorecard.py business_outcome_report.md
git commit -m "Complete AI adoption and business outcome scorecard"
git status --short --branch
```

### Verification checkpoint

- **Expected result:** `main` is clean.
- **Acceptable variation:** Another descriptive commit message is fine.
- **Failure indicator:** The generated report is absent or caches are tracked.
- **Corrective action:** Rerun the scorecard, stage the intended five project files, and commit.

## Map the Completed Workflow

1. Define the user, assisted decision, action, and outcome.
2. Establish operational baselines before interpreting improvement.
3. Capture raw weekly adoption, workflow, quality, cost, and safety evidence.
4. Calculate adoption, model/safety, and business-outcome metrics separately.
5. Apply owned thresholds and safety gates.
6. Decide to scale with monitoring, repair before scale, or pause and investigate.
7. Continue measurement after the decision.

## Troubleshooting Cheatsheet

| Symptom | Likely cause | Corrective action |
| --- | --- | --- |
| Invalid columns | CSV schema changed | Restore the documented header |
| Invalid counts | A numerator exceeds its denominator | Correct the source evidence |
| Missing target | A decision metric is absent from metric groups | Add it to the correct group |
| Weak adoption | Active or assisted rates miss target | Investigate workflow access training and trust |
| ROI looks inflated | Costs or denominator assumptions are missing | Restore variable cost and approved value assumptions |
| Pause decision | Unauthorized protected action occurred | Stop scale and investigate the control failure |
| Stale report | Inputs changed | Rerun `python3 scorecard.py` |

## Cleanup

```bash
python3 -c "import shutil; shutil.rmtree('__pycache__', ignore_errors=True)"
```

Keep the four learner-built artifacts, `.gitignore`, and Git history.

## Completion Check

- [ ] I defined the measurement contract.
- [ ] I established handling-time rework and quality baselines.
- [ ] I preserved raw numerator and denominator evidence.
- [ ] I separated adoption model/safety and business outcomes.
- [ ] I evaluated all eight decision gates.
- [ ] I included cost in the value calculation.
- [ ] I protected the pause condition for unauthorized actions.
- [ ] I generated and reviewed `business_outcome_report.md`.
- [ ] I committed a clean repository.

## Reflection

1. Which metric is the strongest evidence of workflow adoption?
2. What additional evidence would make the financial benefit credible to Finance?
3. When should a high-quality pilot be repaired instead of scaled?
