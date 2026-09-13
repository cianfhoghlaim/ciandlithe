# CIANDLITHE — `cocoindex_flows/ciandlithe/corpus/_pdf_text.py`
#
# Per the openspec/changes/ciandlithe-leabharlann-corpus-ingest-v1/
# specs/ciandlithe-leabharlann-corpus/spec.md, Requirement: The PDF
# text extractor.
#
# Licence: BUSL-1.1 v2 CIANDLITHE edition (per LICENSE.md)
#
# Per LICENSE.md §3.8 + §5.2:
#   - osint_ceiling_enforced = True (always)
#   - analyst_review_required = True (always)
#   - PoI clause: non-public individuals are never named
"""CIANDLITHE PDF text extractor.

Uses PyMuPDF (`fitz`) to extract page-anchored text spans from every
PDF in the leabharlann corpus. The PDFs are Google-Docs-rendered
with a clean text layer — no OCR needed.

Returns `(page, char_start, char_end, text)` spans suitable for
chunking + embedding.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

logger = logging.getLogger(__name__)

# PyMuPDF is optional — degrade gracefully if not installed
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    fitz = None  # type: ignore[assignment]
    PYMUPDF_AVAILABLE = False


@dataclass(frozen=True)
class PdfSpan:
    """One page-anchored text span extracted from a PDF."""

    page: int           # 0-indexed page number
    char_start: int     # char offset within the page
    char_end: int       # char offset within the page
    text: str           # the span text


@dataclass(frozen=True)
class PdfDocument:
    """All spans for one PDF."""

    path: Path
    page_count: int
    spans: tuple[PdfSpan, ...]
    char_count: int


class PdfTextExtractor:
    """PyMuPDF-backed text extractor for leabharlann PDFs.

    Usage:
        extractor = PdfTextExtractor()
        doc = extractor.extract(Path("leabharlann/.../foo.pdf"))
        for span in doc.spans:
            print(span.page, span.text[:80])
    """

    def extract(self, pdf_path: Path) -> PdfDocument:
        """Extract all page-anchored text spans from the given PDF.

        Args:
            pdf_path: absolute path to the PDF file.

        Returns:
            A PdfDocument with all spans. If PyMuPDF is not installed,
            the returned PdfDocument has 0 spans (graceful degradation).

        Raises:
            FileNotFoundError: if pdf_path doesn't exist.
        """
        if not PYMUPDF_AVAILABLE:
            logger.warning(
                "pymupdf_not_available_returning_empty",
                extra={"pdf_path": str(pdf_path)},
            )
            return PdfDocument(path=pdf_path, page_count=0, spans=(), char_count=0)

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        spans: list[PdfSpan] = []
        page_count = 0
        try:
            with fitz.open(pdf_path) as doc:
                page_count = len(doc)
                for page_idx, page in enumerate(doc):
                    text = page.get_text("text")
                    if not text.strip():
                        continue
                    # Whole-page span (PyMuPDF returns the full page text
                    # as a single string; we record it as one span per page
                    # rather than splitting — chunking happens downstream).
                    spans.append(PdfSpan(
                        page=page_idx,
                        char_start=0,
                        char_end=len(text),
                        text=text,
                    ))
        except Exception as exc:
            logger.warning(
                "pdf_extraction_failed",
                extra={"pdf_path": str(pdf_path), "error": str(exc)},
            )
            # Continue with whatever spans we collected (partial recovery)
            return PdfDocument(
                path=pdf_path,
                page_count=page_count,
                spans=tuple(spans),
                char_count=sum(len(s.text) for s in spans),
            )

        char_count = sum(len(s.text) for s in spans)
        return PdfDocument(
            path=pdf_path,
            page_count=page_count,
            spans=tuple(spans),
            char_count=char_count,
        )

    def iter_page_text(self, pdf_path: Path) -> Iterator[tuple[int, str]]:
        """Yield (page, page_text) for each non-empty page.

        Convenience iterator for downstream chunkers.
        """
        doc = self.extract(pdf_path)
        for span in doc.spans:
            yield span.page, span.text


def extract_first_n_chars(pdf_path: Path, n: int = 4000) -> str:
    """Extract the first `n` characters of a PDF (used by the cohort classifier).

    Cheap: only reads the first ~5 pages.
    """
    if not PYMUPDF_AVAILABLE:
        return ""
    if not pdf_path.exists():
        return ""
    try:
        with fitz.open(pdf_path) as doc:
            collected: list[str] = []
            total = 0
            for page in doc:
                text = page.get_text("text")
                if not text.strip():
                    continue
                if total + len(text) > n:
                    collected.append(text[: n - total])
                    break
                collected.append(text)
                total += len(text)
                if total >= n:
                    break
            return "\n".join(collected)[:n]
    except Exception as exc:
        logger.warning(
            "extract_first_n_chars_failed",
            extra={"pdf_path": str(pdf_path), "error": str(exc)},
        )
        return ""


__all__ = [
    "PYMUPDF_AVAILABLE",
    "PdfDocument",
    "PdfSpan",
    "PdfTextExtractor",
    "extract_first_n_chars",
]