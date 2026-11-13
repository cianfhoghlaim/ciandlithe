# `ciandlithe-architecture` — the per-sister canonical spec

> **Parent change**: [`2026-08-24-dlt-sources-to-multi-repo-scaffold-v1`](../../../2026-08-24-dlt-sources-to-multi-repo-scaffold-v1/proposal.md) §13
> **Companion plan**: [`openspec/plans/2026-08-24-dlt-deep-analysis-v2.md`](../../../../../openspec/plans/2026-08-24-dlt-deep-analysis-v2.md) §Phase 2.1
> **Capability spec**: ARCHITECTURE (end-state) — describes what the ciandlithe sister repo looks like once the Phase 3 carve-out (parent change §21.1) + the 6 cascade contracts (parent change §15-§19) land.
> **Status**: PLACEHOLDER — the per-sister canonical spec is added by the init change (`2026-08-24-ciandlithe-init-v1` §V.5). The full Requirements + Scenarios land in the Phase 3 carve-out change (`2026-09-XX-ciandlithe-initial-carveout-v1`).

## Purpose

The ciandlithe sister repo owns the **BI legal-system vertical**: courts, tribunals, regulators, ombudsmen, law societies, bar councils, legal-aid bodies, coroners, health-service complaints bodies, and registered claimant-representation clinics of the Republic of Ireland, the United Kingdom of Great Britain and Northern Ireland (including the devolved administrations of Scotland, Wales, and Northern Ireland), and the Crown Dependencies (Jersey, Guernsey, Isle of Man).

## Background

Per `openspec/changes/2026-08-25-tuatha-british-isles-mmo-consolidation-v1/` (the tuatha precedent) + the parent change §13, the dlt-sources multi-repo scaffold splits the Cianfhoghlaim `dlt_sources/` subtree into 4+ sister repos. Each sister repo adopts the canonical shape:

```
<repo>/
├── pyproject.toml          # uv workspace member, depends on cianfhoghlaim
├── mise.toml               # <repo>:<verb>:* task namespace
├── README.md
├── AGENTS.md
├── LICENSE
├── openspec/{AGENTS.md, specs/, changes/}
├── dlt_sources/{_cross/, common/, <vertical>/}
├── baml/<category>/<file>.baml
├── dagster/<file>.py
├── cocoindex/_lifespan.py + Apps
├── notebooks/<file>.ipynb
├── tests/dlt/test_imports.py + tests/<area>/
├── ci/README.md
└── docs/{AGENTS.md, architecture.md}
```

ciandlithe follows this shape. The `<vertical>` directory is `law/` (per the prompt spec) — though the existing standalone implementation uses `dlt_sources/ciandlithe/<cohort>/<sub-nation>/<source>.py` as the per-jurisdiction naming convention. The `law/` directory is the FUTURE organisation (Phase 3 onward); the existing `ciandlithe/<cohort>/<sub-nation>/<source>.py` layout is preserved per the existing ciandlithe-repo-foundation-v1 change.

## ADDED Requirements

### Requirement: ciandlithe is a uv workspace member that depends on cianfhoghlaim

The system SHALL declare `pyproject.toml [tool.uv.sources]` pointing to `../../cianfhoghlaim` (the canonical uv workspace member reference).

#### Scenario: A developer runs `uv sync` in ciandlithe

- **WHEN** the developer runs `cd /Users/cianmacandeisigh/dev/ciandlithe && uv sync`
- **THEN** uv resolves the `cianfhoghlaim` workspace member dependency from `../../cianfhoghlaim`
- **AND** the developer can `import cianfhoghlaim` from any ciandlithe Python process

> **NOTE**: The current ciandlithe pyproject.toml is explicitly standalone (per its comment block at lines 96-108 — the cross-repo source map was REMOVED per Q24 of the bootstrap-v2 plan). The transition to a uv workspace member dependency is a follow-up change; this spec documents the FUTURE state.

### Requirement: ciandlithe's mise tasks use the `ciandlithe:<verb>:*` namespace

