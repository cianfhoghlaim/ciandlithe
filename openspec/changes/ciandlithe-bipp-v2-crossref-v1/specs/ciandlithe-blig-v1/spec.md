## ADDED Requirements

### Requirement: The BIPP v2 cross-reference resolver

The system SHALL provide a `BippV2CrossrefResolver` class at `baml_src/ciandlithe/processing/bipp_v2_crossref.py`.

#### Scenario: The 7 ciandlithe composite pilots cross-reference the 7 BIPP v2 cohorts

- **WHEN** the operator invokes `BippV2CrossrefResolver().resolve_related_cohort("pilot-sodium-valproate")`
- **THEN** the method SHALL return a `BippV2CohortReference` with the BIPP v2 cohort id `roi_political_accountability`