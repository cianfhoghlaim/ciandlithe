# CIANDLITHE — `cocoindex_flows/ciandlithe/corpus/__init__.py`
#
# Per the openspec/changes/ciandlithe-leabharlann-corpus-ingest-v1/
# specs/ciandlithe-leabharlann-corpus/spec.md.
#
# Licence: BUSL-1.1 v2 CIANDLITHE edition (per LICENSE.md)
#
# Per LICENSE.md §3.8 + §5.2:
#   - osint_ceiling_enforced = True (always)
#   - analyst_review_required = True (always)
#   - PoI clause: non-public individuals are never named
"""CIANDLITHE corpus ingestion — exports for the corpus module.

The canonical 2 CocoIndex v1 flows ingest the leabharlann law +
medical Gemini Deep Research PDFs into LanceDB tables ready for
RAG + the temporal graph (WO-4) + the timeline visualiser (WO-6).

Reads via PyMuPDF + a regex/heuristic classifier. CocoIndex v1
embedding via the canonical BAAI/bge-m3 1024-d embedder (the
shared embedder from `cocoindex_flows/_shared/_lifespan.py`).
"""

from ._classifier import (
    CaseCluster,
    Classification,
    Cohort,
    CohortClassifier,
    Jurisdiction,
    classify_by_filename,
    classify_by_text,
)
from ._pdf_text import (
    PYMUPDF_AVAILABLE,
    PdfDocument,
    PdfSpan,
    PdfTextExtractor,
    extract_first_n_chars,
)

__all__ = [
    "CaseCluster",
    "Classification",
    "Cohort",
    "CohortClassifier",
    "Jurisdiction",
    "PYMUPDF_AVAILABLE",
    "PdfDocument",
    "PdfSpan",
    "PdfTextExtractor",
    "classify_by_filename",
    "classify_by_text",
    "extract_first_n_chars",
]