The system SHALL declare `mise.toml [tasks."ciandlithe:<verb>"]` for every per-sister task. Per the prompt spec: `ciandlithe:test` + `ciandlithe:lint` + `ciandlithe:typecheck` + `ciandlithe:openspec-validate` + `ciandlithe:smoke-all`.

#### Scenario: A developer runs `mise tasks ls | grep '^ciandlithe:'`

- **WHEN** the developer runs `cd /Users/cianmacandeisigh/dev/ciandlithe && mise tasks ls | grep '^ciandlithe:'`
- **THEN** the output includes at minimum: `ciandlithe:test`, `ciandlithe:lint`, `ciandlithe:typecheck`, `ciandlithe:openspec-validate`, `ciandlithe:smoke-all`

> **NOTE**: The current ciandlithe mise.toml uses a richer namespace (`ciandlithe:provider:*` + `ciandlithe:browser-tool:*` + `ciandlithe:osint:*` + `ciandlithe:blip:v1:*` + `ciandlithe:ccc:*` + `ciandlithe:web:*` etc.) which SUPERSETS the prompt spec. The smoke-all alias maps to `mise run test:smoke` (the existing convention).

### Requirement: ciandlithe has its own openspec AGENTS.md + canonical specs

The system SHALL host `openspec/AGENTS.md` (per-repo openspec conventions) + `openspec/specs/` (per-sister canonical specs).

#### Scenario: A developer validates the ciandlithe openspec surface

- **WHEN** the developer runs `cd /Users/cianmacandeisigh/dev/ciandlithe && mise run openspec:validate-all`
- **THEN** every openspec change + every canonical spec validates with `--strict`

### Requirement: ciandlithe hosts the 6 cascade contracts per parent change §15-§19

The system SHALL participate in:
1. **`dlt-sister-sync-reusable-workflow`** — `.github/workflows/dlt-sister-sync-call.yml` calls cianfhoghlaim's reusable workflow
2. **`cognee-twin-clusters`** — 6 ciandlithe_* Cognee clusters
3. **`dlt-nightly-mirror-merge`** — ciandlithe emits `_sister_refs/ciandlithe/...` diffs
4. **`dlt-destination-versioning-contract`** — pins `cianfhoghlaim >=<minor>,<<next-minor`
5. **`agent-observability-ciandlithe`** — `ciandlithe_*` Langfuse project + project-scoped API key
6. **`openspec-per-sister-sync`** — per-sister `openspec/AGENTS.md` + `openspec/specs/` (this spec)

#### Scenario: A PR on ciandlithe/dlt_sources/_cross/__init__.py opens a reciprocal PR on cianfhoghlaim/dlt_sources/_sister_refs/ciandlithe/_cross/__init__.py

- **WHEN** the agent opens a PR on ciandlithe that touches `dlt_sources/_cross/__init__.py`
- **THEN** the `dlt-sister-sync-call.yml` workflow invokes cianfhoghlaim's `dlt-sister-sync.yml` reusable workflow
- **AND** a reciprocal PR opens on cianfhoghlaim targeting `dlt_sources/_sister_refs/ciandlithe/_cross/__init__.py`

## MODIFIED Requirements

None (the spec is additive).

## REMOVED Requirements

None.

## Cross-references

- [`../../specs/ciandlithe-pipeline/spec.md`](../../specs/ciandlithe-pipeline/spec.md) — the existing umbrella BLIP v1 spec
- [`../../../changes/2026-08-24-ciandlithe-init-v1/specs/ciandlithe-dlt-sources-split/spec.md`](../../../changes/2026-08-24-ciandlithe-init-v1/specs/ciandlithe-dlt-sources-split/spec.md) — the per-jurisdiction DLT source carve-out contract
- [`../../../../../../openspec/plans/2026-08-24-dlt-deep-analysis-v2.md`](../../../../../../openspec/plans/2026-08-24-dlt-deep-analysis-v2.md) — the v2 plan
- [`../../../../../tuatha-british-isles-mmo/spec.md`](../../../../../tuatha-british-isles-mmo/spec.md) — the tuatha precedent spec
- [`../../../2026-08-25-tuatha-british-isles-mmo-consolidation-v1/`](../../../2026-08-25-tuatha-british-isles-mmo-consolidation-v1/) — the precedent openspec change