# CIANDLITHE — `cocoindex_flows/ciandlithe/corpus/leabharlann_law_flow.py`
#
# Per the openspec/changes/ciandlithe-leabharlann-corpus-ingest-v1/
# specs/ciandlithe-leabharlann-corpus/spec.md, Requirement: The 2
# CocoIndex corpus flows.
#
# Licence: BUSL-1.1 v2 CIANDLITHE edition (per LICENSE.md)
#
# Per LICENSE.md §3.8 + §5.2:
#   - osint_ceiling_enforced = True (always)
#   - analyst_review_required = True (always)
#   - PoI clause: non-public individuals are never named
"""ciandlithe leabharlann_law_flow — the 59 law PDFs ingestion.

Walks `leabharlann/gemini_deep_research/law/`, extracts text per PDF
via PyMuPDF, classifies each via the regex/heuristic classifier (the
fast path — BAML is declared but not invoked in WO-1), chunks via a
plain-text chunker, and stores the result.

This module is the CocoIndex-v1-decorated orchestrator pattern (R1–R4
contract per openspec/changes/ciandlithe-repo-foundation-v1/
specs/ciandlithe-pipeline/spec.md). When the cocoindex SDK is installed
the `@coco.flow(scope="function_flow")` decorator + `app_main` callback
are used to declare the pipeline declaratively; when it's not, the
underlying plain-Python orchestrator runs and is verifiable by pytest
without any cocoindex dependency.

Source: `/Users/cianmacandeisigh/dev/cianfhoghlaim/leabharlann/gemini_deep_research/law/`
(59 PDFs, ~22 MB, read-only). Override via `LEABHARLANN_ROOT` env var.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ._classifier import CohortClassifier
from ._pdf_text import PdfTextExtractor

logger = logging.getLogger(__name__)


# CocoIndex is optional — degrade gracefully.
try:
    from ...._shared import EMBEDDER, LANCE_DB, shared_lifespan  # noqa: F401
    COCOINDEX_AVAILABLE = True
    import cocoindex as _coco  # type: ignore[import-not-found]  # noqa: F401
except ImportError:
    COCOINDEX_AVAILABLE = False
    _coco = None  # type: ignore[assignment]


DEFAULT_LEABHARLANN_ROOT = os.environ.get(
    "LEABHARLANN_ROOT",
    str(Path.home() / "dev" / "cianfhoghlaim" / "leabharlann"),
)
LAW_ROOT = Path(DEFAULT_LEABHARLANN_ROOT) / "gemini_deep_research" / "law"


@dataclass
class ChunkRecord:
    """One chunk of one PDF after PyMuPDF extraction + classification."""

    doc_id: str
    path: str
    filename: str
    page: int
    chunk_index: int
    text: str
    cohort: str
    jurisdiction: str
    case_cluster: str
    source_pdf_urls: list[str]
    extraction_confidence: float
    osint_ceiling_enforced: bool = True
    analyst_review_required: bool = True
    char_count: int = 0


@dataclass
class FlowResult:
    """The output of running the law flow."""

    flow_name: str
    total_pdfs: int = 0
    successful_pdfs: int = 0
    failed_pdfs: int = 0
    classified_as_unclassified: int = 0
    total_chunks: int = 0
    total_chars: int = 0
    chunks: list[ChunkRecord] = field(default_factory=list)


def list_law_pdfs(root: Path | None = None) -> list[Path]:
    """Return the sorted list of law PDFs on disk."""
    root = root or LAW_ROOT
    if not root.exists():
        return []
    return sorted(p for p in root.glob("*.pdf") if p.is_file())


def _chunk_text(text: str, target_chars: int = 1000, overlap_chars: int = 200) -> list[str]:
    """Plain-text chunker (RecursiveSplitter-ish but without the dependency).

    Splits on paragraph boundaries (double newline) first; falls back
    to sentence boundaries; falls back to fixed windows with overlap.
    """
    if not text:
        return []
    # First pass: paragraph split
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) + 2 <= target_chars:
            current = f"{current}\n\n{para}".strip() if current else para
        else:
            if current:
                chunks.append(current)
            if len(para) > target_chars:
                # Sentence-split the long paragraph
                sentences = [s.strip() for s in para.split(". ") if s.strip()]
                s_buf = ""
                for s in sentences:
                    if len(s_buf) + len(s) + 2 <= target_chars:
                        s_buf = f"{s_buf}. {s}".strip() if s_buf else s
                    else:
                        if s_buf:
                            chunks.append(s_buf)
                        s_buf = s
                if s_buf:
                    current = s_buf
                else:
                    current = ""
            else:
                current = para
    if current:
        chunks.append(current)
    # Add overlap between consecutive chunks
    if overlap_chars > 0 and len(chunks) > 1:
        overlapped: list[str] = [chunks[0]]
        for i in range(1, len(chunks)):
            tail = overlapped[-1][-overlap_chars:]
            overlapped.append(f"{tail}\n\n{chunks[i]}")
        chunks = overlapped
    return chunks


def _process_one_pdf(
    pdf_path: Path,
    extractor: PdfTextExtractor,
    classifier: CohortClassifier,
) -> list[ChunkRecord]:
    """Extract text + classify + chunk one PDF. Returns 0+ ChunkRecords."""
    try:
        doc = extractor.extract(pdf_path)
    except Exception as exc:
        logger.warning(
            "pdf_extract_failed",
            extra={"pdf_path": str(pdf_path), "error": str(exc)},
        )
        return []
    if doc.char_count == 0:
        return []
    classification = classifier.classify(pdf_path)
    chunks_text = _chunk_text(doc.spans[0].text if doc.spans else "")
    if not chunks_text:
        # PDF has text but chunking produced nothing — fall back to per-page
        chunks_text = []
        for span in doc.spans:
            page_chunks = _chunk_text(span.text)
            chunks_text.extend(page_chunks)
    records: list[ChunkRecord] = []
    for i, chunk in enumerate(chunks_text):
        records.append(ChunkRecord(
            doc_id=f"{pdf_path}#{i}",
            path=str(pdf_path),
            filename=pdf_path.name,
            page=doc.spans[0].page if doc.spans else 0,
            chunk_index=i,
            text=chunk,
            cohort=classification.cohort,
            jurisdiction=classification.jurisdiction,
            case_cluster=classification.case_cluster,
            source_pdf_urls=[str(pdf_path)],
            extraction_confidence=classification.confidence,
            char_count=len(chunk),
        ))
    return records


def run_law_flow(
    root: Path | None = None,
    *,
    write_to: Path | None = None,
) -> FlowResult:
    """Execute the law corpus ingestion pipeline.

    Args:
        root: override the LAW_ROOT (defaults to the canonical path).
        write_to: optional path to write the result as JSON-Lines
            (for downstream consumption by the temporal graph + the
            timeline visualiser).

    Returns:
        A FlowResult summarising the run.
    """
    root = root or LAW_ROOT
    result = FlowResult(flow_name="leabharlann_law_flow")

    pdfs = list_law_pdfs(root)
    result.total_pdfs = len(pdfs)
    if not pdfs:
        logger.warning("no_law_pdfs_found", extra={"root": str(root)})
        return result

    extractor = PdfTextExtractor()
    classifier = CohortClassifier()

    for pdf in pdfs:
        records = _process_one_pdf(pdf, extractor, classifier)
        if not records:
            result.failed_pdfs += 1
            continue
        result.successful_pdfs += 1
        result.chunks.extend(records)
        result.total_chunks += len(records)
        result.total_chars += sum(r.char_count for r in records)
        if records and records[0].cohort == "unclassified":
            result.classified_as_unclassified += 1

    if write_to is not None:
        write_to.parent.mkdir(parents=True, exist_ok=True)
        import json
        with write_to.open("w", encoding="utf-8") as f:
            for r in result.chunks:
                f.write(json.dumps({
                    "doc_id": r.doc_id,
                    "path": r.path,
                    "filename": r.filename,
                    "page": r.page,
                    "chunk_index": r.chunk_index,
                    "text": r.text,
                    "cohort": r.cohort,
                    "jurisdiction": r.jurisdiction,
                    "case_cluster": r.case_cluster,
                    "source_pdf_urls": r.source_pdf_urls,
                    "extraction_confidence": r.extraction_confidence,
                    "osint_ceiling_enforced": r.osint_ceiling_enforced,
                    "analyst_review_required": r.analyst_review_required,
                    "char_count": r.char_count,
                }, ensure_ascii=False) + "\n")
        logger.info("law_flow_wrote", extra={"path": str(write_to), "rows": len(result.chunks)})

    logger.info(
        "law_flow_done",
        extra={
            "total_pdfs": result.total_pdfs,
            "successful_pdfs": result.successful_pdfs,
            "total_chunks": result.total_chunks,
            "unclassified": result.classified_as_unclassified,
        },
    )
    return result


# ---------------------------------------------------------------------------
# CocoIndex v1 decorator layer (R2 — module-scope app) — only present
# when the cocoindex SDK is installed. When absent, `run_law_flow()` is
# still the canonical orchestrator entry point.
# ---------------------------------------------------------------------------
if COCOINDEX_AVAILABLE:

    @_coco.flow(scope="function_flow")  # type: ignore[misc]
    async def leabharlann_law_flow(
        root: Path,
        table: Any,
        classifier_out: Any,
    ) -> None:
        """The CocoIndex-decorated orchestrator (calls run_law_flow
        internally)."""
        # Real impl would emit to `table` + `classifier_out`. For WO-1
        # we defer to run_law_flow and just log.
        result = run_law_flow(root)
        classifier_out["flow_name"] = result.flow_name
        classifier_out["total_pdfs"] = result.total_pdfs
        classifier_out["successful_pdfs"] = result.successful_pdfs
        classifier_out["total_chunks"] = result.total_chunks

    @_coco.AppConfig  # type: ignore[misc]
    class _Config:
        name = "LeabharlannLawFlow"

    app = _coco.App(_Config)  # type: ignore[call-arg]
else:
    app = None


# Exports
__all__ = [
    "app",
    "list_law_pdfs",
    "run_law_flow",
    "ChunkRecord",
    "FlowResult",
    "LAW_ROOT",
]