# MzansiConnect Customer Churn and Retention: Project Plan

## Business problem

The project brief describes MzansiConnect, a mid-sized South African mobile network operator with an approximate 21% customer churn rate, particularly among prepaid customers without fixed-term contracts. Since acquiring a customer costs more than retaining one, the business needs evidence about why subscribers leave and a practical way to prioritize fair, relevant retention support.

## Measurable success criteria

- On a held-out evaluation set, the churn model captures at least 50% of actual churners in the highest-risk 20% of customers, measured with cumulative gains and lift.
- Deliver a reproducible pipeline from permitted source files through data checks and analysis to model scoring.
- Provide an interactive scoring interface or equivalent documented workflow for retention staff, with clear limitations and human oversight.
- Report churn patterns and model performance across relevant customer groups before recommending any campaign.

## Stakeholders

| Stakeholder | Role and interest |
|---|---|
| Head of Customer Retention | Sponsor; uses churn insights and risk prioritization to plan outreach. |
| Marketing and Campaigns | Uses validated customer segments to shape relevant offers and win-back campaigns. |
| Data Science and Analytics | Audits, prepares, analyzes, and models the data; documents reproducibility and limitations. |
| Retention agents | Use any approved scoring workflow to guide, not replace, customer-support decisions. |
| Customers | Data subjects whose privacy, service experience, and fair treatment must be protected. |

## Data science questions

1. **Descriptive:** What proportion of subscribers churn, overall and by province, plan type, and payment method?
2. **Diagnostic:** Which support-ticket categories and resolution times are associated with churn, after accounting for relevant customer differences?
3. **Diagnostic:** Do six-month data and voice usage trends differ between churned and retained subscribers?
4. **Predictive (classification):** What is the probability that an eligible active subscriber will churn during a defined future evaluation window?
5. **Predictive (regression):** What monthly revenue (ZAR) should be expected from a subscriber over the next quarter?
6. **Prescriptive:** Which retention action, if any, is appropriate for each validated high-risk customer segment, considering likely benefit, cost, and customer impact?
7. **Prescriptive:** Which 20% of eligible customers should receive limited outreach capacity to capture at least 50% of expected churners, subject to fairness and campaign constraints?

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Missing values, duplicate records, sentinel values (such as `-999`), or inconsistent formats distort results. | Profile all sources against the six-dimensional quality checklist; document cleaning decisions and preserve raw data access controls. |
| Leakage from churn labels or post-outcome activity inflates model performance. | Define the prediction date and outcome window; exclude post-cutoff information and split data before fitting preprocessing steps. |
| Personal information is exposed or re-identification occurs from combined attributes. | Minimize fields, restrict access, mask identifiers, coarsen quasi-identifiers, and review each proposed disclosure. |
| Model errors or biased targeting harm customers or exclude groups from useful support. | Evaluate false positives/negatives and performance across groups; use human review, suitable interventions, and monitoring. |

## Six-week timeline

| Week | Milestones |
|---|---|
| 1 | Confirm brief, data authority and schema; establish repository, governance, and quality checks. |
| 2 | Audit and clean permitted data; design and populate a normalized SQLite store. |
| 3 | Explore churn patterns, test hypotheses, and develop stakeholder-facing summaries. |
| 4 | Engineer time-valid features; build baseline classification and revenue regression models. |
| 5 | Tune and evaluate models, gains/lift, and customer segments; perform fairness and error analysis. |
| 6 | Finalize a reviewed scoring interface, documentation, limitations, and presentation; plan monitoring and retention. |

## Data lifecycle and access

Subject to authorization and data-minimization review, customer and plan attributes may come from a CRM or billing platform, monthly activity from network usage/billing logs, and issue history from a call-centre or ticketing system. A controlled ingestion step should validate file provenance and schema, then store encrypted raw extracts with narrow access. Approved, minimized analytical tables can be stored in a secured SQLite database for this capstone, with pseudonymous keys and documented transformations. Notebooks, reports, and any scoring interface should use only the approved analytical view; external sharing requires a disclosure review and de-identification. Access should be role-based: data stewards manage source data, named analysts access only what is needed, retention staff see only authorized scores and explanations, and external contractors receive a minimized, masked extract only under approved terms. Log access and exports, protect credentials separately, and securely delete or anonymize data at the end of the approved retention period.

## Schema note

The referenced `data_dictionary.csv` was not present in the supplied repository when this plan was prepared. The column inventory and classifications in [the data quality checklist](./data_quality_checklist.md) cover fields named in the supplied Phase 1 deliverable and are provisional, not a verified exhaustive dictionary. Reconcile them against the authoritative dictionary and source files before analysis.
