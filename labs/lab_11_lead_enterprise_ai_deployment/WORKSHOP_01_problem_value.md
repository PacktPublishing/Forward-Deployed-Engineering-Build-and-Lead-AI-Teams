# Capstone Workshop 1 — Frame the Customer Problem and Value Case

## Goal

Start one shared capstone project for Northstar Mutual's Enterprise AI Claims Assistant. Define the customer problem, measurable business outcome, discovery evidence, owned assumptions, and value hypothesis before selecting technology or promising a rollout.

Build in your own project directory. The completed course repository is a reference you consult only when you are stuck or comparing your result.

## What You'll Build or Produce

- `.gitignore` — Git hygiene for the shared capstone project.
- `problem_value.json` — the problem, baseline, scope, non-goals, discovery evidence, assumptions, and value calculation contract.
- The first Git commit in the project you will continue through Workshops 2–5.

## Estimated Time

35–50 minutes.

## Cost Guardrails

This workshop runs locally with Python's standard library. It creates no external services or cost.

## Completion Evidence

- `python3 -m json.tool problem_value.json` succeeds.
- The problem names a user, observable friction, and three baseline measures.
- The outcome is measurable and constrained by three explicit non-goals.
- Discovery evidence is separated from assumptions, and every assumption has an owner and test.
- The value hypothesis includes a benefit formula and financial assumptions.
- Git is clean after the Workshop 1 commit.

## Prerequisites

- Python 3.10 or later
- Git
- A text editor
- Familiarity with customer discovery, workflow baselines, business outcomes, and value hypotheses

## Where This Workshop Fits

This workshop combines the first two capstone lectures: **Define the Customer Problem and Business Outcome** and **Create the Discovery Brief and Value Hypothesis**. Its output becomes the decision contract for every later workshop.

## Step 1 — Create the Shared Capstone Project

```bash
mkdir lab_11_lead_enterprise_ai_deployment
cd lab_11_lead_enterprise_ai_deployment
```

Create `.gitignore`:

```gitignore
__pycache__/
*.py[cod]
.DS_Store
```

### Verification checkpoint

- **Expected result:** Only `.gitignore` exists in your learner-owned directory.
- **Acceptable variation:** You may use a different directory name.
- **Failure indicator:** You are editing the completed reference repository.
- **Corrective action:** Create a new empty directory and continue there.

## Step 2 — Define the Problem and Business Outcome

