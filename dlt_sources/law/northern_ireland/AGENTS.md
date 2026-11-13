# dlt_sources/law/northern_ireland — Northern Ireland legal DLT sources

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change,
the per-jurisdiction ``law/`` sled was carved out of
``dlt_sources/british_isles/northern_ireland/law/`` in cianfhoghlaim.

**Data lives in cianfhoghlaim until Phase 3.2 EU/CW carve-out.**
Real legislation crawler code:
`/Users/cianmacandeisigh/dev/cianfhoghlaim/dlt_sources/law/northern_ireland/british_isles/legislation.py`

Northern Ireland uses UK statute + some Scottish law via the Good
Friday Agreement.

## Files in this sled

- `__init__.py` — 1-line re-export of `northern_ireland_law_source`.
- `_factory.py` — `JurisdictionPipelineBase` subclass with
  `STAGE = "law"`; exposes `northern_ireland_law_source` binding.
- `sources.py` — placeholder for Phase 3.2.
- `schema.py` — re-export of the shared `BritishIslesLegislationRow`.
- `AGENTS.md` — this routing doc.

## Sister-repo sync contract

Per the parent change §15 (per-PR reciprocal mirror), a change to any
file in this directory triggers a reciprocal PR on cianfhoghlaim at
`dlt_sources/_sister_refs/ciandlithe/law/northern_ireland/<file>`.