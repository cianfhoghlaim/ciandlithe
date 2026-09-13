# Spec: `ciandlithe-dlt-sources-split` — the per-jurisdiction DLT source carve-out contract

> **Parent change**: [`2026-08-24-dlt-sources-to-multi-repo-scaffold-v1`](../../../../../2026-08-24-dlt-sources-to-multi-repo-scaffold-v1/proposal.md)
> **Companion plan**: [`openspec/plans/2026-08-24-dlt-deep-analysis-v2.md`](../../../../../../openspec/plans/2026-08-24-dlt-deep-analysis-v2.md) §Phase 2.1
> **Capability spec**: this is a **CAPABILITY** spec (per the openspec convention), describing the end state of the dlt source carve-out into ciandlithe.
> **Status**: PLACEHOLDER (per the init change §13.3) — the actual end-state contract is documented in the per-sister canonical spec at `openspec/specs/ciandlithe-architecture/spec.md` (added by the init change).

## Purpose

This spec captures the **end state** that the Phase 3 carve-out (per parent change §21.1) must produce:

1. **Per-jurisdiction DLT sources** for the BI legal-system slice (WRC + UK statute + courts + tribunals + regulators + ombudsmen + law societies + bar councils + legal-aid bodies + coroners + health-service complaints bodies + claimant-representation clinics) live in `dlt_sources/ciandlithe/`.

2. **The `_cross/` base class** (`dlt_sources/ciandlithe/_cross/jurisdiction_pipeline_base.py`) re-exports `JurisdictionPipelineBase` from `cianfhoghlaim.dlt_sources.british_isles._cross.jurisdiction_pipeline_base` (per parent change §11). The ciandlithe copy is a stand-in until the cross-repo import surface is wired.

3. **The `common/` helpers** (`dlt_sources/ciandlithe/common/`) re-export the 4 canonical helpers (`endpoint_recovery`, `firecrawl_source`, `http_client`, `destinations_cianfhoghlaim`) from `cianfhoghlaim.dlt_sources.common`. The ciandlithe copy is a stand-in until the cross-repo import surface is wired.

4. **The 6 cascade contracts** (per parent change §15-§19 + the v2 plan §C.6) are wired into the ciandlithe CI/CD + the cross-repo mirror path.

## Background

Per `openspec/plans/2026-08-24-dlt-deep-analysis-v2.md` §0.1, the Cianfhoghlaim `dlt_sources/` subtree currently carries 919 `@dlt.source` + 1,244 `@dlt.resource` across 34 subtrees under one roof. The Phase 2.1 multi-repo scaffold splits these into 4+ sister repos (tuatha + ciandlithe + cianchosaint + future ciancheiltis), each owning a vertical. ciandlithe owns the **BI legal-system** vertical per the user-confirmed split (per the parent change proposal §"Why" + the bilingual carve rule).

## ADDED Requirements

### Requirement: Per-jurisdiction DLT sources live under `dlt_sources/ciandlithe/<cohort>/<sub-nation>/<source>.py`

The system SHALL organise the BI legal-system dlt sources into the `dlt_sources/ciandlithe/` namespace, mirroring the existing `dlt_sources/cianchosaint/<vertical>/<jurisdiction>/<source>.py` pattern.

#### Scenario: An agent adds a new DLT source for the Irish Courts Service

- **WHEN** the agent creates `dlt_sources/ciandlithe/ireland/courts/courts_ie_judgments.py` with a `@dlt.source` factory
- **THEN** the source is auto-importable via `from dlt_sources.ciandlithe.ireland.courts.courts_ie_judgments import courts_ie_judgments_source`
- **AND** the source's URL is verified against `dlt_sources/ciandlithe/common/osint_allowlist.yaml` by `mise run lint:license`

### Requirement: The `JurisdictionPipelineBase` re-export lives at `dlt_sources/ciandlithe/_cross/jurisdiction_pipeline_base.py`

The system SHALL re-export `JurisdictionPipelineBase` from `cianfhoghlaim.dlt_sources.british_isles._cross.jurisdiction_pipeline_base` via the `dlt_sources/ciandlithe/_cross/__init__.py` module. Until the cross-repo import surface is wired (deferred to a follow-up change), the ciandlithe local copy is the canonical reference.

#### Scenario: A ciandlithe DLT source extends `JurisdictionPipelineBase`

- **WHEN** the agent writes `from dlt_sources.ciandlithe._cross.jurisdiction_pipeline_base import JurisdictionPipelineBase`
- **THEN** the import succeeds via the local ciandlithe copy OR the cross-repo `cianfhoghlaim.dlt_sources.british_isles._cross.jurisdiction_pipeline_base` import (the canonical Phase 1.3 base class per parent change §11)
- **AND** the merged base class API surface is identical (same `__init__` signature + same `build_pipeline_resource()` override + same `run_smoke()` + same `abort_failed_load_packages()` + same `fail_pending_job_and_retry()` + same `_tenacity_retry_context()`)

### Requirement: The `common/` helpers re-export from cianfhoghlaim

The system SHALL re-export the 4 canonical helpers (`endpoint_recovery`, `firecrawl_source`, `http_client`, `destinations_cianfhoghlaim`) from `cianfhoghlaim.dlt_sources.common` via the `dlt_sources/ciandlithe/common/__init__.py` module. Until the cross-repo import surface is wired, the ciandlithe local copies are the canonical reference.

#### Scenario: A ciandlithe DLT source imports a common helper

- **WHEN** the agent writes `from dlt_sources.ciandlithe.common.endpoint_recovery import retry_with_jitter`
- **THEN** the import succeeds via the local ciandlithe copy OR the cross-repo `cianfhoghlaim.dlt_sources.common.endpoint_recovery` import

## MODIFIED Requirements

None (the spec is additive; the parent change §15-§19 modifications are tracked in those changes).

## REMOVED Requirements

None.

## Out of scope (follow-up changes)

- The actual Phase 3 carve-out (the per-jurisdiction file moves from `cianfhoghlaim/dlt_sources/...` to `ciandlithe/dlt_sources/ciandlithe/<cohort>/<sub-nation>/<source>.py`) — `2026-09-XX-ciandlithe-initial-carveout-v1` (parent change §21.1)
- The cross-repo import surface wire-up (`from cianfhoghlaim.dlt_sources.british_isles._cross.jurisdiction_pipeline_base import JurisdictionPipelineBase`) — `2026-09-XX-ciandlithe-uv-workspace-v1`
- The 6 cascade contracts (parent change §15-§19) — wired AFTER the GitHub repo exists

## Cross-references

- [`../ciandlithe-architecture/spec.md`](../ciandlithe-architecture/spec.md) — the per-sister canonical spec (the end-state architecture)
- [`../../../../cianfhoghlaim-dlt-sources-multi-repo/spec.md`](../../../../cianfhoghlaim-dlt-sources-multi-repo/spec.md) — the parent 8-repo topology spec
- [`../../../../../tuatha-british-isles-mmo/spec.md`](../../../../../tuatha-british-isles-mmo/spec.md) — the tuatha precedent
- [`../../../../../../openspec/plans/2026-08-24-dlt-deep-analysis-v2.md`](../../../../../../openspec/plans/2026-08-24-dlt-deep-analysis-v2.md) — the v2 plan