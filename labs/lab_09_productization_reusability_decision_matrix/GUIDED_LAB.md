# Lab 09 — Create a Productization and Reusability Decision Matrix

## Goal

Evaluate completed assets from Northstar Mutual's Enterprise AI Claims Assistant and decide which should become product capabilities, shared platform services, supported configuration, isolated customer extensions, or retired work. Apply a transparent scoring policy and generate a portfolio decision record.

Build the project in your own new directory. Consult the completed reference only when you need help or want to compare results.

## What You'll Build or Produce

- `productization_policy.json` — scoring dimensions, thresholds, definitions, guardrails, cadence, and accountable roles.
- `productization_matrix.csv` — eight deployment assets with evidence and proposed decisions.
- `productization_review.py` — the executable decision review.
- `productization_review.md` — the generated portfolio recommendation.
- `.gitignore` — Git hygiene.

## Estimated Time

70–95 minutes.

## Cost Guardrails

This local standard-library exercise makes no network calls and requires no paid service.

## Completion Evidence

- `python3 -m py_compile productization_review.py` succeeds.
- `python3 productization_review.py` prints `LAB 09 PASSED` and `PORTFOLIO_PLAN_APPROVED`.
- Eight components receive evidence-based, policy-aligned decisions.
- Product and platform candidates demonstrate repeated demand.
- Custom work has isolation, funding ownership, and a dated review.
- Low-value pilot work has an explicit retirement action.
- `productization_review.md` records the portfolio mix and guardrails.
- Git is clean on `main`.

## Prerequisites

- Python 3.10 or later
- Git
- A text editor
- Familiarity with product, platform, configuration, and customer-specific delivery work
- The prior claims-assistant architecture, security controls, delivery plan, and pilot outcome evidence.

## Where This Lab Fits

This lab moves from one successful deployment to portfolio learning. You will use demand, standardization, strategic fit, coupling, security variance, and maintenance evidence to choose product, platform, configuration, custom extension, or retirement. These decisions determine which capabilities the organization in Lab 10 must fund and staff.

## Step 1 — Create Your Project

```bash
mkdir lab_09_productization_reusability_decision_matrix
cd lab_09_productization_reusability_decision_matrix
```

Create `.gitignore`:

```gitignore
__pycache__/
*.py[cod]
.DS_Store
```

### Verification checkpoint

- **Expected result:** Your learner-owned directory contains only `.gitignore`.
- **Acceptable variation:** Another directory name is acceptable.
- **Failure indicator:** You are editing the completed Lab 09 reference repository.
- **Corrective action:** Create a separate directory and continue there.

## Step 2 — Define the Productization Policy

Create `productization_policy.json`:

```json
{
  "metadata": {
    "lab_id": "lab_09",
    "customer": "Northstar Mutual",
    "initiative": "Enterprise AI Claims Assistant",
    "portfolio_scope": "Claims deployment assets reviewed for cross-customer reuse",
    "review_date": "2026-08-16"
  },
  "scales": {
    "reuse_demand": "1 single customer to 5 repeated demand",
    "standardization": "1 unique implementation to 5 stable shared contract",
    "strategic_fit": "1 peripheral to 5 core differentiation",
    "customer_coupling": "1 independent to 5 deeply customer-specific",
    "security_variance": "1 uniform control to 5 materially different boundaries",
    "maintenance_burden": "1 low to 5 high"
  },
  "scoring_formula": "2*reuse_demand + 2*standardization + strategic_fit - customer_coupling - security_variance - maintenance_burden",
  "decision_thresholds": [
    {
      "decision": "PRODUCT",
      "minimum_score": 12,
      "maximum_score": 25
    },
    {
      "decision": "PLATFORM",
      "minimum_score": 8,
      "maximum_score": 11
    },
    {
      "decision": "CONFIGURATION",
      "minimum_score": 4,
      "maximum_score": 7
    },
    {
      "decision": "CUSTOM_EXTENSION",
      "minimum_score": -20,
      "maximum_score": 3
    }
  ],
  "overrides": {
    "RETIRE": "Use when lifecycle_status is retire regardless of score"
  },
  "decision_definitions": {
    "PRODUCT": "Versioned supported capability with a standard customer-facing contract and roadmap owner.",
    "PLATFORM": "Shared internal service or framework used by multiple deployments with platform ownership.",
    "CONFIGURATION": "Supported declarative variation that does not fork shared code.",
    "CUSTOM_EXTENSION": "Isolated customer-specific component with funding owner review date and no shared-core fork.",
    "RETIRE": "Remove or archive because value and reuse do not justify ongoing maintenance."
  },
  "portfolio_rules": [
    "No permanent customer-specific fork of shared product or platform code.",
    "Product and platform decisions require repeated demand and a named owner.",
    "Configuration must use a supported contract rather than copied source.",
    "Custom extensions require customer funding an isolation boundary and a dated review.",
    "Retirement must identify the dependency check and removal action."
  ],
  "review_cadence": "Quarterly portfolio review using deployment evidence support cost adoption and repeated demand",
  "accountable_roles": [
    {
      "role": "Forward Deployed Product Manager",
      "name": "Avery Chen"
    },
    {
      "role": "Platform Owner",
      "name": "Jordan Kim"
    },
    {
      "role": "Security Owner",
      "name": "Dana Brooks"
    },
    {
      "role": "Claims Solution Owner",
      "name": "Elena Ruiz"
    }
  ]
}
```

