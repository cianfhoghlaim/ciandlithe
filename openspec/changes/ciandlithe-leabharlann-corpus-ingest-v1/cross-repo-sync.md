# Cross-Repo Sync: ciandlithe-leabharlann-corpus-ingest-v1

This change touches ONLY the `ciandlithe/ciandlithe` repo. `leabharlann`
is read-only source material (113 PDFs). `cianchosaint` and
`cianchoghlaim` are not touched.

## Repo 1: ciandlithe (sole)

**Branch**: `main`
**Push target**: `github.com/cianfhoghlaim/ciandlithe`

**Files added:**
- `cocoindex_flows/ciandlithe/corpus/{__init__, _pdf_text, _classifier,
  leabharlann_law_flow, leabharlann_medical_flow}.py`
- `baml_src/ciandlithe/corpus/{research_doc_extraction, case_chronology_extraction,
  legal_entity_extraction}.baml`
- `tests/smoke/test_leabharlann_corpus.py`
- `openspec/changes/ciandlithe-leabharlann-corpus-ingest-v1/{proposal,
  tasks, cross-repo-sync}.md`
- `openspec/changes/ciandlithe-leabharlann-corpus-ingest-v1/specs/ciandlithe-leabharlann-corpus/spec.md`
- `openspec/specs/ciandlithe-leabharlann-corpus/{spec.md, AGENTS.md}`

**Files modified:**
- `dlt_sources/ciandlithe/cross/case_study_loader.py` — extended with
  text extraction

**Commit message:**
`feat(corpus): ingest all 113 leabharlann law+medical PDFs — PyMuPDF + heuristic classifier + BGE-M3-ready chunks`