# ciandlithe-langfuse-prompt-mirror Capability

## Purpose

`ciandlithe-langfuse-prompt-mirror` is the mirror Langfuse v3 prompt management capability for the ciandlithe platform. It mirrors the cianchosaint `cianchosaint-langfuse-prompt-management` spec but knows about the 15 ciandlithe-specific canonical prompt names (the per-cohort BAML extraction functions).

This is a **mirror**, not a wholesale-copy: the resolver lives in BOTH repos, the pattern is identical, but the canonical prompt names differ (ciandlithe has 15 names; cianchosaint has 21 names).

## Background

Per the `openspec/changes/ciandlithe-repo-foundation-v1/proposal.md`:
> "The ciandlithe BAML extraction schemas are a subset of the cianchosaint ones"

The ciandlithe BAML extraction functions are:
- `ExtractCompositePilotDossier` (the composite pilot)
- `ExtractCourtForm` + `ExtractCourtFee` (per the ROI/law wholesale-copy)
- `ExtractJudgement` (per the ROI/law wholesale-copy)
- `ExtractCourtRule` (per the ROI/law wholesale-copy)
- `ExtractPIABPage` (per the ROI/law wholesale-copy)
- `ExtractLegalAidPage` (per the ROI/law wholesale-copy)
- `ExtractHSEIncidentReport` (the HSE extraction — planned for `ciandlithe-blig-v1-spec-v1`)
- `ExtractCoronerInquestFinding` (the coroner extraction — planned)
- `ExtractNHSIncidentReport` (the NHS extraction — planned)
- `ExtractGMCFTPANDecision` (the GMC extraction — planned)
- `ExtractDailyCourtList` (the daily court list extraction — planned)
- `ExtractCourtJudgment` (the cross-jurisdiction court judgment extraction — planned)
- `ExtractLegalCaseProfile` (the umbrella record — planned)
- `ExtractPoliticalGraphRelationship` (the BLIG v1 political-accountability extraction — planned)

= 15 canonical prompt names.

## Requirements

### Requirement: The mirror `LangfusePromptResolver` class

The system SHALL provide a `LangfusePromptResolver` class at `baml_src/_shared/langfuse_prompt_resolver.py` with the SAME circuit-breaker + graceful-fallback pattern as cianchosaint + 15 ciandlithe-specific canonical prompt names.

#### Scenario: The ciandlithe resolver has 15 canonical prompt names

- **WHEN** the operator runs `LangfusePromptResolver.canonical_prompt_names()` in ciandlithe
- **THEN** the result SHALL include exactly the 15 names listed in §Purpose (no more, no less)
- **AND** SHALL NOT include any cianchosaint-specific names (e.g. `extract_reform_uk_dossier`, `extract_psni_record`, etc.)

#### Scenario: The mirror resolver falls back to inline BAML prompts

- **WHEN** the operator invokes `resolver.resolve(prompt_name="extract_composite_pilot_dossier")`
- **AND** LANGFUSE_PUBLIC_KEY is empty
- **THEN** the resolver SHALL return a `LangfusePromptHit` with `fallback_used=True`
- **AND** SHALL log `langfuse_not_configured_using_fallback`

#### Scenario: The mirror resolver opens the circuit-breaker after 3 consecutive failures

- **WHEN** the resolver records 3 consecutive `record_failure()` calls
- **THEN** the circuit-breaker SHALL transition to `is_open=True`
- **AND** SHALL skip the Langfuse call on the next invocation

### Requirement: Cross-repo sync with cianchosaint

The system SHALL be the **mirror** of the cianchosaint `cianchosaint-langfuse-prompt-management` spec — same pattern, different canonical prompt names.

#### Scenario: The ciandlithe resolver shares the same circuit-breaker constants as cianchosaint

- **WHEN** the operator inspects `langfuse_prompt_resolver.py` in ciandlithe
- **THEN** the `CIRCUIT_BREAKER_THRESHOLD` SHALL be 3 (matching cianchosaint)
- **AND** the `CIRCUIT_BREAKER_RESET_SECONDS` SHALL be 60 (matching cianchosaint)

#### Scenario: The ciandlithe resolver has different LANGFUSE_HOST than cianchosaint

- **WHEN** the operator inspects the default `LANGFUSE_HOST`
- **THEN** it SHALL be `https://langfuse.ciandlithe.ie` (NOT `https://langfuse.cianchosaint.ie`)

## Cross-references

- [`../../baml_src/_shared/langfuse_prompt_resolver.py`](../../baml_src/_shared/langfuse_prompt_resolver.py) — the canonical mirror resolver
- [`../../../cianchosaint/baml_src/_shared/langfuse_prompt_resolver.py`](../../../cianchosaint/baml_src/_shared/langfuse_prompt_resolver.py) — the cianchosaint upstream
- [`../../baml_src/ciandlithe/case_studies/reform_civil_suit_dossier.baml`](../../baml_src/ciandlithe/case_studies/reform_civil_suit_dossier.baml) — the ciandlithe composite pilot BAML
- [`../../baml_src/ciandlithe/ireland/law/`](../../baml_src/ciandlithe/ireland/law/) — the wholesale-copied ROI/law BAML files