# Capstone Workshop 2 — Design the Team and Decision Model

## Goal

Select the cross-functional forward deployed team for the Enterprise AI Claims Assistant and assign explicit decision rights for business scope, architecture, security, protected claim actions, go-live, rollback, and productization.

Continue in the learner-owned project directory from Workshop 1. The completed course repository remains a reference, not your workspace.

## What You'll Build or Produce

- `team_decisions.json` — named roles, accountabilities, allocations, and six consequential decision-rights records.
- A staffing rationale tied to the risks and rollout stage.
- The Workshop 2 Git commit in the same capstone repository.

## Estimated Time

35–50 minutes.

## Cost Guardrails

This workshop runs locally and creates no external services or cost.

## Completion Evidence

- `python3 -m json.tool team_decisions.json` succeeds.
- Seven required delivery roles have names, accountabilities, and positive allocations.
- Six enterprise decisions have responsible roles and one accountable role.
- Customer authority over protected claim actions and go-live remains explicit.
- Metadata matches `problem_value.json` exactly.
- Git is clean after the Workshop 2 commit.

## Prerequisites

- Completed Workshop 1 files in the same project directory
- Familiarity with forward deployed roles, staffing allocations, RACI, escalation, and customer authority

## Where This Workshop Fits

This workshop combines **Select the Forward Deployed Team** and **Assign Ownership and Decision Rights**. It converts the problem and value case into an operating model capable of making and executing the required decisions.

## Step 1 — Create the Team and Decision Artifact

