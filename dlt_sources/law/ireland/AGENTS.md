# dlt_sources/law/ireland — Irish legal DLT sources

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change,
the per-jurisdiction ``law/`` sled was carved out of
``dlt_sources/british_isles/ireland/law/`` in cianfhoghlaim.

**Data lives in cianfhoghlaim until Phase 3.2 EU/CW carve-out.**
The Ireland legal corpus is the **richest** of the 8 BI jurisdictions —
8 separate OSINT sources at
`/Users/cianmacandeisigh/dev/cianfhoghlaim/dlt_sources/law/ireland/british_isles/`:

| File | Source | Status |
|---|---|---|
| `irish_statute_book.py` | irishstatutebook.ie ELI walker | TODO Phase 3.2 |
| `doj.py` | Department of Justice | TODO Phase 3.2 |
| `lawreform.py` | Law Reform Commission | TODO Phase 3.2 |
| `courts_ie.py` | Courts Service Ireland | TODO Phase 3.2 |
| `workplace_relations.py` | WRC + Employment Tribunal | TODO Phase 3.2 |
| `injuries_ie.py` | Personal Injuries Assessment Board | TODO Phase 3.2 |
| `citizensinformation.py` | Citizens Information | TODO Phase 3.2 |
| `gov_ie_law.py` | gov.ie legal | TODO Phase 3.2 |

## Files in this sled

- `__init__.py` — 1-line re-export of `ireland_law_source`.
- `_factory.py` — `JurisdictionPipelineBase` subclass with
  `STAGE = "law"`; exposes `ireland_law_source` binding.
- `sources.py` — placeholder for Phase 3.2 (will host the 8
  per-source `import` re-exports once they move into ciandlíthe).
- `schema.py` — re-export of the shared `BritishIslesLegislationRow`.
- `AGENTS.md` — this routing doc.

## Sister-repo sync contract

Per the parent change §15 (per-PR reciprocal mirror), a change to any
file in this directory triggers a reciprocal PR on cianfhoghlaim at
`dlt_sources/_sister_refs/ciandlithe/law/ireland/<file>`.