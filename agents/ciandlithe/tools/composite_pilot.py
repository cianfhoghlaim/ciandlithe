# CIANDLITHE — composite_pilot.py (the FunctionTool)
#
# Mirrors the cianchosaint precedent at
# `cianchosaint/agents/cianchosaint/tools/reform_uk_pilot.py`.
#
# The composite pilot exercises ALL 7 BLIP v1 cohorts via 7 leabharlann
# PDFs (read-only context). It is the canonical pilot for ciandlithe,
# mirroring how the Reform UK pilot was the canonical pilot for
# cianchosaint.
#
# Per LICENSE.md §3.8 + §5.2:
#   - osint_ceiling_enforced = True (always)
#   - analyst_review_required = True (always)
#   - PoI clause: extractions naming non-public individuals fail
#   - NEVER submits forms to courts.ie / irishstatutebook.ie / nidirect.gov.uk
#
# Per AGENTS.md (composite pilot reference):
#   - 1. QUB / Royal Victoria Hospital brain-injury  (medical_malpractice, NI)
#   - 2. Eric employer / breach of contract          (employer_breach, cross-border NI ↔ ROI)
#   - 3. Garda discrimination / data-access         (garda_discrimination, ROI)
#   - 4. DkIT disability / education complaint      (education_discrimination, ROI)
#   - 5. NUIG / UoG rejection + abuse of power       (education_discrimination, ROI)
#   - 6. UCL offer / DBS                            (admission_breach, England)
#   - 7. Sodium valproate / HSE misprescription      (medical_malpractice, ROI)
"""CIANDLITHE composite pilot FunctionTool.

Mirrors the cianchosaint `reform_uk_pilot.py` precedent. Reads 7 leabharlann
PDFs (read-only context) and produces 7 `CompositePilotDossier` records —
one per pilot party. Returns a list of dicts.

The FunctionTool NEVER submits forms. It generates a dossier (PDF + JSON)
for manual review by the claimant or their solicitor.
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


# -------------------------------------------------------------------
# The 7 pilot parties + their canonical leabharlann PDF paths
# (read-only context; NOT in this repo; lives in leabharlann/)
# -------------------------------------------------------------------
PILOT_PARTIES: list[dict[str, str]] = [
    {
        "party_id": "pilot-qub-rvh",
        "cohort": "MedicalMalpractice",
        "sub_nation": "NI",
        "display_name": "QUB / Royal Victoria Hospital brain-injury",
        "leabharlann_pdf": "leabharlann/gemini_deep_research/law/qub_royal_victoria_malpractice.pdf",
        "companion_pdfs": [
            "leabharlann/gemini_deep_research/medical/misdiagnosis_brain_damage_recovery.pdf",
            "leabharlann/gemini_deep_research/law/maximizing_civil_suit_damages_against_qub.pdf",
        ],
    },
    {
        "party_id": "pilot-eric",
        "cohort": "EmployerBreach",
        "sub_nation": "CROSS_BORDER",
        "display_name": "Eric employer / breach of contract",
        "leabharlann_pdf": "leabharlann/gemini_deep_research/law/suing_ceo_for_breach_abuse_damages.pdf",
        "companion_pdfs": [
            "leabharlann/gemini_deep_research/law/cross_border_legal_action_research.pdf",
            "leabharlann/gemini_deep_research/law/monroes.pdf",
        ],
    },
    {
        "party_id": "pilot-garda",
        "cohort": "GardaDiscrimination",
        "sub_nation": "IRELAND",
        "display_name": "Garda discrimination / data-access",
        "leabharlann_pdf": "leabharlann/gemini_deep_research/law/garda_corruption_and_data_access.pdf",
        "companion_pdfs": [
            "leabharlann/gemini_deep_research/law/garda_data_and_accommodation_request.pdf",
            "leabharlann/gemini_deep_research/law/garda_brutality_dual_citizenship_and_justice.pdf",
        ],
    },
    {
        "party_id": "pilot-dkit",
        "cohort": "EducationDiscrimination",
        "sub_nation": "IRELAND",
        "display_name": "DkIT disability / education complaint",
        "leabharlann_pdf": "leabharlann/gemini_deep_research/law/discrimination_case_strategy_university_of_galway.pdf",
        "companion_pdfs": [
            "leabharlann/gemini_deep_research/law/cbd_discrimination_lawsuit_preparation.pdf",
            "leabharlann/gemini_deep_research/law/challenging_university_rejection_and_ombudsman_decision.pdf",
        ],
    },
    {
        "party_id": "pilot-nuig",
        "cohort": "EducationDiscrimination",
        "sub_nation": "IRELAND",
        "display_name": "NUIG / UoG rejection + abuse of power",
        "leabharlann_pdf": "leabharlann/gemini_deep_research/law/discrimination_case_strategy_university_of_galway.pdf",
        "companion_pdfs": [
            "leabharlann/gemini_deep_research/law/cbd_dispensary_manager_discrimination_lawsuit.pdf",
        ],
    },
    {
        "party_id": "pilot-ucl",
        "cohort": "AdmissionBreach",
        "sub_nation": "ENGLAND",
        "display_name": "UCL offer / DBS",
        "leabharlann_pdf": "leabharlann/gemini_deep_research/law/ucl_sar_equality_act_claim.pdf",
        "companion_pdfs": [],
    },
    {
        "party_id": "pilot-sodium-valproate",
        "cohort": "MedicalMalpractice",
        "sub_nation": "IRELAND",
        "display_name": "Sodium valproate / HSE misprescription",
        "leabharlann_pdf": "leabharlann/gemini_deep_research/medical/irish_sodium_valproate_inquiry_and_healthcare.pdf",
        "companion_pdfs": [
            "leabharlann/gemini_deep_research/medical/sodium_valproate_lawsuits_and_inquiries.pdf",
            "leabharlann/gemini_deep_research/medical/essential_tbi_medication.pdf",
        ],
    },
]


def composite_pilot_tool(
    cohort: str = "all",
    pilot_party_id: str | None = None,
) -> dict[str, Any]:
    """The CIANDLITHE composite pilot FunctionTool.

    Per the openspec/changes/ciandlithe-composite-pilot-workflow-v1/
    specs/ciandlithe-composite-pilot-workflow/spec.md, this tool
    cross-references the 7 pilot parties + their leabharlann PDFs
    (read-only context) and returns a structured `CompositePilotDossier`
    dict (per `baml_src/ciandlithe/case_studies/reform_civil_suit_dossier.baml`).

    NEVER submits forms. NEVER exposes non-public individuals without
    manual review.

    Args:
        cohort: One of "MedicalMalpractice" / "EmployerBreach" / "GardaDiscrimination" /
                "EducationDiscrimination" / "AdmissionBreach" / "CivilActionOutline" /
                or "all" for all 7 pilots.
        pilot_party_id: Optional — one of the 7 pilot_party_id values
                (e.g. "pilot-qub-rvh"). If None, all matching pilots are returned.

    Returns:
        A dict with the keys:
          - dossiers: list of CompositePilotDossier dicts (one per matching pilot)
          - osint_ceiling_enforced: bool (always True)
          - analyst_review_required: bool (always True)
          - source_pdf_urls: list of leabharlann PDF URLs (read-only context)
          - extraction_confidence: float (0.0-1.0; the LLM-asserted confidence)
          - composite_pilot_metadata: dict with provenance + lineage
    """
    logger.info(
        "composite_pilot_invoked",
        extra={"cohort": cohort, "pilot_party_id": pilot_party_id},
    )

    # Filter the pilot parties by cohort / party_id
    selected_parties: list[dict[str, str]] = []
    if pilot_party_id is not None:
        selected_parties = [p for p in PILOT_PARTIES if p["party_id"] == pilot_party_id]
        if not selected_parties:
            return {
                "dossiers": [],
                "osint_ceiling_enforced": True,
                "analyst_review_required": True,
                "source_pdf_urls": [],
                "extraction_confidence": 0.0,
                "composite_pilot_metadata": {
                    "error": f"pilot_party_id {pilot_party_id!r} not in PILOT_PARTIES",
                    "valid_pilot_party_ids": [p["party_id"] for p in PILOT_PARTIES],
                },
            }
    elif cohort == "all":
        selected_parties = list(PILOT_PARTIES)
    else:
        selected_parties = [p for p in PILOT_PARTIES if p["cohort"] == cohort]

    # Build the source PDF list
    source_pdf_urls: list[str] = []
    for party in selected_parties:
        source_pdf_urls.append(party["leabharlann_pdf"])
        source_pdf_urls.extend(party["companion_pdfs"])

    # Generate one CompositePilotDossier per selected party
    # (in real implementation: each dossier goes through BAML ExtractCompositePilotDossier)
    dossiers: list[dict[str, Any]] = []
    for party in selected_parties:
        dossier = {
            "case_id": party["party_id"],
            "cohort": party["cohort"],
            "jurisdiction": party["sub_nation"],
            "court_level": "TRIBUNAL",  # default; BAML extraction will refine
            "parties": [
                {
                    "party_id": f"{party['party_id']}-claimant",
                    "display_name": "[redacted per PoI clause; see leabharlann PDF]",
                    "role": "Claimant",
                    "is_public_official": False,
                    "jurisdiction": party["sub_nation"],
                    "source_pdf_url": party["leabharlann_pdf"],
                    "extraction_confidence": 0.0,
                },
            ],
            "timeline": [],
            "statute_references": [],
            "precedent_judgments": [],
            "damages_estimate": None,
            "burden_of_proof": "BalanceOfProbabilities",
            "limitation_period_years": 2.0,
            "filing_form": None,
            "filing_fee_eur": None,
            "next_steps": [
                "Read the leabharlann PDF for full procedural detail",
                "Identify the relevant court (District / Circuit / High / Tribunal)",
                "Generate the Statement of Claim / WRC complaint / HSE complaint / PIAB form using the BAML Extract functions",
                "Manual review by a qualified solicitor or barrister before filing",
            ],
            "osint_ceiling_enforced": True,
            "analyst_review_required": True,
            "source_pdf_urls": [party["leabharlann_pdf"]] + party["companion_pdfs"],
            "extraction_confidence": 0.0,  # placeholder; BAML extraction populates
        }
        dossiers.append(dossier)

    return {
        "dossiers": dossiers,
        "osint_ceiling_enforced": True,
        "analyst_review_required": True,
        "source_pdf_urls": source_pdf_urls,
        "extraction_confidence": 0.0,  # populated per-dossier
        "composite_pilot_metadata": {
            "total_pilot_parties": len(PILOT_PARTIES),
            "selected_pilot_parties": len(selected_parties),
            "valid_cohorts": [
                "MedicalMalpractice",
                "EmployerBreach",
                "GardaDiscrimination",
                "EducationDiscrimination",
                "AdmissionBreach",
                "CivilActionOutline",
                "all",
            ],
            "lineage": "ciandlithe-repo-foundation-v1 + ciandlithe-composite-pilot-workflow-v1",
        },
    }


# -------------------------------------------------------------------
# 6 per-cohort FunctionTool stubs (each wraps composite_pilot_tool with
# a default cohort). Mirrors the cianchosaint precedent of one tool per
# vertical.
# -------------------------------------------------------------------
def medical_malpractice_tool(pilot_party_id: str | None = None) -> dict[str, Any]:
    return composite_pilot_tool(cohort="MedicalMalpractice", pilot_party_id=pilot_party_id)


def employer_breach_tool(pilot_party_id: str | None = None) -> dict[str, Any]:
    return composite_pilot_tool(cohort="EmployerBreach", pilot_party_id=pilot_party_id)


def garda_discrimination_tool(pilot_party_id: str | None = None) -> dict[str, Any]:
    return composite_pilot_tool(cohort="GardaDiscrimination", pilot_party_id=pilot_party_id)


def education_discrimination_tool(pilot_party_id: str | None = None) -> dict[str, Any]:
    return composite_pilot_tool(cohort="EducationDiscrimination", pilot_party_id=pilot_party_id)


def admission_breach_tool(pilot_party_id: str | None = None) -> dict[str, Any]:
    return composite_pilot_tool(cohort="AdmissionBreach", pilot_party_id=pilot_party_id)


def civil_action_outline_tool(pilot_party_id: str | None = None) -> dict[str, Any]:
    return composite_pilot_tool(cohort="CivilActionOutline", pilot_party_id=pilot_party_id)


__all__ = [
    "PILOT_PARTIES",
    "composite_pilot_tool",
    "medical_malpractice_tool",
    "employer_breach_tool",
    "garda_discrimination_tool",
    "education_discrimination_tool",
    "admission_breach_tool",
    "civil_action_outline_tool",
]


if __name__ == "__main__":
    import json
    result = composite_pilot_tool()
    print(json.dumps(result, indent=2))