# Data Quality Checklist

Run these checks on the raw source tables before joining, transformation, or modeling. Record the source, run date, row counts, failures, remediation, and the person approving each exception. Do not silently convert invalid or missing values into plausible values.

> **Schema limitation:** `data_dictionary.csv` and raw CSVs were not present in the supplied repository. The field list below is based on the provided Phase 1 Word deliverable and is provisional, not guaranteed exhaustive. Confirm every column and its allowed values against the authoritative dictionary before treating this checklist as complete.

## Provisional column classification

All fields listed are structured tabular data. No unstructured field was identified in the supplied Phase 1 materials; if the dictionary contains ticket text or other free text, add it to the inventory and assess it separately.

| Source / field | Data type | Structure | Notes |
|---|---|---|---|
| `customers.customer_id` | Identifier | Structured | Direct or pseudonymous customer key; validate uniqueness and linkage. |
| `customers.age` | Discrete | Structured | Numeric years; treat as personal information. |
| `customers.gender` | Nominal | Structured | Category; validate against documented domain. |
| `customers.income_band` | Ordinal | Structured | Ordered category; obtain the authoritative category order. |
| `customers.province` | Nominal | Structured | Geographic quasi-identifier. |
| `customers.city_type` | Nominal | Structured | Category; confirm values and meaning. |
| `customers.signup_date` | Date/time | Structured | Date; retain only required granularity. |
| `customers.plan_type` | Nominal | Structured | Category; confirm plan definitions. |
| `customers.payment_method` | Nominal | Structured | Category; confirm allowed values. |
| `customers.monthly_spend` | Continuous | Structured | Numeric monetary amount; confirm currency and period. |
| `customers.churned` | Nominal | Structured | Binary outcome mentioned in the brief; confirm exact encoding and observation window. |
| `usage_monthly.customer_id` | Identifier | Structured | Foreign key to customer table. |
| `usage_monthly.billing_month` | Date/time | Structured | Monthly period; confirm timezone/date convention if applicable. |
| `usage_monthly.data_mb` | Continuous | Structured | Usage quantity; confirm unit and whether fractional values are valid. |
| `usage_monthly.voice_mins` | Continuous | Structured | Usage quantity; confirm unit and whether fractional values are valid. |
| `support_tickets.ticket_id` | Identifier | Structured | Ticket key; validate uniqueness. |
| `support_tickets.customer_id` | Identifier | Structured | Foreign key to customer table. |
| `support_tickets.ticket_category` | Nominal | Structured | Category; confirm domain. |
| `support_tickets.created_at` | Date/time | Structured | Ticket creation timestamp. |
| `support_tickets.resolved_at` | Date/time | Structured | Resolution timestamp; may be missing for open tickets. |
| `support_tickets.resolution_hours` | Continuous | Structured | Duration; distinguish unresolved tickets from invalid values. |

## Six quality dimensions

| Dimension | Checks and acceptance criteria | Fields / sources |
|---|---|---|
| **Completeness** | Count nulls and blank strings by field; report missingness rates and patterns by churn, plan, and source. Distinguish legitimately absent resolution times on open tickets from missing data. Agree thresholds and remediation with the data owner before modeling. | All columns in customers, usage, and support tables. |
| **Validity** | Validate types, documented category domains, plausible age bounds, non-negative usage/spend/durations, and sentinel values such as `-999`. Require `resolved_at >= created_at` when both exist; confirm date parsing and currency/unit rules. | `age`, categories, `data_mb`, `voice_mins`, `monthly_spend`, ticket dates, `resolution_hours`, `churned`. |
| **Consistency** | Normalize whitespace and case only after recording original values; compare category meanings across extracts; check date formats, timezone conventions, monthly period conventions, and unit consistency. Reconcile contradictory churn or plan states with source owners. | `province`, `gender`, `plan_type`, `payment_method`, `ticket_category`, dates and measures across sources. |
| **Uniqueness** | Detect exact duplicate rows, duplicate customer primary keys, duplicate ticket IDs, and duplicate customer-month usage records. Define the expected grain for every table before deduplication. | `customers.customer_id`, `support_tickets.ticket_id`, `usage_monthly.customer_id` + `billing_month`. |
| **Timeliness** | Confirm extract and event timestamps, analysis cutoff, and prediction window. Reject or investigate future-dated events and usage outside the agreed study period; ensure features are available at prediction time. | `signup_date`, `billing_month`, `created_at`, `resolved_at`, churn outcome dates if available. |
| **Accuracy** | Check customer foreign keys against the customer master; reconcile sampled values and totals to approved CRM, billing, network, or ticketing source reports. Investigate implausible values with source owners rather than assuming they are errors. | Customer keys across usage/support; sampled demographics, spend, usage, and ticket records. |

## Pre-modeling sign-off

- [ ] Obtain and review the authoritative `data_dictionary.csv`; reconcile every field, type, unit, domain, and sensitivity classification.
- [ ] Confirm source provenance, permissions, table grain, and target definition with data owners.
- [ ] Save an audit summary and exceptions without exposing unnecessary personal information.
- [ ] Approve documented cleaning rules and verify they do not use information from after the prediction cutoff.
- [ ] Confirm that only authorized, minimized data moves into analysis or external sharing.
