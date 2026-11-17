# MzansiConnect Customer Churn & Retention

A five-person Shaper's Data Science Program capstone project exploring how a
South African mobile network operator can understand customer churn and plan
appropriate retention work.

## Project overview

The project brief describes an estimated churn rate of approximately 21%. The
goal is to build a reproducible workflow for auditing customer data, exploring
churn drivers, evaluating churn classification and revenue regression, and
communicating responsible, actionable findings. The project plan sets a target
of capturing at least 50% of churners in the highest-risk 20% of customers.
This is a target, not a measured result.

The Phase 1 materials describe the data as synthetic. The raw CSVs and
authoritative data dictionary are not included in this repository, so no
dataset-level findings, model scores, or cleaning outcomes are claimed here.
See [the project plan](docs/project_plan.md), [the governance note](docs/data_governance_note.md),
and [the data quality checklist](docs/data_quality_checklist.md).

## Datasets

The project expects the following project-provided CSV tables in `data/raw/`.
They are not currently present in the repository.

| File | Expected contents |
|---|---|
| `customers.csv` | Customer profile and account fields, such as customer ID, demographics, plan, payment method, spend, and the churn target where provided. |
| `usage_monthly.csv` | Monthly customer usage, including data and voice measures. |
| `support_tickets.csv` | Support interactions, including ticket category and resolution timing. |

These descriptions and example fields are drawn from the Phase 1 materials;
verify exact columns, definitions, and sources against the authoritative data
dictionary before analysis. Keep authorized raw files in `data/raw/`, preserve
them unchanged, and do not commit personal or otherwise restricted data.

## Repository structure

```text
.
├── .github/workflows/tests.yml
├── data/
│   ├── processed/
│   └── raw/
├── docs/
│   ├── data_governance_note.md
│   ├── data_quality_checklist.md
│   └── project_plan.md
├── src/
│   ├── data_loading.py
│   └── utils.py
├── tests/
│   ├── test_data_loading.py
│   └── test_utils.py
├── phase2_data_loading.py
├── phase2_utils.py
├── test_phase2_utils.py
└── requirements.txt
```

`src/` contains the reusable project loaders and quality helpers. The
`phase2_*.py` files and root-level `test_phase2_utils.py` are a separate Phase 2
implementation retained for the assignment.

## Setup and tests

Tested with Python 3.14.2. From a fresh clone:

```bash
git clone https://github.com/Renitaparumal/MzansiConnect_CapstoneProject-.git
cd MzansiConnect_CapstoneProject-
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -v
```

On Windows, activate the environment with `.venv\Scripts\activate`. Dependency
versions are pinned in [requirements.txt](requirements.txt). The current test
suite result is **25 passed**; GitHub Actions also runs the test suite on pushes
and pull requests.

## Data preparation and quality decisions

The implemented helpers support reporting missingness, standardizing selected
text fields, flagging IQR outliers, removing duplicates, and dropping rows
missing required values. They return results without changing the caller's
input, and log relevant row counts. Decisions such as imputation, sentinel
interpretation, duplicate removal, or exclusions must be based on inspection
of the actual data and documented before use. Since the CSVs are absent, this
repository does not claim that a cleaning pass has been completed.

The Phase 1 checklist covers completeness, validity, consistency, uniqueness,
timeliness, and accuracy. Its field inventory is provisional until it can be
reconciled with the authoritative dictionary.

## Team responsibilities

The project is a five-person collaboration. The checked-in materials do not
reliably attribute completed work to individual members, so individual names
and contribution claims are intentionally not inferred from commit history.
The team should record each member's actual ownership and contributions here
as work is assigned. Project work areas are:

| Work area | Responsibilities |
|---|---|
| Data and governance | Confirm data provenance, dictionary, permitted use, and privacy controls. |
| Data preparation | Audit quality dimensions, document cleaning decisions, and maintain reproducible loaders. |
| Analysis and modelling | Explore churn drivers and evaluate classification/regression without leakage. |
| Validation and delivery | Review model performance/fairness and prepare evidence-based reports or tools. |
| Repository coordination | Maintain tests, documentation, review workflow, and release evidence. |

## Current status and evidence

Phase 1 planning and governance documents and Phase 2 Python utilities/tests are
present. The repository currently has no raw datasets, data dictionary, or
reported analytical findings. Conclusions and retention recommendations
therefore remain pending actual data analysis and model validation.

## Git workflow

Use focused feature branches and pull requests with a summary, rationale,
affected files, and test results. The project README also records the
intentional merge-conflict practice and its resolution.

### Checkpoint questions

- **Why use a virtual environment?** It isolates pinned project dependencies
  from other Python projects and makes setup more reproducible.
- **Why return a DataFrame instead of modifying it in place?** Returning a new
  object avoids unexpected changes to data held by callers and makes helpers
  easier to test.
- **What is the difference between merge and rebase?** Merge joins histories
  while preserving branch commits; rebase replays commits on a new base and
  changes their IDs. Avoid rebasing commits others depend on.
- **Why use pull requests?** They enable review, discussion, automated checks,
  and a record of why changes were integrated.

### Merge conflict practice

Two practice branches changed the same README sentence differently. Merging
them produced a conflict. It was resolved by comparing both versions, keeping
the wording that accurately described the workflow, removing conflict markers,
and completing the merge commit.
