# MzansiConnect_CapstoneProject-

A collaboration project between five individuals from Shaper's Data Science Program.

## Phase 1: Kick-off, Data Fundamentals, and Data Governance

- [Project plan](docs/project_plan.md)
- [Data governance and privacy note](docs/data_governance_note.md)
- [Data quality checklist and provisional column inventory](docs/data_quality_checklist.md)
- Original Word package: [Phase 1 deliverables](MzansiConnect_Capstone_Phase_1_Deliverables.docx)
- Original Word package: [Phase 1 checkpoint questions](Checkpoint_Questions_Phase_1.docx)

### Phase 1 checkpoint questions

- **Which columns should be removed or masked before external sharing, and why?** Remove direct identifiers such as `customer_id` (or replace with a controlled random token where linkage is essential), along with names, contact details, account identifiers, and unnecessary free text. Generalize `age` and dates, coarsen `province` and `city_type`, suppress small groups, and review combinations that could re-identify a subscriber. Masking a key alone does not prevent linkage through quasi-identifiers.
- **Is churn classification or regression? What is the other framing?** Predicting whether an eligible subscriber churns within a defined window is binary classification (or a churn probability). A regression framing predicts a continuous outcome such as expected monthly revenue over the next quarter or time remaining until cancellation. The target and evaluation metric must match the business question.
