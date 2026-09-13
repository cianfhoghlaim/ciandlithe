## ADDED Requirements

### Requirement: The PDF text extractor

The system SHALL provide a `PdfTextExtractor` class at `cocoindex_flows/ciandlithe/corpus/_pdf_text.py` that extracts page-anchored text spans from every PDF in the leabharlann corpus.

#### Scenario: PyMuPDF returns non-empty text for every PDF

- **WHEN** the operator invokes `PdfTextExtractor().extract(pdf_path)`
- **THEN** the method SHALL return a list of `(page, char_start, char_end, text)` spans
- **AND** SHALL return a non-empty list for ≥95% of the 113 leabharlann PDFs
- **AND** SHALL NOT use OCR (the PDFs are Google-Docs-rendered with a clean text layer)

### Requirement: The PDF → cohort classifier

The system SHALL provide a `CohortClassifier` at `cocoindex_flows/ciandlithe/corpus/_classifier.py` that maps each PDF to `(cohort, jurisdiction, case_cluster)`.

#### Scenario: The classifier assigns a cohort + jurisdiction

- **WHEN** the operator invokes `CohortClassifier().classify(pdf_path)`
- **THEN** the method SHALL return a `Classification(cohort, jurisdiction, case_cluster)` record
- **AND** SHALL assign `cohort="unclassified"` if no signal is found (→ review queue, never silent drop)
- **AND** SHALL assert at least 95 of the 113 PDFs are assigned to a non-`unclassified` cohort

### Requirement: The 2 CocoIndex corpus flows

The system SHALL provide 2 CocoIndex v1 apps at `cocoindex_flows/ciandlithe/corpus/{leabharlann_law_flow,leabharlann_medical_flow}.py` that ingest the 59 law + 54 medical PDFs respectively.

#### Scenario: The law flow mounts a LanceDB table

- **WHEN** the operator runs `mise run ciandlithe:corpus:law:ingest --dry-run`
- **THEN** the flow SHALL walk `leabharlann/gemini_deep_research/law/`
- **AND** SHALL extract text per PDF via PyMuPDF
- **AND** SHALL chunk via `RecursiveSplitter` (1k tokens / 200 overlap)
- **AND** SHALL embed via `BAAI/bge-m3` 1024-d
- **AND** SHALL mount a LanceDB table `ciandlithe.leabharlann_law_chunks` with vector index

#### Scenario: The medical flow mirrors the law flow

- **WHEN** the operator runs `mise run ciandlithe:corpus:medical:ingest --dry-run`
- **THEN** the medical flow does the same for the 54 medical PDFs

### Requirement: The 3 BAML extraction declarations

The system SHALL provide 3 BAML function declarations at `baml_src/ciandlithe/corpus/` for the structured-extraction layer that a later change will wire.

#### Scenario: The BAML declarations exist and use the older syntax

- **WHEN** the operator inspects `baml_src/ciandlithe/corpus/`
- **THEN** the directory SHALL contain `research_doc_extraction.baml`, `case_chronology_extraction.baml`, `legal_entity_extraction.baml`
- **AND** every `function ... { ... }` block SHALL use the BAML 0.222.0-compatible syntax (`client "Primary"` on its own line, no nested `client` inside the function body)

### Requirement: The case_study_loader extension

The system SHALL extend `dlt_sources/ciandlithe/cross/case_study_loader.py` to extract text via PyMuPDF and cache in a `leabharlann_cache` LanceDB table.

#### Scenario: load_case_study returns extracted text

- **WHEN** the operator invokes `load_case_study("pilot-sodium-valproate")`
- **THEN** the returned dict SHALL include `extracted_text_chars` (non-zero)
- **AND** the existing public function signature SHALL be unchanged (the 7 existing smoke tests keep passing)

### Requirement: The corpus smoke test

The system SHALL provide `tests/smoke/test_leabharlann_corpus.py` that asserts every leabharlann PDF is on disk + yields non-empty text.

#### Scenario: The smoke test passes

- **WHEN** the operator runs `pytest tests/smoke/test_leabharlann_corpus.py -v`
- **THEN** the test SHALL iterate every leabharlann law + medical PDF
- **AND** SHALL assert each file yields non-empty extracted text
- **AND** SHALL assert no more than 5 PDFs land in the `unclassified` review queue

## Cross-references

- [`../../../baml_src/ciandlithe/corpus/`](../../../baml_src/ciandlithe/corpus/) — the BAML extraction declarations
- [`../../../cocoindex_flows/ciandlithe/corpus/`](../../../cocoindex_flows/ciandlithe/corpus/) — the corpus flows
- [`../../../dlt_sources/ciandlithe/cross/case_study_loader.py`](../../../dlt_sources/ciandlithe/cross/case_study_loader.py) — the existing loader (extended)
- [`../../../../leabharlann/gemini_deep_research/`](../../../../leabharlann/gemini_deep_research/) — read-only source material
- [`../../../LICENSE.md`](../../../LICENSE.md) — §5.1 (OSINT ceiling) + §5.2 (PoI clause)