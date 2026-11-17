# MzansiConnect Data Governance and POPIA Note

## Purpose and scope

This note sets minimum safeguards for the MzansiConnect churn and retention capstone. Records linkable to a person—including demographics, location, account information, telecommunications usage, and support interactions—must be handled as personal information under South Africa’s Protection of Personal Information Act (POPIA). The Phase 1 submission describes the dataset as synthetic; safeguards remain important if real or linkable data is introduced. This is an operational guide, not legal advice. The responsible organization should confirm its lawful basis, notices, and obligations before processing personal information.

## Collection, use, and access

Collect only fields needed for the stated analyses, and document each dataset’s source, purpose, permitted users, and study period. Keep raw files read-only in restricted `data/raw/`; use minimized, access-controlled working copies. Never put personal records or confidential exports in public Git history, notebooks, logs, or reports. Limit access to authorized members and use approved storage and transfer methods.

## External contractor checkpoint

Before sharing with an external contractor, remove direct identifiers such as `customer_id` or replace them with a project-specific token; keep the re-identification key separate. Generalize quasi-identifiers: band exact age, reduce dates to month or remove them, and coarsen province and `city_type` if combinations could identify someone. Check gender, plan, payment, financial, usage, and support fields for rare groups; suppress or aggregate them where needed. Share only necessary fields under documented purpose, access, retention, and deletion terms. Hashing is pseudonymization, not guaranteed anonymization, when other fields can be linked.

## Retention, quality, and lifecycle

Retain identifiable and transaction-level records only for an approved period tied to the project purpose and organizational requirements. The submission proposes up to 36 months after account termination for granular usage and support history; this is not a confirmed legal rule and must be approved before adoption. Then securely delete or irreversibly anonymize records, including backups and contractor copies, subject to applicable retention obligations.

## Ethical use and incident readiness

Review model performance and potential disparate impact across age, income, and regional groups where appropriate. False positives may prompt unwanted contact; false negatives may leave customers with service issues without support. Use predictions to guide human review, not as the sole basis for adverse treatment, and provide a way to correct inaccurate data. For suspected privacy incidents, restrict access and promptly notify the designated privacy contact to assess response and notification obligations.
