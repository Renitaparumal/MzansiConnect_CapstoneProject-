# MzansiConnect Customer Churn & Retention Project Plan

## Project summary

MzansiConnect, a South African mobile network operator, needs to understand and reduce churn, estimated at approximately 21%. Customer, monthly usage, and support-ticket data will inform churn-driver analysis and retention insights. Phase 1 describes the dataset as synthetic; raw data is not included in this repository.

## Objectives and success criteria

- Create a reproducible workflow from raw-data review through analysis and delivery; identify churn drivers and customer segments.
- Evaluate a churn classifier against the target of capturing at least 50% of churners in the highest-risk 20%, using cumulative gains and lift.
- Explore revenue regression and deliver findings in a report; provide an interactive scoring interface if scope and data readiness allow.

## Data science questions

1. **Descriptive:** How does churn vary by province, contract or plan type, and payment method?
2. **Diagnostic:** Which support-ticket categories and resolution times are associated with churn?
3. **Diagnostic:** Do six-month data and voice usage trajectories differ between churned and retained subscribers?
4. **Predictive—classification:** What is an active subscriber’s probability of churning during a defined evaluation window?
5. **Predictive—regression:** What is a subscriber’s expected average monthly revenue (ZAR) over the next quarter?
6. **Prescriptive/segmentation:** Which behavioral segments emerge, and what appropriate retention actions could be considered for high-risk segments?

**Model framing:** Churn is binary classification (churn or retention). Regression predicts a continuous outcome such as next-quarter average revenue or time until cancellation.

## Stakeholders

Retention leadership will prioritize outreach; marketing will use segments to inform campaigns; the data science lead will own auditing, analysis, validation, and reporting.

## Approach and lifecycle

1. **Acquire:** Confirm provenance, permitted use, schema, and study period; store authorized inputs in `data/raw/`.
2. **Audit and prepare:** Check six quality dimensions, document cleaning, preserve raw inputs, and store authorized outputs in `data/processed/`.
3. **Analyze:** Explore and test churn patterns; engineer only prediction-time features and evaluate classification and regression.
4. **Validate and deliver:** Check performance, leakage, and fairness; document limitations, report aggregate findings, and apply access, retention, and deletion controls.

## Schedule and principal risks

| Week | Milestone |
|---|---|
| 1 | Repository, governance, and plan |
| 2 | Data audit, cleaning, database, and SQL |
| 3 | Exploratory analysis and hypothesis tests |
| 4 | Feature engineering and baseline models |
| 5 | Evaluation, tuning, and segmentation |
| 6 | Report, presentation, and application if in scope |

Key risks are poor or ambiguous data, leakage, privacy exposure, and unfair or intrusive targeting. Mitigate through documented validation, time-aware features and train/test separation, minimization and access controls, and fairness review.
