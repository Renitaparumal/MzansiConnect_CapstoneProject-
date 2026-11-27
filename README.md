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

The Phase 1 materials describe the data as synthetic. The schema
[data dictionary](data_dictionary.csv) is included. Cleaned CSV exports are
provided for the Phase 5 database work; the original raw CSVs are not included.
The SQL findings are descriptive and do not establish cause or predict model
performance.
See [the project plan](docs/project_plan.md), [the governance note](docs/data_governance_note.md),
and [the data quality checklist](docs/data_quality_checklist.md).

## Datasets

The data dictionary describes the following project-provided CSV tables for
`data/raw/`. The source files are not currently present in the repository.

| File | Expected contents |
|---|---|
| `customers.csv` | Customer identifiers, profile/account fields, and a churn target. |
| `usage_monthly.csv` | Monthly data, voice, SMS, revenue, and dropped-call complaint fields. |
| `support_tickets.csv` | Ticket identifiers, category, resolution, and post-resolution satisfaction fields. |

The cleaned exports used by Phase 5 are in `data/processed/`. See the dictionary
for field definitions. The original source-system provenance still requires
confirmation with the data owner. Keep authorized raw files in `data/raw/`,
preserve them unchanged, and do not commit personal or otherwise restricted
data.

## Repository structure

```text
.
├── .github/workflows/tests.yml
├── data_dictionary.csv
├── data/
│   ├── processed/
│   │   ├── customers_clean.csv
│   │   ├── usage_clean.csv
│   │   ├── tickets_clean.csv
│   │   └── mzansiconnect.db
│   └── raw/
├── docs/
│   ├── data_governance_note.md
│   ├── data_quality_checklist.md
│   ├── erd.png
│   ├── erd.dot
│   ├── sql_findings.md
│   └── project_plan.md
├── src/
│   ├── data_loading.py
│   ├── build_database.py
│   ├── make_erd.py
│   ├── run_queries.py
│   └── utils.py
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── tests/
│   ├── test_data_loading.py
│   ├── test_database.py
│   └── test_utils.py
├── reports/query_results/
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
versions are pinned in [requirements.txt](requirements.txt). GitHub Actions
also runs the test suite on pushes and pull requests.

## Data preparation and quality decisions

The implemented helpers support reporting missingness, standardizing selected
text fields, flagging IQR outliers, removing duplicates, and dropping rows
missing required values. They return results without changing the caller's
input, and log relevant row counts. Decisions such as imputation, sentinel
interpretation, duplicate removal, or exclusions must be based on inspection
of the actual data and documented before use. Phase 5 uses the supplied cleaned
exports; raw CSVs and a reproducible Phase 4 cleaning run are not included.

The Phase 1 checklist covers completeness, validity, consistency, uniqueness,
timeliness, and accuracy. Its field inventory classifies all 28 columns in the
checked-in data dictionary by analytical type, structure, and privacy handling.
The source CSVs are required to validate actual values and complete data
quality checks.

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

Phase 1 planning, governance, and quality documentation; Phase 2 Python
utilities/tests; and Phase 5 database assets are present. The raw CSV datasets
are not included. The SQL results are available in
[docs/sql_findings.md](docs/sql_findings.md); model evaluation and retention
recommendations remain out of scope.

## Phase 5: database and SQL

The database schema defines `customers`, `usage_monthly`, and `support_tickets`
with primary/foreign keys and indexes. The ERD is available as
[docs/erd.png](docs/erd.png), with editable Graphviz source in
[docs/erd.dot](docs/erd.dot). The twelve business questions and the
join-multiplication demonstration are in [sql/queries.sql](sql/queries.sql).

Rebuild the database from the cleaned exports and execute the queries:

```bash
python -m src.build_database
python -m src.run_queries
```

The query runner uses `sqlite3` and pandas, loads results into DataFrames, and
writes CSV results under `reports/query_results/`. The database is
`data/processed/mzansiconnect.db`. See the SQL findings for the Phase 5
checkpoint answers, including why joining both child tables before aggregation
inflates revenue and the storage/write costs of indexes.

## Git workflow

Use focused feature branches and pull requests with a summary, rationale,
affected files, and test results. The project README also records the
intentional merge-conflict practice and its resolution.

### Checkpoint questions

- **Which columns should be removed or masked before external sharing, and
  why?** Remove `customer_id` and `ticket_id`, or replace them with
  project-specific tokens whose key is kept separately. Generalize or
  suppress `age`, `signup_date`, `province`, and `city_type`, especially in
  combination; review `income_band`, `gender`, account, usage, and support
  fields for rare groups. Share only necessary fields. Hashing or tokenization
  reduces direct identification but does not guarantee anonymization.
- **Is churn classification or regression?** The primary framing is binary
  classification (churn or retained during a defined window). A regression
  framing predicts a continuous outcome such as next-quarter revenue or time
  until cancellation.
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
