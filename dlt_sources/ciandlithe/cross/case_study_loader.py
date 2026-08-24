"""CIANDLITHE case-study loader.

Loads the 7 leabharlann gemini_deep_research PDFs (one per composite-pilot
party) as read-only context for the composite pilot FunctionTool + the
per-cohort BAML extraction functions.

The PDFs are NOT ingested via DLT (they are NOT public-sector sources;
they are Gemini Deep Research outputs based on public-sector sources).
They are referenced by file path in the FunctionTool output, not by URL.

Per LICENSE.md §5.2 (PoI clause) + §3.8 (no-auto-submit constraint):
every PDF that names a non-public individual is flagged for analyst
review and is NOT auto-rendered in any shared view.
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import Any

try:
    import structlog
    logger = structlog.get_logger(__name__)
except ImportError:
    structlog = None
    logger = logging.getLogger(__name__)


# The canonical leabharlann root (the user's private leabharlann repo)
DEFAULT_LEABHARLANN_ROOT = os.environ.get(
    "CIANDLITHE_LEABHARLANN_ROOT",
    str(Path.home() / "dev" / "cianfhoghlaim" / "leabharlann"),
)


# The 7 composite-pilot parties + their canonical leabharlann PDF paths
PILOT_PARTY_PDFS: list[dict[str, str]] = [
    {
        "party_id": "pilot-qub-rvh",
        "cohort": "MedicalMalpractice",
        "sub_nation": "NI",
        "primary_pdf": "gemini_deep_research/law/qub_royal_victoria_malpractice.pdf",
        "companion_pdfs": [
            "gemini_deep_research/medical/misdiagnosis_brain_damage_recovery.pdf",
            "gemini_deep_research/law/maximizing_civil_suit_damages_against_qub.pdf",
        ],
    },
    {
        "party_id": "pilot-eric",
        "cohort": "EmployerBreach",
        "sub_nation": "CROSS_BORDER",
        "primary_pdf": "gemini_deep_research/law/suing_ceo_for_breach_abuse_damages.pdf",
        "companion_pdfs": [
            "gemini_deep_research/law/cross_border_legal_action_research.pdf",
            "gemini_deep_research/law/monroes.pdf",
        ],
    },
    {
        "party_id": "pilot-garda",
        "cohort": "GardaDiscrimination",
        "sub_nation": "IRELAND",
        "primary_pdf": "gemini_deep_research/law/garda_corruption_and_data_access.pdf",
        "companion_pdfs": [
            "gemini_deep_research/law/garda_data_and_accommodation_request.pdf",
            "gemini_deep_research/law/garda_brutality_dual_citizenship_and_justice.pdf",
        ],
    },
    {
        "party_id": "pilot-dkit",
        "cohort": "EducationDiscrimination",
        "sub_nation": "IRELAND",
        "primary_pdf": "gemini_deep_research/law/discrimination_case_strategy_university_of_galway.pdf",
        "companion_pdfs": [
            "gemini_deep_research/law/cbd_discrimination_lawsuit_preparation.pdf",
            "gemini_deep_research/law/challenging_university_rejection_and_ombudsman_decision.pdf",
        ],
    },
    {
        "party_id": "pilot-nuig",
        "cohort": "EducationDiscrimination",
        "sub_nation": "IRELAND",
        "primary_pdf": "gemini_deep_research/law/discrimination_case_strategy_university_of_galway.pdf",
        "companion_pdfs": [
            "gemini_deep_research/law/cbd_dispensary_manager_discrimination_lawsuit.pdf",
        ],
    },
    {
        "party_id": "pilot-ucl",
        "cohort": "AdmissionBreach",
        "sub_nation": "ENGLAND",
        "primary_pdf": "gemini_deep_research/law/ucl_sar_equality_act_claim.pdf",
        "companion_pdfs": [],
    },
    {
        "party_id": "pilot-sodium-valproate",
        "cohort": "MedicalMalpractice",
        "sub_nation": "IRELAND",
        "primary_pdf": "gemini_deep_research/medical/irish_sodium_valproate_inquiry_and_healthcare.pdf",
        "companion_pdfs": [
            "gemini_deep_research/medical/sodium_valproate_lawsuits_and_inquiries.pdf",
            "gemini_deep_research/medical/essential_tbi_medication.pdf",
        ],
    },
]


def load_case_study(party_id: str, leabharlann_root: str | None = None) -> dict[str, Any]:
    """Load one composite-pilot party's case study.

    Returns a dict with:
      - party_id: the pilot party id
      - cohort: the BLIP v1 cohort
      - sub_nation: the British-Isles sub-nation
      - primary_pdf_path: the absolute path to the primary leabharlann PDF
      - primary_pdf_exists: bool
      - primary_pdf_size_bytes: int (if exists)
      - companion_pdfs: list of {path, exists, size_bytes}
      - osint_ceiling_enforced: True (always)
      - analyst_review_required: True (always)
      - source_pdf_urls: list of read-only-context URLs (leabharlann paths, NOT OSINT-allowlisted)

    Per LICENSE.md §5.2 + §3.8: this function NEVER names a non-public
    individual in its output; the raw PDF may name them, but the loader
    returns only the metadata + the file path.
    """
    root = Path(leabharlann_root or DEFAULT_LEABHARLANN_ROOT)
    pilot_party = next((p for p in PILOT_PARTY_PDFS if p["party_id"] == party_id), None)
    if pilot_party is None:
        return {
            "party_id": party_id,
            "osint_ceiling_enforced": True,
            "analyst_review_required": True,
            "error": f"unknown party_id {party_id!r}; valid ids: {[p['party_id'] for p in PILOT_PARTY_PDFS]}",
        }

    primary_pdf_path = root / pilot_party["primary_pdf"]
    companion = []
    for c in pilot_party["companion_pdfs"]:
        cp = root / c
        companion.append({
            "relative_path": c,
            "absolute_path": str(cp),
            "exists": cp.exists(),
            "size_bytes": cp.stat().st_size if cp.exists() else 0,
        })

    return {
        "party_id": party_id,
        "cohort": pilot_party["cohort"],
        "sub_nation": pilot_party["sub_nation"],
        "primary_pdf_path": str(primary_pdf_path),
        "primary_pdf_relative": pilot_party["primary_pdf"],
        "primary_pdf_exists": primary_pdf_path.exists(),
        "primary_pdf_size_bytes": primary_pdf_path.stat().st_size if primary_pdf_path.exists() else 0,
        "companion_pdfs": companion,
        "osint_ceiling_enforced": True,
        "analyst_review_required": True,
        "source_pdf_urls": [
            f"file://{root}/{pilot_party['primary_pdf']}",
            *[f"file://{root}/{c}" for c in pilot_party["companion_pdfs"]],
        ],
    }


def load_all_case_studies(leabharlann_root: str | None = None) -> list[dict[str, Any]]:
    """Load all 7 composite-pilot case studies."""
    return [load_case_study(p["party_id"], leabharlann_root) for p in PILOT_PARTY_PDFS]


if __name__ == "__main__":
    import json
    print(json.dumps(load_all_case_studies(), indent=2))