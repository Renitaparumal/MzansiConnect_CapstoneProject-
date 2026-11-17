# MzansiConnect Data Governance and POPIA Note

## Purpose and scope

The Phase 1 brief describes the dataset as synthetic, but source CSVs have not been supplied. Records relating to an identified or identifiable person are personal information under South Africa's Protection of Personal Information Act (POPIA). Confirm lawful basis, notices, and obligations before processing real or linkable data; this note is operational guidance, not legal advice.

## Data lifecycle, collection, storage, and access

Source systems are unconfirmed. Customer/account fields may come from a CRM or billing system, usage and dropped-call complaints from network/service systems, and tickets or satisfaction scores from a call-centre platform. Confirm provenance, purpose, period, and permitted use with the data owner.

Collect only needed fields. Preserve authorized originals read-only in restricted `data/raw/`; store minimized working copies and the project database in access-controlled `data/processed/`. Use approved encrypted storage/transfer, protect credentials separately, and keep personal records out of Git, notebooks, logs, and public reports. The data owner approves access; authorized data scientists handle row-level records; stakeholders receive minimized aggregates. Log access and material transformations.

## Personal information and external sharing

Direct identifiers include `customer_id` and `ticket_id`, including foreign-key copies. Quasi-identifiers include `age`, `signup_date`, `province`, `city_type`, and combinations of demographic, plan, device, income, and referral fields. Payment, revenue, usage, complaint, ticket, cancellation, resolution, and satisfaction fields reveal account or behavioral details when linked to a person; `churned` is also a personal account outcome. Restrict these fields when linkable.

Before contractor sharing, remove identifiers or use project-specific tokens; keep any re-identification key separately. Hashing/tokenization is pseudonymization, not guaranteed anonymization. Band age/income, reduce date precision, coarsen location, and aggregate rare categories. Exclude unnecessary fields, especially post-outcome `cancellation_reason` and the target. Assess combinations for re-identification risk and document purpose, access, retention, and deletion terms.

## Retention and ethical use

Retain identifiable or transaction-level records only as long as needed for the purpose and applicable requirements. The Phase 1 submission proposes up to 36 months after account termination for granular usage/support history; this is not a confirmed POPIA rule and requires data-owner approval. Then securely delete or irreversibly anonymize records, backups, and contractor copies, subject to retention obligations.

A false positive may prompt unwanted contact; a false negative may leave a customer with service problems without support. Review performance across age, income, and regional groups. Use predictions to inform human review, not as the sole basis for adverse decisions, and allow correction of inaccurate data. For suspected incidents, restrict access and notify the privacy contact promptly.
