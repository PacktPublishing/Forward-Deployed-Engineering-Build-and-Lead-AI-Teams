# Lab 10 — Design a Forward Deployed Organization and Staffing Model

## Goal

Design a forward deployed organization that can staff multiple customer engagements without hero culture, hidden specialist bottlenecks, or unclear decision rights. Model persistent capability groups, temporary deployment pods, portfolio demand, backup ownership, utilization guardrails, governance, career levels, and scaling triggers.

Build the project independently in a new directory. The completed reference repository is a comparison aid, not the learner workspace.

## What You'll Build or Produce

- `organization_model.json` — topology, role capacity, rules, governance, decision rights, scaling triggers, anti-hero controls, and career levels.
- `engagement_portfolio.csv` — four prioritized engagements with phase, risk, ownership, and seven-role FTE demand.
- `staffing_model.py` — the executable capacity and coverage review.
- `staffing_plan.md` — the generated portfolio staffing recommendation.
- `.gitignore` — Git hygiene.

## Estimated Time

75–100 minutes.

## Cost Guardrails

This exercise runs locally with Python's standard library. It creates no external services or cost.

## Completion Evidence

- `python3 -m py_compile staffing_model.py` succeeds.
- `python3 staffing_model.py` prints `LAB 10 PASSED` and `PORTFOLIO_STAFFED_WITH_GUARDRAILS`.
- Four engagements have priority, phase, risk, DRI, backup DRI, and role allocations.
- Seven role pools stay below their target utilization.
- Phase and high-risk coverage rules pass.
- Five decision domains and at least five scaling and anti-hero controls exist.
- `staffing_plan.md` exposes capacity and specialist pressure.
- Git is clean on `main`.

## Prerequisites

- Python 3.10 or later
- Git
- A text editor
- Familiarity with cross-functional teams, FTE capacity, delivery phases, and organizational decision rights
- Awareness of the claims-assistant deployment plus other realistic concurrent portfolio demands.

## Where This Lab Fits

This final lab scales the operating model across several customer engagements. It combines lessons from delivery, security, adoption, and productization to allocate scarce roles, protect backup ownership, expose bottlenecks, and trigger hiring or reprioritization. The result is an organization designed to repeat outcomes without hero culture.

## Step 1 — Create Your Project

```bash
mkdir lab_10_forward_deployed_organization_staffing_model
cd lab_10_forward_deployed_organization_staffing_model
```

Create `.gitignore`:

```gitignore
__pycache__/
*.py[cod]
.DS_Store
```

### Verification checkpoint

- **Expected result:** Only `.gitignore` exists in your learner-owned directory.
- **Acceptable variation:** Another directory name is acceptable.
- **Failure indicator:** You are editing the completed reference repository.
- **Corrective action:** Create a separate directory and continue there.

## Step 2 — Design the Organization Model

Create `organization_model.json`:

