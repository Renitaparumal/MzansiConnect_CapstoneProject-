# MzansiConnect Customer Churn & Retention Project Plan

## Business problem and success criteria

The project brief describes an estimated churn rate of approximately 21% and identifies prepaid subscribers without fixed-term contracts as a group of concern. These are brief-level claims, not yet validated against the source CSVs. MzansiConnect needs evidence about churn drivers and customer segments to guide appropriate retention work.

- **Predictive target:** Identify the highest-risk 20% of customers and capture at least 50% of actual churners, measured with cumulative gains and lift. This is a target, not a result.
- **Analysis:** Report data-supported churn drivers and segments, with statistical evidence and limitations.
- **Reproducibility:** Build a documented workflow for data audit, preparation, SQLite storage, statistical testing, and model evaluation.
- **Delivery:** Prepare a final report and presentation; an interactive scoring tool is planned if data and scope permit.

## Data science questions

1. **Descriptive:** How does churn vary by province, plan type, and payment method?
2. **Diagnostic:** Which support-ticket categories and resolution experiences are associated with churn?
3. **Diagnostic:** Do six-month data and voice usage patterns differ between churned and retained customers?
4. **Predictive—classification:** What is an active customer's probability of churning during the defined evaluation window?
5. **Predictive—regression:** What is a customer's expected average monthly revenue over the next quarter?
6. **Prescriptive:** Which behavioral segments merit appropriate retention interventions, subject to human review?

Churn is framed as binary classification. A regression framing predicts a continuous outcome such as future revenue or time until cancellation.

## Stakeholders and risks

| Stakeholder | Role |
|---|---|
| Head of Customer Retention | Sponsor; uses validated insights to prioritize outreach. |
| Marketing and Campaigns Team | Uses supported segment findings to inform appropriate campaigns. |
| Data Science and Analytics Lead | Owns data audit, analysis, database, validation, modelling, and reporting. |

| Principal risk | Mitigation |
|---|---|
| Incomplete or ambiguous data | Confirm sources and definitions; audit six quality dimensions and document cleaning decisions. |
| Target or temporal leakage | Use only information available at prediction time; separate labels and preserve train/test separation. |
| Privacy exposure | Minimize and restrict access; apply sharing, retention, and deletion controls in the governance note. |
| Unfair or intrusive targeting | Review performance across relevant groups; predictions support human review, not sole adverse decisions. |

## Six-week timeline

| Week | Planned milestone |
|---|---|
| 1 | Phases 1–3: repository, project plan, governance note, and quality checklist. |
| 2 | Phases 4–5: data audit/cleaning, normalized SQLite database, and SQL queries. |
| 3 | Phases 6–8: exploratory analysis, hypothesis testing, and dashboard design. |
| 4 | Phases 9–11: feature engineering, baseline models, and deployment architecture. |
| 5 | Phases 12–13: tuning, gains/lift evaluation, and segmentation. |
| 6 | Phase 14: model serialization, scoring application if in scope, report, and presentation. |

Milestones are plans, not evidence of completion. The repository contains the schema dictionary but not the source CSVs; data-dependent work awaits authorized data and validation.