The policy rewards repeated demand, standardization, and strategic fit while penalizing customer coupling, security variance, and maintenance burden. A lifecycle override allows low-value work to be retired even when teams feel attached to it.

### Verification checkpoint

- **Expected result:** Six scoring dimensions, four score bands, a retirement override, five decision definitions, portfolio guardrails, and accountable roles are present.
- **Acceptable variation:** Weights may change with an explicit product strategy.
- **Failure indicator:** The policy equates every customer request with a product requirement or lacks rules for custom work and retirement.
- **Corrective action:** Restore evidence, ownership, maintenance, and lifecycle criteria.

## Step 3 — Build the Decision Matrix

Create `productization_matrix.csv`:

```csv
item_id,capability,reuse_demand,standardization,strategic_fit,customer_coupling,security_variance,maintenance_burden,lifecycle_status,proposed_decision,owner,evidence
P-01,Prompt-injection evaluation pack,5,5,5,1,2,2,active,PRODUCT,AI Quality Product Owner,Used by three regulated deployments with one versioned test contract
P-02,Effective-policy retrieval pattern,5,4,5,2,3,2,active,PRODUCT,Knowledge Platform Product Owner,Repeated effective-date and jurisdiction need across four insurers
P-03,Protected-action audit schema,5,5,5,1,2,2,active,PRODUCT,Security Product Owner,Shared identity evidence approval action and result contract
P-04,Enterprise identity adapter framework,4,4,5,3,4,3,active,PLATFORM,Identity Platform Owner,Reusable framework with customer-specific provider configuration
P-05,Claims decision workspace shell,4,3,4,4,3,3,active,PLATFORM,Claims Solution Platform Owner,Shared workflow shell with supported extension points
P-06,Tenant claim-field mapping,3,3,3,4,3,2,active,CONFIGURATION,Implementation Configuration Owner,Declarative mapping schema avoids customer code branches
P-07,Northstar legacy mainframe action adapter,1,2,2,5,5,5,active,CUSTOM_EXTENSION,Northstar Integration Owner,Customer funded and isolated with review date 2027-03-31
P-08,Pilot spreadsheet export,1,1,1,4,3,4,retire,RETIRE,Claims Solution Owner,No production dependency and archive after pilot evidence export
```

Score each dimension from 1 to 5 using deployment evidence. The proposed decision is reviewable because the raw scores, owner, and evidence remain beside it.

### Verification checkpoint

- **Expected result:** Eight unique assets represent shared evaluation, retrieval, audit, identity, workflow, configuration, custom integration, and retirement decisions.
- **Acceptable variation:** Add assets using the same schema and evidence standard.
- **Failure indicator:** A product candidate has no repeated demand, a custom extension has no review date, or retirement has no removal action.
- **Corrective action:** Change the evidence, lifecycle, or proposed decision; do not manipulate scores to protect sunk work.

## Step 4 — Create the Executable Portfolio Review

Create `productization_review.py`:

