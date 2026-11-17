# MzansiConnect Data Quality Checklist

Run this checklist on each authorized source table before transformation or modelling. Keep raw inputs unchanged, record the file/version and study cutoff, and log each check, result, decision, and affected-row count in the cleaning record. Do not silently interpret sentinel values such as `-999` as valid measurements or replace them without documenting their meaning.

## Six data quality dimensions

| Dimension | Checks | Example fields |
|---|---|---|
| **Completeness** | Count nulls and missing percentages by column; check missingness by plan and other relevant groups; distinguish genuine missing values from documented sentinel codes. | All columns in `customers.csv`, `usage_monthly.csv`, and `support_tickets.csv`; examples include `age`, `data_mb`, and `resolution_hours`. |
| **Validity** | Confirm values conform to documented type, range, and domain rules; identify impossible ages, negative usage or spend, invalid categories, and non-positive ticket resolution times. Validate sentinel-code meaning before recoding. | `age`, `data_mb`, `voice_mins`, `monthly_spend`, `resolution_hours`, categorical fields. |
| **Consistency** | Check formats, units, category spelling/casing, date conventions, and agreement of shared identifiers and related records across tables. Resolve ambiguous dates using source documentation, not guesswork. | `province`, `gender`, `plan_type`, `payment_method`, `ticket_category`, date fields, `customer_id`. |
| **Uniqueness** | Find exact duplicate rows and duplicate values in fields expected to be keys; verify the intended grain before treating repeated customer IDs in monthly or ticket tables as errors. | `customer_id` in the customer master; `ticket_id` in support tickets; customer-month grain in usage. |
| **Timeliness** | Validate the study period and cutoff; identify dates outside it, future-dated activity, stale records, and impossible event orderings such as resolution before ticket creation. | `signup_date`, `billing_month`, `created_at`, `resolved_at`. |
| **Accuracy** | Where an authoritative source or business rule exists, reconcile sampled values and derived measures to it; investigate implausible values and conflicting records. Referential integrity is also checked as a cross-table consistency check. | Customer attributes and spend against source records; usage and support `customer_id` values against the customer master. |

## Field classification inventory

The Word submission names the fields below, but the repository does not currently contain the CSV files or the actual data dictionary. This inventory classifies all fields explicitly named in the Phase 1 materials; compare it with the authoritative dictionary and add any omitted fields before marking the inventory complete. Analytical types are provisional until confirmed against the source schema.

| Source table | Field | Provisional analytical type | Privacy classification and handling |
|---|---|---|---|
| `customers.csv` | `customer_id` | Identifier / key | Direct identifier; exclude from shared extracts or use a project-specific token, with the key held separately. |
| `customers.csv` | `age` | Numeric, continuous | Personal/quasi-identifier; use broad age bands in shared data. |
| `customers.csv` | `signup_date` | Date | Personal/quasi-identifier; reduce precision or remove if unnecessary. |
| `customers.csv` | `province` | Categorical, nominal | Personal/quasi-identifier; coarsen or aggregate when linkage or small groups are possible. |
| `customers.csv` | `city_type` | Categorical, nominal | Personal/quasi-identifier; generalize or suppress where granular. |
| `customers.csv` | `gender` | Categorical, nominal | Personal information; restrict access and assess fairness implications. |
| `customers.csv` | `plan_type` | Categorical, nominal | Account/behavioral information; share only when needed and review combinations for small groups. |
| `customers.csv` | `payment_method` | Categorical, nominal | Account/financial-related information; minimize and restrict access. |
| `customers.csv` | `monthly_spend` | Numeric, continuous (ZAR) | Financial/account information; aggregate or band for sharing when precise values are unnecessary. |
| `customers.csv` or model label | `churned` | Binary categorical target | Account outcome; restrict to the authorized purpose and prevent target leakage. Confirm actual source table and definition. |
| `customers.csv` or related profile | `income_band` / income bands | Categorical, ordinal | Financial/demographic information; minimize, aggregate, and assess fairness. The source field name and location require confirmation. |
| `usage_monthly.csv` | `customer_id` | Foreign key / identifier | Direct identifier; tokenize consistently for authorized joins, then exclude from contractor extracts unless essential. |
| `usage_monthly.csv` | `billing_month` | Date / period | Behavioral timeline; share at month precision only when needed and review linkage risk. |
| `usage_monthly.csv` | `data_mb` | Numeric, continuous | Telecommunications usage information; minimize and aggregate where appropriate. |
| `usage_monthly.csv` | `voice_mins` | Numeric, continuous | Telecommunications usage information; minimize and aggregate where appropriate. |
| `support_tickets.csv` | `customer_id` | Foreign key / identifier | Direct identifier; tokenize consistently for authorized joins, then exclude from shared extracts unless essential. |
| `support_tickets.csv` | `ticket_id` | Identifier / key | Record identifier; remove or replace with a non-linkable project token before sharing. |
| `support_tickets.csv` | `ticket_category` | Categorical, nominal | Support interaction information; review rare categories and group small counts. |
| `support_tickets.csv` | `resolution_hours` | Numeric, continuous | Support interaction information; validate non-negative/positive rule against the documented definition; aggregate if sharing. |
| `support_tickets.csv` | `created_at` | Date-time | Behavioral timeline; generalize to month or remove if unnecessary. |
| `support_tickets.csv` | `resolved_at` | Date-time | Behavioral timeline; generalize to month or remove if unnecessary. |

## Sign-off before analysis

- [ ] Confirm every source file, table grain, field, type, permitted use, and key against the authoritative data dictionary.
- [ ] Record the study period, cutoff, quality rules, findings, and cleaning decisions.
- [ ] Confirm join keys and check unmatched foreign keys without deleting rows automatically.
- [ ] Document exclusions, transformations, and row counts; retain only authorized processed outputs.
- [ ] Review privacy and small-group risks before sharing data, plots, notebooks, or model outputs.
