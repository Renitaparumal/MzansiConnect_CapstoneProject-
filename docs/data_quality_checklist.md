# MzansiConnect Data Quality Checklist

Run this checklist on each authorized source table before transformation or modelling. Keep raw inputs unchanged, record the file/version and study cutoff, and log each check, result, decision, and affected-row count in the cleaning record. Do not silently interpret sentinel values such as `-999` as valid measurements or replace them without documenting their meaning.

## Six data quality dimensions

| Dimension | Checks | Example fields |
|---|---|---|
| **Completeness** | Count nulls and missing percentages by column; check missingness by plan and other relevant groups; distinguish genuine missing values from documented sentinel codes. | All columns in `customers.csv`, `usage_monthly.csv`, and `support_tickets.csv`; examples include `age`, `income_band`, and `resolution_hours`. |
| **Validity** | Confirm values conform to documented type, range, and domain rules; identify impossible ages, negative usage or revenue, invalid categories, and out-of-range satisfaction scores. Validate sentinel-code meaning before recoding. | `age`, `contract_months`, `data_gb`, `voice_minutes`, `sms_count`, `revenue_zar`, `resolution_hours`, `satisfaction_score`, and categorical fields. |
| **Consistency** | Check formats, units, category spelling/casing, date conventions, and agreement of shared identifiers and related records across tables. Resolve ambiguous dates using source documentation, not guesswork. | `province`, `gender`, `plan_type`, `payment_method`, `category`, date fields, and `customer_id`. |
| **Uniqueness** | Find exact duplicate rows and duplicate values in fields expected to be keys; verify the intended grain before treating repeated customer IDs in monthly or ticket tables as errors. | `customer_id` in the customer master; `ticket_id` in support tickets; customer-month grain in usage. |
| **Timeliness** | Validate the study period and cutoff; identify dates outside it, future-dated activity, stale records, and impossible event orderings. Parse mixed date formats only when unambiguous or supported by source documentation. | `signup_date`, `month`, and `created_date`. |
| **Accuracy** | Where an authoritative source or business rule exists, reconcile sampled values and derived measures to it; investigate implausible values and conflicting records. Check that each foreign key in usage and support records maps to a valid customer; investigate unmatched keys rather than deleting them automatically. | Customer attributes and spend against source records; `customer_id` in `usage_monthly.csv` and `support_tickets.csv` against the customer master. |

## Field classification inventory

The inventory below covers every field in the repository's `data_dictionary.csv`. That dictionary describes the schema but the source CSVs are not present, so actual values, completeness, table grain, and definitions still need to be verified against the data. The dictionary describes `usage_monthly.csv` as January–June 2026 and `churned` as whether the customer left by 31 July 2026; confirm these windows against the supplied data before analysis.

| Source table | Field | Dictionary type / analytical interpretation | Privacy classification and handling |
|---|---|---|---|
| `customers.csv` | `customer_id` | Text; identifier/key | Direct identifier; exclude from shared extracts or use a project-specific token, with any re-identification key held separately. |
| `customers.csv` | `signup_date` | Date or text; date with mixed formats | Personal/quasi-identifier; parse only when unambiguous, and reduce precision or remove for sharing if unnecessary. |
| `customers.csv` | `age` | Integer; numeric | Personal/quasi-identifier; use broad age bands in shared data and assess group-level model performance. |
| `customers.csv` | `gender` | Category; nominal | Personal demographic information; restrict to the authorized purpose and assess fairness implications. |
| `customers.csv` | `province` | Category; nominal | Personal/quasi-identifier; coarsen or aggregate when linkage or small groups are possible. |
| `customers.csv` | `city_type` | Category; nominal | Location-related quasi-identifier; generalize or suppress where combinations create linkage risk. |
| `customers.csv` | `plan_type` | Category; nominal | Account information; share only when needed and review combinations for small groups. |
| `customers.csv` | `contract_months` | Integer; numeric/discrete | Contract/account information; minimize and aggregate or band for sharing when exact duration is unnecessary. |
| `customers.csv` | `device_type` | Category; nominal | Device/account information; minimize and review combinations for small groups. |
| `customers.csv` | `payment_method` | Category; nominal | Financial/account-related information; minimize and restrict access. |
| `customers.csv` | `income_band` | Category; ordinal | Financial/demographic information; minimize, aggregate small groups, and assess fairness. |
| `customers.csv` | `referral_source` | Category; nominal | Acquisition/behavioral information; share only when needed and group rare values. |
| `customers.csv` | `cancellation_reason` | Category; nominal | Post-cancellation account information; restrict access and exclude from churn prediction because it is recorded at cancellation and leaks the outcome. |
| `customers.csv` | `churned` | Yes/No; binary target | Account outcome; restrict to the authorized purpose, protect as a label, and exclude from predictors. |
| `usage_monthly.csv` | `customer_id` | Text; foreign key/identifier | Direct identifier; tokenize consistently for authorized joins, then exclude from shared extracts unless essential. |
| `usage_monthly.csv` | `month` | Text; year-month period | Behavioral timeline; retain only the necessary period and review linkage risk before sharing. |
| `usage_monthly.csv` | `data_gb` | Float; numeric/continuous | Telecommunications usage information; minimize and aggregate where appropriate. |
| `usage_monthly.csv` | `voice_minutes` | Float; numeric/continuous | Telecommunications usage information; minimize and aggregate where appropriate. |
| `usage_monthly.csv` | `sms_count` | Integer; numeric/count | Telecommunications usage information; minimize and aggregate where appropriate. |
| `usage_monthly.csv` | `revenue_zar` | Float; numeric/continuous (ZAR) | Customer revenue/account information; aggregate or band for sharing when precise values are unnecessary. |
| `usage_monthly.csv` | `dropped_call_complaint` | Binary; indicator | Service experience/complaint information; restrict to the authorized purpose and aggregate where possible. |
| `support_tickets.csv` | `ticket_id` | Text; identifier/key | Record identifier that may enable linkage; remove or replace with a project-specific token before sharing. |
| `support_tickets.csv` | `customer_id` | Text; foreign key/identifier | Direct identifier; tokenize consistently for authorized joins, then exclude from shared extracts unless essential. |
| `support_tickets.csv` | `created_date` | Date | Support-interaction timeline; reduce precision or remove if unnecessary for the analysis or sharing. |
| `support_tickets.csv` | `category` | Category; nominal | Support-interaction information; review rare categories and group small counts. |
| `support_tickets.csv` | `resolution_hours` | Float; numeric/continuous | Support-interaction information; the dictionary says blank when unresolved, so distinguish unresolved tickets from missing data. Aggregate if sharing. |
| `support_tickets.csv` | `resolved` | Yes/No; binary | Support-interaction outcome; restrict to the authorized purpose and use only if available by the prediction cutoff. |
| `support_tickets.csv` | `satisfaction_score` | Integer; ordinal (1–5) | Support-interaction information; dictionary describes post-resolution CSAT, so exclude from prediction if it would not be available at the prediction time. |

## Sign-off before analysis

- [ ] Confirm every source file, table grain, field, type, permitted use, and key against the authoritative data dictionary and actual data.
- [ ] Record the study period, cutoff, quality rules, findings, and cleaning decisions.
- [ ] Confirm join keys and check unmatched foreign keys without deleting rows automatically.
- [ ] Document exclusions, transformations, and row counts; retain only authorized processed outputs.
- [ ] Review privacy and small-group risks before sharing data, plots, notebooks, or model outputs.