```python
#!/usr/bin/env python3
"""Evaluate productization and reusability decisions from portfolio evidence."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
POLICY_FILE = ROOT / "productization_policy.json"
MATRIX_FILE = ROOT / "productization_matrix.csv"
REPORT_FILE = ROOT / "productization_review.md"


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot load {path.name}: {exc}") from exc


def load_matrix(path: Path) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))
    except OSError as exc:
        raise ValueError(f"Cannot load {path.name}: {exc}") from exc


def score(item: dict[str, str]) -> int:
    return (
        2 * int(item["reuse_demand"])
        + 2 * int(item["standardization"])
        + int(item["strategic_fit"])
        - int(item["customer_coupling"])
        - int(item["security_variance"])
        - int(item["maintenance_burden"])
    )


def expected_decision(policy: dict[str, Any], item: dict[str, str], item_score: int) -> str:
    if item["lifecycle_status"] == "retire":
        return "RETIRE"
    for threshold in policy["decision_thresholds"]:
        if threshold["minimum_score"] <= item_score <= threshold["maximum_score"]:
            return threshold["decision"]
    raise ValueError(f"No decision threshold covers score {item_score}")


def validate(
    policy: dict[str, Any], rows: list[dict[str, str]]
) -> list[dict[str, Any]]:
    errors: list[str] = []
    required_sections = {
        "metadata", "scales", "scoring_formula", "decision_thresholds",
        "overrides", "decision_definitions", "portfolio_rules",
        "review_cadence", "accountable_roles",
    }
    missing = required_sections - set(policy)
    if missing:
        errors.append("Missing policy sections: " + ", ".join(sorted(missing)))

    expected_columns = {
        "item_id", "capability", "reuse_demand", "standardization",
        "strategic_fit", "customer_coupling", "security_variance",
        "maintenance_burden", "lifecycle_status", "proposed_decision",
        "owner", "evidence",
    }
    if rows and set(rows[0]) != expected_columns:
        errors.append("Decision-matrix columns do not match the required schema")
    ids = [item.get("item_id") for item in rows]
    if not ids or len(ids) != len(set(ids)):
        errors.append("Item IDs must be present and unique")

    reviewed: list[dict[str, Any]] = []
    allowed_decisions = set(policy.get("decision_definitions", {}))
    for item in rows:
        try:
            numeric_values = [
                int(item[field])
                for field in [
                    "reuse_demand", "standardization", "strategic_fit",
                    "customer_coupling", "security_variance", "maintenance_burden",
                ]
            ]
        except (KeyError, TypeError, ValueError):
            errors.append(f"{item.get('item_id')} contains invalid scoring data")
            continue
        if any(value not in range(1, 6) for value in numeric_values):
            errors.append(f"{item['item_id']} scores must be integers 1 through 5")
        item_score = score(item)
        calculated = expected_decision(policy, item, item_score)
        if item.get("proposed_decision") not in allowed_decisions:
            errors.append(f"{item['item_id']} has an unsupported decision")
        if item.get("proposed_decision") != calculated:
            errors.append(
                f"{item['item_id']} proposes {item.get('proposed_decision')} "
                f"but the policy calculates {calculated}"
            )
        if not item.get("owner") or not item.get("evidence"):
            errors.append(f"{item['item_id']} needs an owner and evidence")
        if calculated == "CUSTOM_EXTENSION" and "review date" not in item["evidence"].lower():
            errors.append(f"{item['item_id']} custom extension needs a dated review")
        if calculated == "RETIRE" and "archive" not in item["evidence"].lower():
            errors.append(f"{item['item_id']} retirement needs a removal or archive action")
        if calculated in {"PRODUCT", "PLATFORM"} and int(item["reuse_demand"]) < 4:
            errors.append(f"{item['item_id']} lacks repeated demand for {calculated}")
        reviewed.append({**item, "score": item_score, "calculated_decision": calculated})

    if errors:
        raise ValueError("\n".join(f"- {error}" for error in errors))
    return reviewed


def build_report(
    policy: dict[str, Any], reviewed: list[dict[str, Any]], decision: str
) -> str:
    counts = Counter(item["calculated_decision"] for item in reviewed)
    lines = [
        "# Enterprise AI Claims Assistant — Productization and Reusability Review", "",
        f"- **Decision:** {decision}",
        f"- **Scope:** {policy['metadata']['portfolio_scope']}", "",
        "## Decision Matrix", "",
        "| Item | Capability | Score | Decision | Owner |",
        "| --- | --- | ---: | --- | --- |",
    ]
    for item in sorted(reviewed, key=lambda row: row["score"], reverse=True):
        lines.append(
            f"| {item['item_id']} | {item['capability']} | {item['score']} | "
            f"{item['calculated_decision']} | {item['owner']} |"
        )
    lines.extend(["", "## Portfolio Mix", ""])
    for label in ["PRODUCT", "PLATFORM", "CONFIGURATION", "CUSTOM_EXTENSION", "RETIRE"]:
        lines.append(f"- {label}: {counts.get(label, 0)}")
    lines.extend(["", "## Decision Definitions", ""])
    for label, definition in policy["decision_definitions"].items():
        lines.append(f"- **{label}:** {definition}")
    lines.extend(["", "## Guardrails", ""])
    lines.extend(f"- {rule}" for rule in policy["portfolio_rules"])
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    try:
        policy = load_json(POLICY_FILE)
        rows = load_matrix(MATRIX_FILE)
        reviewed = validate(policy, rows)
        decision = "PORTFOLIO_PLAN_APPROVED"
        REPORT_FILE.write_text(build_report(policy, reviewed, decision), encoding="utf-8")
    except (KeyError, TypeError, ValueError) as exc:
        print(f"LAB 09 FAILED\n{exc}")
        return 1

    counts = Counter(item["calculated_decision"] for item in reviewed)
    print("LAB 09 PASSED")
    print(f"- Decision: {decision}")
    print(f"- Components reviewed: {len(reviewed)}")
    print(f"- Product candidates: {counts['PRODUCT']}")
    print(f"- Platform candidates: {counts['PLATFORM']}")
    print(f"- Custom extensions: {counts['CUSTOM_EXTENSION']}")
    print(f"- Retirements: {counts['RETIRE']}")
    print(f"- Report: {REPORT_FILE.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

The code calculates every score, applies the configured thresholds and retirement override, validates proposed decisions and portfolio guardrails, then generates the review.

### Verification checkpoint

- **Expected result:** The script derives decisions from evidence rather than trusting the CSV label.
- **Acceptable variation:** Add dimensions only if the policy and code remain synchronized.
- **Failure indicator:** A manual label can bypass the score or a permanent customer fork is treated as normal productization.
- **Corrective action:** Restore calculated decisions and custom-extension guardrails.

## Step 5 — Run and Inspect the Matrix

```bash
python3 -m py_compile productization_review.py
python3 productization_review.py
```

Expected output:

```text
LAB 09 PASSED
- Decision: PORTFOLIO_PLAN_APPROVED
- Components reviewed: 8
- Product candidates: 3
- Platform candidates: 2
- Custom extensions: 1
- Retirements: 1
- Report: productization_review.md
```

Inspect the generated review:

```bash
sed -n '1,240p' productization_review.md
```

On Windows PowerShell:

```powershell
Get-Content productization_review.md
```

### Verification checkpoint

- **Expected result:** The portfolio mix contains 3 product, 2 platform, 1 configuration, 1 custom-extension, and 1 retirement decision.
- **Acceptable variation:** Another real portfolio may produce a different mix when the evidence supports it.
- **Failure indicator:** The script prints `LAB 09 FAILED` or a proposed decision differs from the calculated policy.
- **Corrective action:** Review the named dimensions and evidence, then correct the proposal or policy transparently.

## Step 6 — Conduct the Product Review

Answer from the matrix:

1. Which product candidate has the strongest repeated demand?
2. Which platform asset should not become a customer-facing product?
3. What prevents configuration from turning into copied customer code?
4. What evidence must exist before renewing the custom extension?
5. Why is retirement a positive portfolio decision?

### Verification checkpoint

- **Expected result:** Each answer cites scores, evidence, ownership, or guardrails.
- **Acceptable variation:** Recommend a proof period before committing to productization.
- **Failure indicator:** Decisions rely only on a strategic customer's request.
- **Corrective action:** Add cross-deployment evidence, cost, coupling, and maintenance consequences.

## Step 7 — Commit Your Evidence

```bash
git init -b main
git add .gitignore productization_policy.json productization_matrix.csv productization_review.py productization_review.md
git commit -m "Complete productization and reusability decision matrix"
git status --short --branch
```

### Verification checkpoint

- **Expected result:** `main` is clean.
- **Acceptable variation:** Another descriptive commit message is acceptable.
- **Failure indicator:** The generated review is missing or caches are tracked.
- **Corrective action:** Rerun the review, stage the intended five project files, and commit.

## Map the Completed Workflow

1. Define a portfolio scoring policy and decision meanings.
2. Collect deployment evidence for reusable and customer-specific assets.
3. Score reuse demand, standardization, strategic fit, coupling, security variance, and maintenance.
4. Calculate product, platform, configuration, custom-extension, or retirement decisions.
5. Apply ownership, no-fork, custom-review, and retirement guardrails.
6. Review the portfolio mix and fund the next evidence.
7. Repeat the review quarterly using actual reuse and support data.

## Troubleshooting Cheatsheet

| Symptom | Likely cause | Corrective action |
| --- | --- | --- |
| Invalid schema | CSV headers changed | Restore the documented columns |
| Score out of range | A dimension is not 1–5 | Correct the evidence score |
| Decision mismatch | Proposed label differs from calculated policy | Review evidence or transparently revise policy |
| Weak product evidence | Reuse demand is below 4 | Keep it configuration or custom until repeated demand exists |
| Unsafe custom work | No owner isolation or review date | Hold the extension decision |
| Retirement failure | No archive or removal action | Record dependency check and disposal action |
| Stale review | Inputs changed | Rerun `python3 productization_review.py` |

## Cleanup

```bash
python3 -c "import shutil; shutil.rmtree('__pycache__', ignore_errors=True)"
```

Keep the four learner artifacts, `.gitignore`, and Git history.

## Completion Check

- [ ] I defined the scoring policy and decision meanings.
- [ ] I scored all eight assets using evidence.
- [ ] I distinguished product platform and configuration.
- [ ] I protected shared code from customer-specific forks.
- [ ] I gave the custom extension an owner and review date.
- [ ] I recorded a retirement action.
- [ ] I generated and reviewed `productization_review.md`.
- [ ] I committed a clean repository.

## Reflection

1. Which asset is most likely to be over-productized and why?
2. What real reuse evidence would change a configuration decision into product?
3. Which maintenance burden is currently understated?
