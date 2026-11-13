# ciandlithe-dlt-sources-carveout-v1 Specification

## Purpose

Codify the Q1 user-confirmed split between **cianchosaint** (the
defence / policing / intelligence-oversight OSINT platform) and
**ciandlithe** (the civil-litigation sister repo): evidence-collection
for law-enforcement purposes lives in cianchosaint; court-facing
procedural rules (court rules, judicial case management, civil
procedure, evidence law, family law procedure, criminal procedure,
tribunal procedure, inquest procedure) live in ciandlithe. This spec
covers the ciandlithe half: the `dlt_sources/_cross/jurisdiction_pipeline_base.py`
extension to add `STAGE = "law"` + the 8 per-jurisdiction `law/`
source families that own the court-facing procedural rules for the
8 British Isles jurisdictions.

## Requirements
### Requirement: CIANDLITHE is the canonical home for BI per-jurisdiction `law/` DLT sources

The CIANDLITHE sister repo SHALL own the 8 British-Isles per-jurisdiction
`law/` DLT sources as the canonical home for court-facing procedural rules.

#### Scenario: BI legal data canonical home

- **GIVEN** the parent change `2026-08-24-dlt-sources-to-multi-repo-scaffold-v1`
  defines the multi-repo scaffold (with ciandlíthe as the BI legal system
  sister repo per the user-confirmed split)
- **AND** the Phase 3.1 carve-out has moved the 8 BI per-jurisdiction
  `law/` sleds from cianfhoghlaim to ciandlíthe (per this change)
- **WHEN** a consumer queries the canonical BI legal data (statute,
  courts, WRC-equivalent) for any of the 8 BI jurisdictions
- **THEN** the consumer SHALL import from
  `ciandlithe.dlt_sources._cross.legal_registry` (the canonical home)
- **AND** the canonical home SHALL expose:
  - `bi_legal_registry_source(use_md: bool = True)` — the cross-cutting
    `@dlt.source` fan-out
  - `LegalRegistryJurisdictionPipeline` — the
    `JurisdictionPipelineBase` subclass with `STAGE = "legal_registry"`
  - `LegalCohortRow` — the canonical per-(jurisdiction, stage, subject,
    legal_source) row shape (Pydantic)
  - `BI_LEGAL_SOURCE_DEFAULTS` — the 8-tuple (statute, court, WRC) URL
    defaults for the 8 BI jurisdictions

#### Scenario: BI jurisdiction `law/` sleds are skeletons until Phase 3.2

- **GIVEN** the 8 BI per-jurisdiction `law/<jurisdiction>/_factory.py`
  modules in ciandlíthe are SKELETONS (the actual legislation crawler
  code stays in cianfhoghlaim at
  `dlt_sources/law/<jurisdiction>/british_isles/legislation.py` until
  Phase 3.2)
- **WHEN** the canonical `bi_legal_registry_source` is invoked today
- **THEN** the fan-out SHALL emit 0 rows (each per-jurisdiction
  `<jurisdiction>_law_source` returns an empty `iter([])`)
- **AND** the smoke test SHALL pass (imports succeed; no
  `ImportError`; no `ModuleNotFoundError`)

### Requirement: The 8 BI jurisdiction discriminator codes

The canonical `LegalCohortRow.jurisdiction` field SHALL be the
per-jurisdiction discriminator for the BI legal registry.

#### Scenario: 8 BI jurisdiction discriminator

- **GIVEN** the canonical `LegalCohortRow.jurisdiction` field is the
  per-jurisdiction discriminator
- **THEN** the discriminator SHALL be one of the 8 BI jurisdiction
  codes: `england`, `scotland`, `wales`, `northern_ireland`,
  `ireland`, `jersey`, `guernsey`, `isle_of_man`
- **AND** these 8 codes SHALL match the canonical
  `JurisdictionPipelineBase.VALID_JURISDICTIONS` tuple

### Requirement: Per-row carries 3 legal dimensions

Each `LegalCohortRow` SHALL carry 3 legal dimensions covering the
per-jurisdiction statute book, court system, and workplace-relations
commission.

#### Scenario: 3 legal dimensions per row

- **GIVEN** each `LegalCohortRow` carries 3 legal dimensions
- **THEN** the row SHALL include:
  - `statute_source: str` — the per-jurisdiction statutory-law URL
    (e.g. `https://www.legislation.gov.uk/` for UK,
    `https://www.irishstatutebook.ie/` for Ireland)
  - `court_source: str` — the per-jurisdiction court-system URL
    (e.g. `https://www.courts.ie/` for Ireland)
  - `wrc_source: str` — the per-jurisdiction workplace-relations URL
    (e.g. `https://www.workplacerelations.ie/` for Ireland)

### Requirement: Backward-compatibility shim in cianfhoghlaim

The system SHALL keep existing cianfhoghlaim callers working via the
shim at `dlt_sources/british_isles/_cross/legal_registry.py` with a
`DeprecationWarning` nudge.

#### Scenario: backward-compat shim in cianfhoghlaim

- **GIVEN** the cianfhoghlaim shim at
  `dlt_sources/british_isles/_cross/legal_registry.py`
- **WHEN** a cianfhoghlaim caller imports from the legacy path
  (`from dlt_sources.british_isles._cross.legal_registry import ...`)
- **THEN** the import SHALL succeed (lazy re-export from the
  ciandlíthe canonical home)
- **AND** the import SHALL emit a `DeprecationWarning` pointing to
  the ciandlíthe canonical home
- **AND** the migration message SHALL reference the post-carve-out
  report at
  `stedding/sync-reports/ciandlithe-initial-carveout-2026-08-25.md`

#### Scenario: per-PR reciprocal mirror

- **GIVEN** the parent change §15 (per-PR reciprocal mirror)
  defines the cross-repo sync contract
- **WHEN** a file in `dlt_sources/law/<jurisdiction>/*` or
  `dlt_sources/_cross/legal_registry.py` is changed in ciandlíthe
- **THEN** the per-PR reusable workflow
  (`.github/workflows/dlt-sister-sync-call.yml` in ciandlíthe) SHALL
  POST to the cianfhoghlaim reciprocal PR endpoint
- **AND** the reciprocal PR SHALL update the cianfhoghlaim
  `_sister_refs/ciandlithe/<path>` mirror
- **AND** the reciprocal PR SHALL be labeled
  `dlt-sister-sync, auto-mirror`