```json
{
  "metadata": {
    "lab_id": "lab_10",
    "organization": "Northstar Forward Deployed AI Practice",
    "case_anchor": "Enterprise AI Claims Assistant",
    "planning_horizon": "Q4 2026 portfolio",
    "review_date": "2026-08-16"
  },
  "operating_model": {
    "topology": "Persistent capability groups staff temporary cross-functional deployment pods.",
    "deployment_pod": [
      "Forward Deployed Engineer",
      "AI Engineer",
      "Platform Engineer",
      "Product Partner",
      "Technical Deployment Lead"
    ],
    "shared_specialists": [
      "Forward Deployed Architect",
      "Security Engineer"
    ],
    "leadership_layers": [
      {
        "layer": "Engagement",
        "accountability": "Customer outcome scope delivery and operational transition",
        "owner": "Technical Deployment Lead"
      },
      {
        "layer": "Technical",
        "accountability": "Architecture quality security and reusable engineering decisions",
        "owner": "Principal FDE"
      },
      {
        "layer": "Portfolio",
        "accountability": "Capacity prioritization specialist allocation and escalation",
        "owner": "FDE Director"
      }
    ]
  },
  "roles": [
    {
      "id": "fde",
      "title": "Forward Deployed Engineer",
      "available_fte": 8,
      "max_target_utilization_percent": 90,
      "accountabilities": [
        "End-to-end customer solution",
        "Integration and evidence",
        "Customer technical ownership"
      ]
    },
    {
      "id": "ai",
      "title": "AI Engineer",
      "available_fte": 5,
      "max_target_utilization_percent": 90,
      "accountabilities": [
        "Models retrieval evaluation and guardrails",
        "AI quality evidence"
      ]
    },
    {
      "id": "architect",
      "title": "Forward Deployed Architect",
      "available_fte": 3,
      "max_target_utilization_percent": 90,
      "accountabilities": [
        "Cross-system architecture",
        "Trade-offs and design governance"
      ]
    },
    {
      "id": "platform",
      "title": "Platform Engineer",
      "available_fte": 4,
      "max_target_utilization_percent": 90,
      "accountabilities": [
        "Environments delivery reliability and observability"
      ]
    },
    {
      "id": "security",
      "title": "Security Engineer",
      "available_fte": 3,
      "max_target_utilization_percent": 90,
      "accountabilities": [
        "Threat model access data protection and release approval"
      ]
    },
    {
      "id": "product",
      "title": "Product Partner",
      "available_fte": 3,
      "max_target_utilization_percent": 90,
      "accountabilities": [
        "Discovery adoption value and product feedback"
      ]
    },
    {
      "id": "delivery",
      "title": "Technical Deployment Lead",
      "available_fte": 3,
      "max_target_utilization_percent": 90,
      "accountabilities": [
        "Integrated plan decisions risks cutover and handoff"
      ]
    }
  ],
  "staffing_rules": [
    "Every engagement has a named DRI and a different backup DRI.",
    "Risk level 5 requires at least 0.5 architect FTE and 0.5 security FTE.",
    "Go-live requires at least 1.0 platform FTE and 0.5 delivery FTE.",
    "Discovery requires at least 1.0 FDE FTE and 0.5 product FTE.",
    "Pilot requires at least 1.0 AI FTE and 0.5 platform FTE.",
    "No role pool may exceed its target utilization."
  ],
  "governance": [
    {
      "cadence": "Weekly portfolio staffing review",
      "owner": "FDE Director",
      "decisions": [
        "Priority changes",
        "Specialist conflicts",
        "Hiring or contractor trigger"
      ]
    },
    {
      "cadence": "Weekly architecture and security council",
      "owner": "Principal FDE",
      "decisions": [
        "Design exceptions",
        "Security risk acceptance",
        "Reusable pattern approval"
      ]
    },
    {
      "cadence": "Biweekly talent review",
      "owner": "FDE Manager",
      "decisions": [
        "Coaching load",
        "Backup coverage",
        "Career evidence and rotations"
      ]
    }
  ],
  "decision_rights": [
    {
      "decision": "Engagement priority",
      "dri": "FDE Director",
      "approver": "Executive Portfolio Sponsor"
    },
    {
      "decision": "Technical standard",
      "dri": "Principal FDE",
      "approver": "Architecture Council"
    },
    {
      "decision": "Security exception",
      "dri": "Security Lead",
      "approver": "Chief Information Security Officer"
    },
    {
      "decision": "Staff reassignment",
      "dri": "FDE Director",
      "approver": "Affected Engagement Sponsors"
    },
    {
      "decision": "Hiring trigger",
      "dri": "FDE Director",
      "approver": "Business Unit Leader"
    }
  ],
  "scaling_triggers": [
    {
      "trigger": "Any role exceeds 85 percent utilization for two planning cycles",
      "action": "Open capacity plan and reduce uncommitted scope"
    },
    {
      "trigger": "A shared specialist becomes the sole qualified owner for two or more critical engagements",
      "action": "Assign a shadow and create a dated capability transfer plan"
    },
    {
      "trigger": "Security or architecture review wait exceeds 10 business days",
      "action": "Add reviewer capacity or narrow concurrent high-risk work"
    },
    {
      "trigger": "More than two engagements enter go-live or hypercare together",
      "action": "Create a temporary command-center rotation and executive priority review"
    },
    {
      "trigger": "Reusable work exceeds 30 percent of delivery effort",
      "action": "Fund a dedicated product or platform workstream"
    }
  ],
  "anti_hero_controls": [
    "Primary and backup DRI on every engagement",
    "Decision and runbook artifacts stored in shared repositories",
    "Observed handoffs before role rotation",
    "Shared on-call and review rotations",
    "No critical approval dependent on one person"
  ],
  "career_levels": [
    {
      "level": "FDE",
      "evidence": "Delivers a bounded workstream with support"
    },
    {
      "level": "Senior FDE",
      "evidence": "Owns an engagement slice and customer decisions"
    },
    {
      "level": "Principal FDE",
      "evidence": "Sets technical direction across engagements and develops specialists"
    },
    {
      "level": "FDE Manager",
      "evidence": "Builds capability capacity and consistent delivery systems"
    }
  ]
}
```

