# MzansiConnect Customer Churn & Retention Project Plan

## Project summary

MzansiConnect, a South African mobile network operator, needs to understand and reduce an estimated churn rate of approximately 21%, reported in the project brief and not yet verified against source data. The brief identifies prepaid subscribers without fixed-term contracts as a group of concern; this also requires validation against the data. Customer, monthly usage, and support-ticket data will inform churn-driver analysis and retention insights. Phase 1 describes the dataset as synthetic; raw data and the authoritative data dictionary are not included in this repository.

## Objectives and success criteria

- **Churn insights:** Audit and analyze the authorized data to identify churn drivers and customer segments; report findings with supporting evidence.
- **Predictive performance:** Evaluate a churn classifier using cumulative gains and lift, targeting capture of at least 50% of actual churners in the highest-risk 20%. This is a target, not a result.
- **Operational readiness:** Aim to deliver an interactive web application or scoring interface for retention agents, subject to data readiness and project scope. Do not describe this as deployed until verified.
- **Reproducibility:** Build a version-controlled, modular workflow covering raw CSV ingestion, data quality review, SQLite persistence, statistical testing, and model inference.
- **Additional analysis:** Explore regression for expected average monthly revenue over the next quarter and unsupervised segmentation where the data supports them.

## Data science questions

1. **Descriptive:** How does churn vary by province, contract or plan type, and payment method?
2. **Diagnostic:** Which support-ticket categories and resolution times are associated with churn?
3. **Diagnostic:** Do six-month data and voice usage trajectories differ between churned and retained subscribers?
4. **Predictive—classification:** What is an active subscriber’s probability of churning during a defined evaluation window?
5. **Predictive—regression:** What is a subscriber’s expected average monthly revenue (ZAR) over the next quarter?
6. **Prescriptive/segmentation:** Which behavioral segments emerge, and what appropriate retention actions could be considered for high-risk segments?

**Model framing:** Churn is binary classification (churn or retention). Regression predicts a continuous outcome such as next-quarter average revenue or time until cancellation.

## Stakeholders

| Stakeholder | Interest and use |
|---|---|
| Head of Customer Retention | Project sponsor; uses validated churn insights, executive reporting, and—if delivered—the scoring interface to prioritize outreach. |
| Marketing and Campaigns Team | Uses evidence-based segment profiles to inform appropriate offers and win-back campaigns. |
| Data Science and Analytics Lead | Owns repository and data workflow, quality auditing, SQLite warehousing, statistical validation, model development, and reporting. |

## Approach and lifecycle

1. **Kick-off and governance:** Establish the repository, confirm permitted use and provenance, and maintain the project plan, privacy note, and quality framework.
2. **Data fundamentals:** Obtain the authorized source files and data dictionary; confirm schema and table grain before claiming a complete field inventory.
3. **Audit and prepare:** Assess the six quality dimensions, document cleaning decisions, preserve raw inputs, and prepare authorized outputs.
4. **Persist and query:** Create the planned normalized SQLite database and implement documented business queries.
5. **Explore and test:** Explore churn patterns, conduct appropriate statistical tests, and communicate limitations.
6. **Engineer and model:** Engineer features available at prediction time, then train baseline classification and regression models without target leakage.
7. **Evaluate and segment:** Assess cumulative gains/lift, tune where justified, and perform segmentation where supported by the data.
8. **Deliver:** Validate performance and fairness, prepare the report and presentation, and build/deploy an interactive scoring tool only if data readiness and scope permit.

Throughout the lifecycle, apply access, retention, minimization, and deletion controls described in the governance note. Keep raw inputs unchanged and do not commit personal or restricted data.

## Schedule and principal risks

| Week | Milestone |
|---|---|
| 1 | Phases 1–3: repository and Git setup, project plan, governance note, and quality checklist. |
| 2 | Phases 4–5: data audit and cleaning, normalized SQLite database, and SQL business queries. |
| 3 | Phases 6–8: exploratory analysis, statistical hypothesis testing, and dashboard design. |
| 4 | Phases 9–11: feature engineering, baseline classification/regression, and deployment architecture. |
| 5 | Phases 12–13: tuning, gains/lift evaluation, and customer segmentation. |
| 6 | Phase 14: model serialization, interactive application deployment, final report, and presentation. |

These are planned milestones, not evidence that the work is complete. Data-dependent milestones may need to change if the source files, dictionary, or permitted access are unavailable.

| Risk | Mitigation |
|---|---|
| Missing, ambiguous, or poor-quality data, including sentinel values and inconsistent dates | Confirm source definitions, audit all six quality dimensions, and record each cleaning rule and its impact before database loading. |
| Target or temporal leakage | Separate labels from features, use only prediction-time information, and preserve train/test separation. |
| Privacy or POPIA exposure | Minimize and restrict data, apply appropriate masking/tokenization and access controls, and review sharing and retention before use. |
| Unfair or intrusive targeting | Review performance across relevant groups; use predictions to inform human review rather than as the sole basis for adverse treatment. |
