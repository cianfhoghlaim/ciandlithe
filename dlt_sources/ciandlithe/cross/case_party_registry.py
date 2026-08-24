"""CIANDLITHE case-party registry.

The canonical registry of the 7 composite-pilot parties. Each entry
maps a pilot party id to its BLIP v1 cohort + sub-nation + display name.

This is the SINGLE SOURCE OF TRUTH for the composite pilot. The
composite_pilot FunctionTool (`agents/ciandlithe/tools/composite_pilot.py`)
imports `PILOT_PARTIES` from this module (not its own copy) to ensure
drift-free lineage.

Per LICENSE.md §5.2 (PoI clause): the registry does NOT include the
names of any non-public individuals. Only the leabharlann PDF file
names (which are public-facing Gemini Deep Research outputs) are
referenced.
"""

from __future__ import annotations

from typing import TypedDict


class PilotPartyEntry(TypedDict):
    party_id: str
    cohort: str
    sub_nation: str
    display_name: str
    leabharlann_pdf: str
    companion_pdfs: list[str]


PILOT_PARTIES: list[PilotPartyEntry] = [
    {
        "party_id": "pilot-qub-rvh",
        "cohort": "MedicalMalpractice",
        "sub_nation": "NI",
        "display_name": "QUB / Royal Victoria Hospital brain-injury",
        "leabharlann_pdf": "gemini_deep_research/law/qub_royal_victoria_malpractice.pdf",
        "companion_pdfs": [
            "gemini_deep_research/medical/misdiagnosis_brain_damage_recovery.pdf",
            "gemini_deep_research/law/maximizing_civil_suit_damages_against_qub.pdf",
        ],
    },
    {
        "party_id": "pilot-eric",
        "cohort": "EmployerBreach",
        "sub_nation": "CROSS_BORDER",
        "display_name": "Eric employer / breach of contract",
        "leabharlann_pdf": "gemini_deep_research/law/suing_ceo_for_breach_abuse_damages.pdf",
        "companion_pdfs": [
            "gemini_deep_research/law/cross_border_legal_action_research.pdf",
            "gemini_deep_research/law/monroes.pdf",
        ],
    },
    {
        "party_id": "pilot-garda",
        "cohort": "GardaDiscrimination",
        "sub_nation": "IRELAND",
        "display_name": "Garda discrimination / data-access",
        "leabharlann_pdf": "gemini_deep_research/law/garda_corruption_and_data_access.pdf",
        "companion_pdfs": [
            "gemini_deep_research/law/garda_data_and_accommodation_request.pdf",
            "gemini_deep_research/law/garda_brutality_dual_citizenship_and_justice.pdf",
        ],
    },
    {
        "party_id": "pilot-dkit",
        "cohort": "EducationDiscrimination",
        "sub_nation": "IRELAND",
        "display_name": "DkIT disability / education complaint",
        "leabharlann_pdf": "gemini_deep_research/law/discrimination_case_strategy_university_of_galway.pdf",
        "companion_pdfs": [
            "gemini_deep_research/law/cbd_discrimination_lawsuit_preparation.pdf",
            "gemini_deep_research/law/challenging_university_rejection_and_ombudsman_decision.pdf",
        ],
    },
    {
        "party_id": "pilot-nuig",
        "cohort": "EducationDiscrimination",
        "sub_nation": "IRELAND",
        "display_name": "NUIG / UoG rejection + abuse of power",
        "leabharlann_pdf": "gemini_deep_research/law/discrimination_case_strategy_university_of_galway.pdf",
        "companion_pdfs": [
            "gemini_deep_research/law/cbd_dispensary_manager_discrimination_lawsuit.pdf",
        ],
    },
    {
        "party_id": "pilot-ucl",
        "cohort": "AdmissionBreach",
        "sub_nation": "ENGLAND",
        "display_name": "UCL offer / DBS",
        "leabharlann_pdf": "gemini_deep_research/law/ucl_sar_equality_act_claim.pdf",
        "companion_pdfs": [],
    },
    {
        "party_id": "pilot-sodium-valproate",
        "cohort": "MedicalMalpractice",
        "sub_nation": "IRELAND",
        "display_name": "Sodium valproate / HSE misprescription",
        "leabharlann_pdf": "gemini_deep_research/medical/irish_sodium_valproate_inquiry_and_healthcare.pdf",
        "companion_pdfs": [
            "gemini_deep_research/medical/sodium_valproate_lawsuits_and_inquiries.pdf",
            "gemini_deep_research/medical/essential_tbi_medication.pdf",
        ],
    },
]


__all__ = ["PILOT_PARTIES", "PilotPartyEntry"]