Create `team_decisions.json`:

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
  "forward_deployed_team": [
    {
      "role": "Technical Deployment Lead",
      "name": "Jordan Kim",
      "accountability": "Integrated outcome, plan, decisions, risks, cutover, and handoff",
      "allocation_fte": 1.0
    },
    {
      "role": "Forward Deployed Engineer",
      "name": "Sam Rivera",
      "accountability": "End-to-end workflow, customer integration, and evidence",
      "allocation_fte": 2.0
    },
    {
      "role": "AI Engineer",
      "name": "Avery Chen",
      "accountability": "Retrieval, model behavior, evaluation, and guardrails",
      "allocation_fte": 1.0
    },
    {
      "role": "Platform Engineer",
      "name": "Morgan Lee",
      "accountability": "Environments, observability, reliability, and rollback",
      "allocation_fte": 1.0
    },
    {
      "role": "Security Engineer",
      "name": "Dana Brooks",
      "accountability": "Threat model, access, data protection, and security approval",
      "allocation_fte": 0.5
    },
    {
      "role": "Product Partner",
      "name": "Taylor Reed",
      "accountability": "Adoption, value measurement, and reusable product signals",
      "allocation_fte": 0.5
    },
    {
      "role": "Claims Subject-Matter Expert",
      "name": "Marcus Green",
      "accountability": "Ground truth, workflow acceptance, training, and quality review",
      "allocation_fte": 0.5
    }
  ],
  "decision_rights": [
    {
      "decision": "Business outcome and rollout scope",
      "responsible": [
        "Technical Deployment Lead",
        "Product Partner"
      ],
      "accountable": "Business Owner",
      "consulted": [
        "Claims Subject-Matter Expert",
        "Finance Partner"
      ],
      "informed": [
        "Steering Committee"
      ]
    },
    {
      "decision": "Architecture and technical exceptions",
      "responsible": [
        "Forward Deployed Engineer",
        "AI Engineer",
        "Platform Engineer"
      ],
      "accountable": "Technical Deployment Lead",
      "consulted": [
        "Security Engineer"
      ],
      "informed": [
        "Business Owner"
      ]
    },
    {
      "decision": "Security risk acceptance",
      "responsible": [
        "Security Engineer"
      ],
      "accountable": "Security Approver",
      "consulted": [
        "Technical Deployment Lead",
        "Data Owner"
      ],
      "informed": [
        "Business Owner"
      ]
    },
    {
      "decision": "Protected claim action",
      "responsible": [
        "Licensed Claims Adjuster"
      ],
      "accountable": "Claims Operations Owner",
      "consulted": [
        "Claims Subject-Matter Expert"
      ],
      "informed": [
        "Audit and Compliance"
      ]
    },
    {
      "decision": "Go-live or rollback",
      "responsible": [
        "Technical Deployment Lead",
        "Platform Engineer"
      ],
      "accountable": "Claims Operations Owner",
      "consulted": [
        "Security Approver",
        "Business Owner"
      ],
      "informed": [
        "Pilot Users",
        "Support Team"
      ]
    },
    {
      "decision": "Productization investment",
      "responsible": [
        "Product Partner"
      ],
      "accountable": "Product Owner",
      "consulted": [
        "Technical Deployment Lead",
        "Platform Engineer",
        "Security Engineer"
      ],
      "informed": [
        "FDE Portfolio Lead"
      ]
    }
  ]
}
```

The team is selected for this deployment stage, not from a generic org chart. The architecture needs AI, platform, security, product, workflow, and integration capability. The rollout also needs one technical deployment lead who owns the integrated plan and customer outcome.

### Verification checkpoint

- **Expected result:** Seven unique roles have named people, clear accountabilities, and positive FTE allocations.
- **Acceptable variation:** Names and allocations may reflect another organization if all seven capabilities remain covered.
- **Failure indicator:** A single “AI engineer” owns discovery, security, platform, adoption, and cutover.
- **Corrective action:** Separate the capability areas and assign realistic accountable roles and allocations.

## Step 2 — Challenge the Staffing Model

For every team member, connect the allocation to a concrete capstone obligation:

| Role | Obligation that justifies the role |
| --- | --- |
| Technical Deployment Lead | Integrated outcome, decisions, delivery risks, cutover, and handoff |
| Forward Deployed Engineer | Customer workflow and end-to-end integration |
| AI Engineer | Retrieval, evaluation, model behavior, and guardrails |
| Platform Engineer | Environments, observability, reliability, and rollback |
| Security Engineer | Threats, access, data protection, and security approval |
| Product Partner | Adoption, value measurement, and reusable capability signals |
| Claims Subject-Matter Expert | Ground truth, workflow acceptance, training, and quality |

Do not maximize staffing. Choose the smallest credible team and expose fractional specialist demand rather than hiding it.

### Verification checkpoint

- **Expected result:** Every role maps to work that would otherwise be unowned or create a delivery bottleneck.
- **Acceptable variation:** One person may fill two roles if the accountabilities and available capacity remain explicit.
- **Failure indicator:** Allocations are copied from a template without any relationship to scope, risk, or rollout stage.
- **Corrective action:** Remove unjustified capacity and add any missing capability required by the actual plan.

## Step 3 — Test the Decision Rights

Review the six decision records. Each must answer:

- Who performs the work?
- Who has final accountability?
- Which customer authority cannot be delegated to the vendor or model?
- Who must be consulted before the decision?
- Who needs timely notification after the decision?

Pay particular attention to two boundaries:

1. A licensed claims adjuster remains responsible for a protected claim action, with the Claims Operations Owner accountable.
2. The Claims Operations Owner remains accountable for go-live or rollback even though the technical team prepares and executes the plan.

### Verification checkpoint

- **Expected result:** Each decision has at least one responsible role and exactly one accountable role expressed as a single value.
- **Acceptable variation:** Consulted and informed groups may change with the organization.
- **Failure indicator:** Two roles both have final accountability, or the model/vendor owns a protected customer decision.
- **Corrective action:** Name one accountable role and restore customer authority for consequential business actions.

## Step 4 — Validate Cross-Workshop Consistency and Commit

```bash
python3 -m json.tool team_decisions.json
python3 -c "import json; a=json.load(open('problem_value.json')); b=json.load(open('team_decisions.json')); assert a['metadata']==b['metadata']; print('Metadata aligned')"
git add team_decisions.json
git commit -m "Design capstone team and decision rights"
git status --short --branch
```

### Verification checkpoint

- **Expected result:** Both validation commands succeed, `Metadata aligned` prints, and Git is clean.
- **Acceptable variation:** Equivalent JSON comparison code is acceptable.
- **Failure indicator:** The customer, initiative, candidate, or review stage differs between workshop artifacts.
- **Corrective action:** Copy the complete metadata object from `problem_value.json`, validate again, and commit.

## Map the Completed Workflow

| Input | Decision | Output |
| --- | --- | --- |
| Problem, scope, and assumptions | Which capabilities are required? | Seven-role deployment team |
| Delivery stage and risk | How much capacity is credible? | Explicit FTE allocations |
| Consequential decisions | Who works, decides, advises, and learns? | Six decision-rights records |
| Protected actions | Which authority stays with the customer? | Licensed-adjuster and Claims Operations ownership |

## Troubleshooting Cheatsheet

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Metadata comparison fails | An artifact uses a different case version | Copy metadata from Workshop 1 without editing it. |
| One role owns everything | Staffing was organized around a hero | Split accountabilities across the required capabilities. |
| Decision has multiple accountable parties | Consensus was confused with accountability | Select one final accountable role and keep others consulted. |
| Customer authority is unclear | Technical execution and business authority were combined | Name the licensed adjuster or Claims Operations Owner explicitly. |

## Cleanup

This workshop creates no external resources. Keep all files for Workshop 3.

## Completion Check

- [ ] Seven required delivery capabilities are staffed.
- [ ] Every team member has a named accountability and allocation.
- [ ] Six consequential decisions have responsible and accountable roles.
- [ ] Protected actions and go-live preserve customer authority.
- [ ] Workshop metadata is aligned.
- [ ] My Workshop 2 commit is clean.

## Reflection

1. Which role becomes the first bottleneck if the rollout doubles in size?
2. Which decision is most dangerous to leave ambiguous during cutover?
3. Where could one person fill two roles safely, and where would that create a conflict?
