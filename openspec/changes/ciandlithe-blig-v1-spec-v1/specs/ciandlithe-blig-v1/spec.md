## ADDED Requirements

### Requirement: The cross-domain intelligence graph

The system SHALL provide the BLIG v1 graph that composes the BLIP v1 + BIPP v2 verticals.

#### Scenario: The sodium valproate composite pilot cross-references the ROI political accountability cohort

- **WHEN** the operator invokes the composite pilot FunctionTool for `pilot-sodium-valproate`
- **THEN** the dossier SHALL include a `related_political_accountability_context` field referencing the BIPP v2 ROI political accountability cohort

#### Scenario: The Garda discrimination composite pilot cross-references the Garda data-access sub-cohort

- **WHEN** the operator invokes the composite pilot FunctionTool for `pilot-garda`
- **THEN** the dossier SHALL include cross-references to the BIPP v2 NI political accountability cohort