Create `problem_value.json`:

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
  "customer_problem": {
    "primary_user": "Licensed Claims Adjuster",
    "problem_statement": "Adjusters spend too much time assembling evidence-linked claim summaries across fragmented systems, causing slow handling, rework, and incomplete audit evidence.",
    "baseline": {
      "average_handling_minutes": 42,
      "rework_rate_percent": 14,
      "quality_score_percent": 86
    },
    "business_outcome": "Reduce handling time and rework while improving quality and citation completeness without allowing unauthorized protected actions.",
    "scope": "Retrieve effective policy evidence, produce a cited summary, and recommend request_evidence, continue_review, or escalate.",
    "non_goals": [
      "Autonomously approve or deny a claim",
      "Authorize payment or change reserves",
      "Send customer communication or update the claims system without human approval"
    ]
  },
  "discovery_and_value": {
    "evidence": [
      "Workflow interviews with licensed adjusters",
      "Four-week bounded pilot with 25 adjusters",
      "Reviewed evaluation set segmented by claim type and failure mode",
      "Security, recovery, and human-approval drills"
    ],
    "assumptions": [
      {
        "assumption": "Effective-date and jurisdiction metadata remain complete for each rollout wave.",
        "owner": "Claims Data Lead",
        "test": "Block a jurisdiction when policy metadata coverage is below 100 percent."
      },
      {
        "assumption": "Licensed adjusters retain decision authority and review cited evidence.",
        "owner": "Claims Operations Lead",
        "test": "Monitor acceptance, overrides, approval identity, and audit completeness weekly."
      }
    ],
    "value_hypothesis": {
      "statement": "If adjusters receive a source-linked summary and a bounded recommendation inside their workflow, then average handling time and rework will fall without reducing quality or safety.",
      "benefit_formula": "time_saved_hours * loaded_adjuster_hourly_cost_usd + avoided_rework_count * avoided_rework_value_usd",
      "loaded_adjuster_hourly_cost_usd": 85,
      "avoided_rework_value_usd": 120
    }
  }
}
```

Read the `customer_problem` section as a decision contract:

- The primary user is a licensed claims adjuster.
- The baseline measures time, rework, and quality before AI assistance.
- The assistant is bounded to cited summaries and three allowed recommendations.
- Claim adjudication, payments, reserves, customer communication, and unapproved system writes remain outside the assistant's authority.

### Verification checkpoint

- **Expected result:** The problem, baseline, outcome, scope, and non-goals describe one coherent workflow decision.
- **Acceptable variation:** You may rewrite the problem statement while preserving the measurable baseline and protected-action boundary.
- **Failure indicator:** The outcome is “deploy AI,” the primary user is missing, or autonomous claim decisions enter scope.
- **Corrective action:** Restate the user problem, measurable result, smallest valuable scope, and explicit non-goals.

## Step 3 — Test the Discovery and Value Logic

For each discovery assumption, answer three questions:

1. What evidence would prove or disprove it?
2. Who owns that evidence?
3. What scope change occurs if it fails?

Then trace the value hypothesis:

```text
Source-linked summary and bounded recommendation
→ less handling time and avoidable rework
→ time value plus avoided-rework value
→ quality and safety must remain above their approved floors
```

This prevents the team from counting model activity as business value. The formula values workflow improvement, while later scorecards verify adoption, quality, safety, and cost.

### Verification checkpoint

- **Expected result:** You can distinguish observed evidence, an unproven assumption, a calculated benefit, and a safety constraint.
- **Acceptable variation:** Another defensible benefit formula is acceptable if its inputs, owner, and measurement window are explicit.
- **Failure indicator:** Benefits depend only on recommendation volume, or assumptions have no owner or test.
- **Corrective action:** Connect value to time, rework, quality, or another customer outcome and assign evidence ownership.

## Step 4 — Validate and Commit Workshop 1

```bash
python3 -m json.tool problem_value.json
git init -b main
git add .gitignore problem_value.json
git commit -m "Frame capstone problem and value case"
git status --short --branch
```

### Verification checkpoint

- **Expected result:** JSON validation succeeds and Git reports a clean `main` branch.
- **Acceptable variation:** On older Git versions, run `git init`, followed by `git branch -M main`.
- **Failure indicator:** JSON reports a line error or Git still lists uncommitted files.
- **Corrective action:** Repair the first JSON error, stage the intended files, commit, and check status again.

## Map the Completed Workflow

| Capstone decision | Evidence you created | Downstream use |
| --- | --- | --- |
| Customer problem | User, friction, baseline, scope, and non-goals | Controls architecture and rollout scope |
| Business outcome | Time, rework, quality, and safety intent | Becomes the scorecard contract |
| Discovery brief | Evidence and testable assumptions | Drives team, data, and risk work |
| Value hypothesis | Benefit formula and financial assumptions | Enables the final business-outcome decision |

## Troubleshooting Cheatsheet

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `JSONDecodeError` | Missing comma, quote, brace, or bracket | Run `python3 -m json.tool problem_value.json` and repair the first reported line. |
| Outcome sounds like a feature | The result is written as “build an assistant” | Rewrite it as a measurable workflow or business change. |
| Value cannot be calculated | Inputs or financial assumptions are missing | Define the baseline, measurement, formula, and owner. |
| Scope includes claim decisions | Product capability and human authority are mixed | Restore the three non-goals and the licensed-adjuster boundary. |

## Cleanup

This workshop creates no cloud resources. Keep the directory and files for Workshop 2.

## Completion Check

- [ ] I named the primary user and workflow friction.
- [ ] I recorded time, rework, and quality baselines.
- [ ] I defined a measurable outcome and bounded scope.
- [ ] I preserved human authority over protected claim actions.
- [ ] I separated discovery evidence from owned assumptions.
- [ ] I can calculate the proposed benefit.
- [ ] My Workshop 1 commit is clean on `main`.

## Reflection

1. Which assumption would most weaken the value case if it failed?
2. Which attractive feature did the non-goals deliberately exclude?
3. What evidence would convince a finance partner that the benefit is real rather than estimated activity?