The topology keeps reusable capability in persistent role groups while forming temporary customer pods. Decision rights, scaling triggers, backups, and shared artifacts prevent a single heroic person from becoming the operating model.

### Verification checkpoint

- **Expected result:** Seven role pools, engagement/technical/portfolio leadership, staffing rules, three governance cadences, five decisions, five scaling triggers, five anti-hero controls, and four career levels are present.
- **Acceptable variation:** Capacity may reflect another organization if role accountabilities and utilization limits remain explicit.
- **Failure indicator:** The model is only an org chart and says nothing about capacity, decisions, specialist allocation, or knowledge transfer.
- **Corrective action:** Add operating rules, measurable triggers, accountable decisions, and resilience controls.

## Step 3 — Create the Engagement Portfolio

Create `engagement_portfolio.csv`:

```csv
engagement_id,customer,phase,priority,complexity,risk,region,dri,backup_dri,fde_fte,ai_fte,architect_fte,platform_fte,security_fte,product_fte,delivery_fte
E-01,Northstar Mutual Claims Assistant,go_live,1,5,5,US,Sam Rivera,Alex Morgan,2.0,1.0,0.5,1.0,0.5,0.5,0.5
E-02,Summit Bank Knowledge Agent,design,2,5,5,US and EU,Nora Patel,Diego Lee,1.0,1.0,1.0,0.5,1.0,0.5,0.5
E-03,Meridian Pharma Compliance Assistant,discovery,3,4,5,US and EU,Jamie Chen,Riley Brooks,1.0,0.5,0.5,0.0,0.5,0.5,0.5
E-04,Harbor Retail Service Copilot,pilot,4,3,3,US,Taylor Singh,Casey Grant,2.0,1.5,0.5,1.0,0.5,0.5,0.5
```

Fractional FTE expresses planned capacity rather than named full-time assignment. Primary and backup DRIs preserve engagement continuity while role allocations reveal portfolio tradeoffs.

### Verification checkpoint

- **Expected result:** Four unique engagements cover discovery, design, pilot, and go-live with priorities 1–4.
- **Acceptable variation:** Add engagements using the same schema and phase rules.
- **Failure indicator:** An engagement has the same primary and backup, a high-risk engagement lacks architecture/security, or phase coverage is absent.
- **Corrective action:** Add qualified coverage, change scope or sequencing, or reduce concurrency.

## Step 4 — Build the Executable Staffing Review

Create `staffing_model.py`:

