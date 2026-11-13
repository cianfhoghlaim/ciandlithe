# dlt_sources/law/england — England & Wales legal DLT sources

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change,
the per-jurisdiction ``law/`` sled was carved out of
``dlt_sources/british_isles/england/law/`` in cianfhoghlaim into the
dedicated ciandlíthe sister-repo ``dlt_sources/law/<jurisdiction>/``
layout.

**Data lives in cianfhoghlaim until Phase 3.2 EU/CW carve-out.**
The real legislation crawler code is at
`/Users/cianmacandeisigh/dev/cianfhoghlaim/dlt_sources/law/england/british_isles/legislation.py`
(the per-domain-folder layout created by the
``2026-08-24-wave-1-dlt-sources-domain-restructure-v1`` wave-1
restructure). This directory is the skeleton home for it in
ciandlíthe.

## Files in this sled

- `__init__.py` — canonical 1-line re-export of `england_law_source`.
- `_factory.py` — `JurisdictionPipelineBase` subclass with
  `STAGE = "law"`; exposes `england_law_source` binding.
- `sources.py` — placeholder for Phase 3.2 per-resource defs.
- `schema.py` — `BritishIslesLegislationRow` Pydantic model
  (the per-act row shape used by all 8 BI jurisdictions).
- `AGENTS.md` — this routing doc.

## Why SKELETON

The Phase 3.2 EU/CW carve-out (Subagent Q) is being done in parallel
and will move the European + Commonwealth legislation sources into
ciandlíthe as a parallel `dlt_sources/law/<region>/<jurisdiction>/`
top-level layout. Until then the per-jurisdiction law pipeline is a
no-op `iter([])` so the smoke test imports succeed today.

## Sister-repo sync contract

Per the **2026-08-24-dlt-sources-to-multi-repo-scaffold-v1** parent
change §15 (per-PR reciprocal mirror), a change to any file in this
directory will trigger a reciprocal PR on cianfhoghlaim at
`dlt_sources/_sister_refs/ciandlithe/law/england/<file>`.