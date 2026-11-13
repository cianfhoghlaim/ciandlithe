# ciandlithe-leabharlann-corpus — Agent Routing

| Spec | Path |
|:--|:--|
| spec.md | [./spec.md](./spec.md) |

## Quick orientation

`ciandlithe-leabharlann-corpus` ingests all 113 leabharlann PDFs
(59 law + 54 medical). PyMuPDF + regex/heuristic classifier + CocoIndex
v1 ingestion into a LanceDB table ready for RAG + the temporal
graph + the timeline visualiser.

## Routing table

| I want to... | Look at... |
|:--|:--|
| See the canonical spec | `./spec.md` |
| Inspect the PDF text extractor | `cocoindex_flows/ciandlithe/corpus/_pdf_text.py` |
| Inspect the cohort classifier | `cocoindex_flows/ciandlithe/corpus/_classifier.py` |
| Run the law ingestion | `mise run ciandlithe:corpus:law:ingest` |
| Run the medical ingestion | `mise run ciandlithe:corpus:medical:ingest` |
| View the case_study_loader extension | `dlt_sources/ciandlithe/cross/case_study_loader.py` |
| View the smoke test | `tests/smoke/test_leabharlann_corpus.py` |