```python
#!/usr/bin/env python3
"""Validate a forward deployed organization and portfolio staffing model."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
MODEL_FILE = ROOT / "organization_model.json"
PORTFOLIO_FILE = ROOT / "engagement_portfolio.csv"
REPORT_FILE = ROOT / "staffing_plan.md"

FTE_FIELDS = [
    "fde_fte", "ai_fte", "architect_fte", "platform_fte",
    "security_fte", "product_fte", "delivery_fte",
]


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot load {path.name}: {exc}") from exc


def load_portfolio(path: Path) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))
    except OSError as exc:
        raise ValueError(f"Cannot load {path.name}: {exc}") from exc


def validate(
    model: dict[str, Any], rows: list[dict[str, str]]
) -> tuple[dict[str, float], dict[str, float]]:
    errors: list[str] = []
    required_sections = {
        "metadata", "operating_model", "roles", "staffing_rules",
        "governance", "decision_rights", "scaling_triggers",
        "anti_hero_controls", "career_levels",
    }
    missing = required_sections - set(model)
    if missing:
        errors.append("Missing organization sections: " + ", ".join(sorted(missing)))

    role_index = {item.get("id"): item for item in model.get("roles", [])}
    expected_role_ids = {field.removesuffix("_fte") for field in FTE_FIELDS}
    if set(role_index) != expected_role_ids:
        errors.append("Organization roles must match the seven staffing fields")
    if len(role_index) != len(model.get("roles", [])):
        errors.append("Role IDs must be unique")

    expected_columns = {
        "engagement_id", "customer", "phase", "priority", "complexity", "risk",
        "region", "dri", "backup_dri", *FTE_FIELDS,
    }
    if rows and set(rows[0]) != expected_columns:
        errors.append("Engagement-portfolio columns do not match the required schema")
    engagement_ids = [item.get("engagement_id") for item in rows]
    priorities = [item.get("priority") for item in rows]
    if not engagement_ids or len(engagement_ids) != len(set(engagement_ids)):
        errors.append("Engagement IDs must be present and unique")
    if len(priorities) != len(set(priorities)):
        errors.append("Portfolio priorities must be unique")

    demand = {role_id: 0.0 for role_id in expected_role_ids}
    allowed_phases = {"discovery", "design", "build", "pilot", "go_live", "hypercare"}
    for item in rows:
        try:
            complexity = int(item["complexity"])
            risk = int(item["risk"])
            int(item["priority"])
            allocation = {field: float(item[field]) for field in FTE_FIELDS}
        except (KeyError, TypeError, ValueError):
            errors.append(f"{item.get('engagement_id')} has invalid numeric values")
            continue
        if item.get("phase") not in allowed_phases:
            errors.append(f"{item['engagement_id']} has an unsupported phase")
        if complexity not in range(1, 6) or risk not in range(1, 6):
            errors.append(f"{item['engagement_id']} complexity and risk must be 1 through 5")
        if not item.get("dri") or not item.get("backup_dri") or item["dri"] == item["backup_dri"]:
            errors.append(f"{item['engagement_id']} needs different primary and backup DRIs")
        if any(value < 0 for value in allocation.values()):
            errors.append(f"{item['engagement_id']} has negative staffing")
        for field, value in allocation.items():
            demand[field.removesuffix("_fte")] += value
        if risk == 5 and (allocation["architect_fte"] < 0.5 or allocation["security_fte"] < 0.5):
            errors.append(f"{item['engagement_id']} high risk lacks architecture or security coverage")
        if item["phase"] == "go_live" and (allocation["platform_fte"] < 1.0 or allocation["delivery_fte"] < 0.5):
            errors.append(f"{item['engagement_id']} go-live coverage is incomplete")
        if item["phase"] == "discovery" and (allocation["fde_fte"] < 1.0 or allocation["product_fte"] < 0.5):
            errors.append(f"{item['engagement_id']} discovery coverage is incomplete")
        if item["phase"] == "pilot" and (allocation["ai_fte"] < 1.0 or allocation["platform_fte"] < 0.5):
            errors.append(f"{item['engagement_id']} pilot coverage is incomplete")

    utilization: dict[str, float] = {}
    for role_id, role in role_index.items():
        capacity = float(role.get("available_fte", 0))
        target = float(role.get("max_target_utilization_percent", 0))
        if capacity <= 0 or not (0 < target <= 100):
            errors.append(f"{role_id} has invalid capacity or target")
            continue
        utilization[role_id] = round(100 * demand[role_id] / capacity, 2)
        if utilization[role_id] > target:
            errors.append(
                f"{role['title']} utilization {utilization[role_id]:.1f}% "
                f"exceeds target {target:.1f}%"
            )
        if not role.get("accountabilities"):
            errors.append(f"{role['title']} lacks accountabilities")

    required_decisions = {
        "Engagement priority", "Technical standard", "Security exception",
        "Staff reassignment", "Hiring trigger",
    }
    if {item.get("decision") for item in model.get("decision_rights", [])} != required_decisions:
        errors.append("Organization decision rights are incomplete")
    if len(model.get("scaling_triggers", [])) < 5:
        errors.append("At least five scaling triggers are required")
    if len(model.get("anti_hero_controls", [])) < 5:
        errors.append("Anti-hero controls are incomplete")

    if errors:
        raise ValueError("\n".join(f"- {error}" for error in errors))
    return demand, utilization


def build_report(
    model: dict[str, Any],
    rows: list[dict[str, str]],
    demand: dict[str, float],
    utilization: dict[str, float],
    decision: str,
) -> str:
    role_index = {item["id"]: item for item in model["roles"]}
    lines = [
        "# Forward Deployed Organization and Staffing Plan", "",
        f"- **Decision:** {decision}",
        f"- **Planning horizon:** {model['metadata']['planning_horizon']}",
        f"- **Topology:** {model['operating_model']['topology']}", "",
        "## Engagement Portfolio", "",
        "| Priority | Engagement | Phase | DRI | Backup | Risk |",
        "| ---: | --- | --- | --- | --- | ---: |",
    ]
    for item in sorted(rows, key=lambda row: int(row["priority"])):
        lines.append(
            f"| {item['priority']} | {item['customer']} | {item['phase']} | "
            f"{item['dri']} | {item['backup_dri']} | {item['risk']} |"
        )
    lines.extend(["", "## Capacity by Role", "", "| Role | Demand FTE | Available FTE | Utilization | Target |", "| --- | ---: | ---: | ---: | ---: |"])
    for role in model["roles"]:
        role_id = role["id"]
        lines.append(
            f"| {role['title']} | {demand[role_id]:.1f} | "
            f"{float(role['available_fte']):.1f} | {utilization[role_id]:.1f}% | "
            f"{float(role['max_target_utilization_percent']):.1f}% |"
        )
    lines.extend(["", "## Scaling Triggers", ""])
    for item in model["scaling_triggers"]:
        lines.append(f"- **Trigger:** {item['trigger']} **Action:** {item['action']}")
    lines.extend(["", "## Anti-Hero Controls", ""])
    lines.extend(f"- {item}" for item in model["anti_hero_controls"])
    lines.extend(["", "## Governance", ""])
    for item in model["governance"]:
        lines.append(f"- {item['cadence']} — {item['owner']}: {', '.join(item['decisions'])}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    try:
        model = load_json(MODEL_FILE)
        rows = load_portfolio(PORTFOLIO_FILE)
        demand, utilization = validate(model, rows)
        decision = "PORTFOLIO_STAFFED_WITH_GUARDRAILS"
        REPORT_FILE.write_text(
            build_report(model, rows, demand, utilization, decision),
            encoding="utf-8",
        )
    except (KeyError, TypeError, ValueError) as exc:
        print(f"LAB 10 FAILED\n{exc}")
        return 1

    role_index = {item["id"]: item for item in model["roles"]}
    peak_role = max(utilization, key=utilization.get)
    print("LAB 10 PASSED")
    print(f"- Decision: {decision}")
    print(f"- Engagements staffed: {len(rows)}")
    print(f"- Role pools: {len(role_index)}")
    print(f"- Peak utilization: {role_index[peak_role]['title']} {utilization[peak_role]:.1f}%")
    print("- Overallocated roles: 0")
    print(f"- Report: {REPORT_FILE.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

The program validates organization completeness, portfolio schema, phase-specific staffing, high-risk specialist coverage, primary/backup ownership, decision rights, anti-hero controls, and role utilization before generating the plan.

### Verification checkpoint

- **Expected result:** Demand is summed across all engagements and compared with each role's available FTE and target utilization.
- **Acceptable variation:** Add a new role only when the JSON, CSV, validation, and guide all teach it.
- **Failure indicator:** Staffing is approved engagement by engagement while the total portfolio overallocates a shared specialist.
- **Corrective action:** Reprioritize, reduce scope, delay work, cross-train, or add capacity before approval.

## Step 5 — Run and Inspect the Staffing Model

```bash
python3 -m py_compile staffing_model.py
python3 staffing_model.py
```

Expected output:

```text
LAB 10 PASSED
- Decision: PORTFOLIO_STAFFED_WITH_GUARDRAILS
- Engagements staffed: 4
- Role pools: 7
- Peak utilization: Forward Deployed Architect 83.3%
- Overallocated roles: 0
- Report: staffing_plan.md
```

Inspect the generated plan:

```bash
sed -n '1,260p' staffing_plan.md
```

On Windows PowerShell:

```powershell
Get-Content staffing_plan.md
```

### Verification checkpoint

- **Expected result:** All role pools remain below 90 percent; architecture and security pressure are visible instead of hidden.
- **Acceptable variation:** A real portfolio may correctly fail when demand exceeds capacity.
- **Failure indicator:** The script prints `LAB 10 FAILED`, an engagement lacks coverage, or a role exceeds its target.
- **Corrective action:** Apply the relevant scaling trigger or change portfolio priority and rerun.

## Step 6 — Conduct the Portfolio Staffing Review

Answer from the plan:

1. Which role becomes the first scaling constraint?
2. Which engagement should retain scarce security or architecture capacity?
3. What work can be standardized or productized to reduce future staffing demand?
4. Who owns the decision to reassign staff?
5. Which backup or capability-transfer action prevents a single-person dependency?

### Verification checkpoint

- **Expected result:** Each answer cites utilization, priority, risk, decision rights, or a scaling trigger.
- **Acceptable variation:** Recommend hiring, contracting, rotations, or scope reduction when evidence supports it.
- **Failure indicator:** Every engagement is treated as equally urgent or specialists are allocated by informal escalation.
- **Corrective action:** Use explicit priorities, decision rights, and portfolio-wide capacity evidence.

## Step 7 — Commit Your Evidence

```bash
git init -b main
git add .gitignore organization_model.json engagement_portfolio.csv staffing_model.py staffing_plan.md
git commit -m "Complete forward deployed organization and staffing model"
git status --short --branch
```

### Verification checkpoint

- **Expected result:** `main` is clean.
- **Acceptable variation:** Another descriptive commit message is acceptable.
- **Failure indicator:** The generated plan is absent or caches are tracked.
- **Corrective action:** Rerun the staffing model, stage the intended five project files, and commit.

## Map the Completed Workflow

1. Choose a capability-group and deployment-pod topology.
2. Define role capacity, accountabilities, and utilization guardrails.
3. Prioritize concurrent engagements by phase, complexity, and risk.
4. Allocate fractional FTE with primary and backup ownership.
5. Validate phase coverage and shared-specialist capacity across the portfolio.
6. Apply governance, decision rights, scaling triggers, and anti-hero controls.
7. Review career and capability investments as part of portfolio planning.

## Troubleshooting Cheatsheet

| Symptom | Likely cause | Corrective action |
| --- | --- | --- |
| Role mismatch | JSON roles and CSV FTE columns differ | Synchronize the seven documented roles |
| Duplicate priority | Two engagements compete without an explicit order | Assign unique portfolio priorities |
| Missing backup | DRI and backup are blank or identical | Assign a qualified different backup |
| High-risk coverage failure | Architecture or security is below 0.5 FTE | Add capacity narrow scope or delay |
| Phase coverage failure | Discovery pilot or go-live lacks required roles | Add the named role allocation |
| Overallocated role | Total demand exceeds target utilization | Reprioritize cross-train hire contract or reduce scope |
| Stale plan | Inputs changed | Rerun `python3 staffing_model.py` |

## Cleanup

```bash
python3 -c "import shutil; shutil.rmtree('__pycache__', ignore_errors=True)"
```

Keep the four learner-built artifacts, `.gitignore`, and Git history.

## Completion Check

- [ ] I chose an operating topology.
- [ ] I defined seven role pools and accountabilities.
- [ ] I prioritized four concurrent engagements.
- [ ] I assigned different primary and backup DRIs.
- [ ] I applied phase and high-risk coverage rules.
- [ ] I kept all role pools below target utilization.
- [ ] I defined governance decisions scaling triggers and anti-hero controls.
- [ ] I generated and reviewed `staffing_plan.md`.
- [ ] I committed a clean repository.

## Reflection

1. Which capacity constraint should trigger hiring rather than reprioritization?
2. What capability should be cross-trained first?
3. How would the topology change after the portfolio doubles?
