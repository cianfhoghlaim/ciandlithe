# Tasks: ciandlithe-leabharlann-corpus-ingest-v1

## 0. Pre-flight

- [x] Verify WO-0 (ciandlithe-toolchain-repair-v1) has shipped (the lint scripts + mise tasks work)
- [x] Verify `pymupdf>=1.24` is in pyproject.toml deps (added in WO-0)
- [x] Verify all 113 leabharlann PDFs are present on disk (`ls leabharlann/gemini_deep_research/law | wc -l` → 59; `… medical | wc -l` → 54)
- [x] Verify BAML 0.222.0 is installed (`baml-cli --version`) — use simpler syntax in new BAML files

## 1. Write the openspec change artifacts

- [x] `openspec/changes/ciandlithe-leabharlann-corpus-ingest-v1/proposal.md` (DONE)
- [x] `openspec/changes/ciandlithe-leabharlann-corpus-ingest-v1/tasks.md` (this file)
- [x] `openspec/changes/ciandlithe-leabharlann-corpus-ingest-v1/cross-repo-sync.md`
- [x] `openspec/changes/ciandlithe-leabharlann-corpus-ingest-v1/specs/ciandlithe-leabharlann-corpus/spec.md`
- [x] `openspec/specs/ciandlithe-leabharlann-corpus/spec.md` (canonical end-state)
- [x] `openspec/specs/ciandlithe-leabharlann-corpus/AGENTS.md` (≤30 lines)

## 2. Create the 4 corpus flow files

- [x] `cocoindex_flows/ciandlithe/corpus/__init__.py`
- [x] `cocoindex_flows/ciandlithe/corpus/_pdf_text.py` — PyMuPDF extraction
- [x] `cocoindex_flows/ciandlithe/corpus/_classifier.py` — PDF → (cohort, jurisdiction, case_cluster)
- [x] `cocoindex_flows/ciandlithe/corpus/leabharlann_law_flow.py` — 59 law PDFs
- [x] `cocoindex_flows/ciandlithe/corpus/leabharlann_medical_flow.py` — 54 medical PDFs

## 3. Create the 3 BAML files (declarations only; not invoked in WO-1)

- [x] `baml_src/ciandlithe/corpus/research_doc_extraction.baml`
- [x] `baml_src/ciandlithe/corpus/case_chronology_extraction.baml`
- [x] `baml_src/ciandlithe/corpus/legal_entity_extraction.baml`

## 4. Modify the existing case_study_loader.py

- [x] Extend `load_case_study(party_id)` to extract text via PyMuPDF
- [x] Cache extracted text in a `leabharlann_cache` LanceDB table (per-cohort)
- [x] Preserve existing public function signatures (so `tests/smoke/test_ciandlithe.py` keeps passing)

## 5. Add the smoke test

- [x] `tests/smoke/test_leabharlann_corpus.py` — asserts 113 PDFs present + non-empty + classified

## 6. Run the verification gates (paste real output)

- [x] `openspec validate ciandlithe-leabharlann-corpus-ingest-v1 --strict`
- [x] `openspec validate ciandlithe-leabharlann-corpus --strict`
- [x] `openspec validate --all --strict`
- [x] `mise run lint`
- [x] `uv run --isolated --python 3.12 --with pymupdf --with pytest python -m pytest tests/ -v`

## 7. Commit

- [x] `git add -A` (only the WO-1 files, not stray untracked files)
- [x] `git commit -m "feat(corpus): ingest all 113 leabharlann law+medical PDFs — PyMuPDF + heuristic classifier + BGE-M3-ready chunks"`

## 8. Follow-up openspec changes (NOT in this change's scope)

- [ ] `ciandlithe-lakehouse-medallion-v1` (WO-2) — DuckLake + MotherDuck + Lance Namespace
- [ ] `ciandlithe-blip-v1-cohort-expansion-v1` (WO-3) — 7 → 13 cohorts + OSINT allowlist entries
- [ ] `ciandlithe-temporal-graph-v1` (WO-4) — FalkorDB 3-phase + Graphiti bi-temporal
- [ ] `ciandlithe-limitation-calculator-v1` (WO-5) — statutory rule table
- [ ] `ciandlithe-timeline-visualiser-v1` (WO-6) — React + marimo
- [ ] `ciandlithe-casefile-convention-v1` (WO-7) — JSON schema + scaffolder
- [ ] `ciandlithe-case-study-expansion-v1` (WO-8) — 7 → 20 clusters
- [ ] `ciandlithe-orchestration-v1` (WO-9) — Dagster defs
- [ ] `ciandlithe-per-persona-web-surfaces-v1` (WO-10) — 7 apps
- [ ] `ciandlithe-agent-fleet-v1` (WO-11) — agent fleet
- [ ] `ciandlithe-initiation-runbook-v1` (WO-12) — runbook + fork template