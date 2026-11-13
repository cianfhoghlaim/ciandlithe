# Change: ciandlithe-leabharlann-corpus-ingest-v1

## Why

The `leabharlann/gemini_deep_research/law/` (59 PDFs) +
`leabharlann/gemini_deep_research/medical/` (54 PDFs) = **113 PDFs,
~40 MB** are the canonical source-of-truth for every ciandlithe
case-study pilot. Today `case_study_loader.py` only calls
`path.exists()` + `stat().st_size` — nothing is ever parsed. This blocks
every downstream capability:

- No text extraction → no BAML extraction → no entities / dates /
  statutes / citations
- No chunks → no BGE-M3 embeddings → no LanceDB table → no hybrid RAG
- No structured events → no temporal graph (WO-4)
- No cohort mapping → no timeline visualiser (WO-6)
- No chronology → no limitation-period overlay (WO-5)

In particular, **96 of the 113 PDFs are unreferenced anywhere in the
code or docs** — they exist as inert deep-research artefacts. They may
contain material the user has forgotten about.

This change builds the corpus ingestion pipeline end-to-end: PyMuPDF
text extraction + regex/heuristic structured extraction + chunking +
BGE-M3 embeddings + LanceDB table + cohort classifier.

## What changes

- **NEW modules** at `cocoindex_flows/ciandlithe/corpus/`:
  - `_pdf_text.py` — PyMuPDF extraction returning page-anchored spans
    `{page, char_start, char_end, text}`. Deterministic. No OCR.
  - `_classifier.py` — map each PDF → `(cohort, jurisdiction, case_cluster)`
    using filename + first-2-pages heuristics. Unresolvable → `cohort="unclassified"` review queue.
  - `leabharlann_law_flow.py` — CocoIndex v1 app for the 59 law PDFs
  - `leabharlann_medical_flow.py` — CocoIndex v1 app for the 54 medical PDFs
  - `__init__.py` — module exports

- **NEW BAML files** at `baml_src/ciandlithe/corpus/` (using the older
  BAML 0.222.0-compatible syntax — the existing ireland/law/*.baml files
  use a newer syntax that doesn't generate with the installed BAML version;
  these new files use the simpler `client "Primary"` form):
  - `research_doc_extraction.baml`
  - `case_chronology_extraction.baml`
  - `legal_entity_extraction.baml`

  **These BAML files are declared but **not** invoked by WO-1** — the
  corpus pipeline uses Python regex + heuristics in WO-1 to avoid
  requiring live LLM calls + the BAML syntax upgrade. The BAML
  functions become the load-bearing extraction layer in a later change
  (post-WO-9) when Langfuse prompt management + the ciandlithe-specific
  RAGAS eval pipeline are wired.

- **MODIFIED** `dlt_sources/ciandlithe/cross/case_study_loader.py` — the
  loader now extracts text + writes to a `leabharlann_cache` LanceDB
  table (preserves the existing public function signatures so
  `tests/smoke/test_ciandlithe.py` keeps passing).

- **NEW** `tests/smoke/test_leabharlann_corpus.py` — asserts all 113
  PDFs are present on disk + yields non-empty text + every PDF is
  classified (or in `unclassified` review queue).

- **NEW openspec artifacts**:
  - `proposal.md` (this file)
  - `tasks.md`
  - `cross-repo-sync.md`
  - `specs/ciandlithe-leabharlann-corpus/spec.md` (the spec delta)
- **NEW canonical spec** `openspec/specs/ciandlithe-leabharlann-corpus/`
  containing `spec.md` + `AGENTS.md` (≤30 lines).

## Impact

- Affected specs: **1 NEW spec** (`ciandlithe-leabharlann-corpus`).
- Affected code/config: ~7 NEW files (4 corpus flows + 3 BAML files)
  + 1 MODIFIED loader + 1 NEW test.
- Subsequent changes depend on this: every WO that ingests / searches
  / embeds the corpus (WO-4 temporal graph, WO-6 timeline visualiser,
  WO-9 orchestration, WO-12 runbook examples).

## Out of scope (follow-up changes)

- BAML-driven structured extraction (vs the WO-1 regex/heuristic path)
  — gated by an LLM API + the BAML syntax upgrade + Langfuse wiring.
- Live LLM calls — gated by credentials + the 4-tier provider chain.
- Cross-jurisdiction legal entity resolution — belongs in the Graphiti
  graph (WO-4).

## Dependencies

`Blocked by: ciandlithe-toolchain-repair-v1` (archived).
`Blocked by (soft): leabharlann/gemini_deep_research/{law,medical}/`
(read-only source material — 113 PDFs, ~40 MB).
`Affected repos: ciandlithe.`

## Cross-repo sync

This change touches ONLY the `ciandlithe` repo. `leabharlann` is
read-only. `cianchosaint` and `cianfhoghlaim` are not touched.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/ciandlithe
openspec validate ciandlithe-leabharlann-corpus-ingest-v1 --strict
openspec validate --all --strict
mise run lint
uv run --isolated --python 3.12 --with pymupdf --with pyyaml --with pytest \
  python -m pytest tests/smoke/test_leabharlann_corpus.py -v
uv run --isolated --python 3.12 --with pymupdf python -m cocoindex_flows.ciandlithe.corpus.leabharlann_law_flow --dry-run
uv run --isolated --python 3.12 --with pymupdf python -m cocoindex_flows.ciandlithe.corpus.leabharlann_medical_flow --dry-run
```

Real exit codes required. Paste real output in the commit message.