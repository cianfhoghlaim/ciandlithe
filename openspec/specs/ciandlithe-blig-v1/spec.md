# ciandlithe-blig-v1 Capability

## Purpose

`ciandlithe-blig-v1` is the **British Isles Law Intelligence Graph (BLIG v1)** — the umbrella spec for ciandlithe's cross-domain intelligence graph that composes the BLIP v1 (civil-litigation) vertical with the BIPP v2 (political-accountability) vertical.

The BLIG v1 enables a self-rep claimant's medical-malpractice case (per the BLIP v1) to be cross-referenced with related political-accountability context (per the BIPP v2) — e.g. the sodium-Qvalproate HSE investigation (per the ciandlithe composite pilot) is politically covered up (per the BIPP v2 ROI political accountability cohort).

## Background

The 7 ciandlithe composite pilots (per `docs/case-study/composite-pilot.md`) cover:
1. QUB / Royal Victoria Hospital brain-injury (medical_malpractice, NI)
2. Eric employer / breach of contract (employer_breach, Cross-border)
3. Garda discrimination / data-access (garda_discrimination, ROI)
4. DkIT disability / education complaint (education_discrimination, ROI)
5. NUIG / UoG rejection + abuse of power (education_discrimination, ROI)
6. UCL offer / DBS (admission_breach, England)
7. Sodium valproate / HSE misprescription (medical_malpractice, ROI)

The new ciandlithe BLIG v1 graph cross-references these 7 composite pilots with the corresponding BIPP v2 political-accountability cohorts (per the new BIPP v2 vertical in cianchosaint).

## Requirements

### Requirement: The cross-domain intelligence graph

The system SHALL provide the BLIG v1 graph that composes the BLIP v1 + BIPP v2 verticals.

#### Scenario: The sodium valproate composite pilot cross-references the ROI political accountability cohort

- **WHEN** the operator invokes the composite pilot FunctionTool for `pilot-sodium-valproate`
- **THEN** the dossier SHALL include a `related_political_accountability_context` field referencing the BIPP v2 ROI political accountability cohort
- **AND** the dossier SHALL include cross-references to the `fine_gael_coalition_strategy_analysis.pdf` + `varadkar_controversies_and_political_future.pdf` + `galway_by_election_media_analysis.pdf` leabharlann PDFs

#### Scenario: The Garda discrimination composite pilot cross-references the Garda data-access sub-cohort

- **WHEN** the operator invokes the composite pilot FunctionTool for `pilot-garda`
- **THEN** the dossier SHALL include cross-references to the BIPP v2 NI political accountability cohort (the Sinn Féin funding inquiry)

## Cross-references

- [`../../../cianchosaint/openspec/specs/cianchosaint-bipp-v2/spec.md`](../../../cianchosaint/openspec/specs/cianchosaint-bipp-v2/spec.md) — the BIPP v2 vertical
- [`../ciandlithe-pipeline/spec.md`](../../specs/ciandlithe-pipeline/spec.md) — the BLIP v1 pipeline
- [`../../docs/case-study/composite-pilot.md`](../../docs/case-study/composite-pilot.md) — the canonical pilot narrative