# ciandlithe-leabharlann-corpus Capability

## Purpose

`ciandlithe-leabharlann-corpus` is the load-bearing pipeline that ingests
all 113 leabharlann Gemini Deep Research PDFs (59 law + 54 medical) into
a queryable form. PyMuPDF extracts text; a regex/heuristic classifier
maps each PDF to a cohort + jurisdiction + case_cluster; CocoIndex
v1 ingests the corpus into a LanceDB table with vector index + FTS
ready for the temporal graph (WO-4), timeline visualiser (WO-6), and
casefile convention (WO-7).

## Background

The 113 PDFs at
`leabharlann/gemini_deep_research/{law,medical}/` are the canonical
source material for every ciandlithe case-study pilot. Today
`case_study_loader.py` only does `path.exists()` + `stat().st_size` —
nothing is parsed. 96 of the 113 PDFs are unreferenced anywhere.
WO-1 builds the corpus ingestion pipeline that turns them into
queryable rows.

## Requirements

### Requirement: The PDF text extractor

The system SHALL provide `cocoindex_flows/ciandlithe/corpus/_pdf_text.py`
that uses PyMuPDF for page-anchored text extraction (no OCR; the PDFs
are Google-Docs-rendered with a clean text layer).

### Requirement: The cohort classifier

The system SHALL provide `cocoindex_flows/ciandlithe/corpus/_classifier.py`
that maps each PDF to `(cohort, jurisdiction, case_cluster)` using
filename + first-2-pages heuristics. Unresolvable → `unclassified` review
queue, never silent drop.

### Requirement: The 2 CocoIndex corpus flows

The system SHALL provide `leabharlann_law_flow.py` + `leabharlann_medical_flow.py`
that walk the 59 + 54 PDFs respectively, chunk, embed (BGE-M3 1024-d),
and mount LanceDB tables with vector indexes.

### Requirement: The 3 BAML extraction declarations

The system SHALL provide 3 BAML declarations (the structured-extraction
layer that a later change will invoke): `research_doc_extraction.baml`,
`case_chronology_extraction.baml`, `legal_entity_extraction.baml`. These
are declared but not invoked in WO-1 (which uses Python regex/heuristics).

### Requirement: The case_study_loader extension

The system SHALL extend `dlt_sources/ciandlithe/cross/case_study_loader.py`
to extract text via PyMuPDF, preserving the existing public function
signatures.

### Requirement: The corpus smoke test

The system SHALL provide `tests/smoke/test_leabharlann_corpus.py` that
asserts every leabharlann PDF yields non-empty text.

## Cross-references

- [`../../cocoindex_flows/ciandlithe/corpus/`](../../cocoindex_flows/ciandlithe/corpus/) — the corpus flows
- [`../../baml_src/ciandlithe/corpus/`](../../baml_src/ciandlithe/corpus/) — the BAML extraction declarations
- [`../../dlt_sources/ciandlithe/cross/case_study_loader.py`](../../dlt_sources/ciandlithe/cross/case_study_loader.py) — the existing loader (extended)
- [`../../LICENSE.md`](../../LICENSE.md) — §5.1 (OSINT ceiling) + §5.2 (PoI clause)