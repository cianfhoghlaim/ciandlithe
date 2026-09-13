# CIANDLITHE — `cocoindex_flows/ciandlithe/corpus/_classifier.py`
#
# Per the openspec/changes/ciandlithe-leabharlann-corpus-ingest-v1/
# specs/ciandlithe-leabharlann-corpus/spec.md, Requirement: The PDF
# → cohort classifier.
#
# Licence: BUSL-1.1 v2 CIANDLITHE edition (per LICENSE.md)
#
# Per LICENSE.md §3.8 + §5.2:
#   - osint_ceiling_enforced = True (always)
#   - analyst_review_required = True (always)
#   - PoI clause: non-public individuals are never named
"""CIANDLITHE PDF → cohort classifier.

Maps each leabharlann PDF to `(cohort, jurisdiction, case_cluster)`
using:
1. Filename heuristics (the leabharlann naming convention is
   `<topic>_<jurisdiction_or_subject>_<descriptor>.pdf`)
2. First-page text scan for jurisdictional / cohort keywords

Returns `cohort="unclassified"` if no signal is found (→ review
queue, never silent drop — see WO-1 §The cohort classifier).
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Canonical 13 BLIP v1 cohorts (per the WO-3 spec — see WO-3 for full
# enumeration). For WO-1 we only need to discriminate the 7 cohorts
# that the existing case_party_registry uses + a few obvious ones.
# The "unclassified" bucket catches the rest.
# ---------------------------------------------------------------------------

Cohort = Literal[
    "civil_litigation_forms",
    "medical_malpractice",
    "personal_injury_piab_nhs",
    "workplace_relations_wrc_et",
    "hse_nhs_complaints",
    "statutes_si_court_rules",
    "court_judgments_tribunal_decisions",
    "unclassified",
]


Jurisdiction = Literal[
    "IRELAND",
    "NI",
    "SCOTLAND",
    "WALES",
    "ENGLAND",
    "JERSEY",
    "GUERNSEY",
    "IOM",
    "CROSS_BORDER",
    "UK_WIDE",
    "UNKNOWN",
]


CaseCluster = Literal[
    "qub_rvh",
    "eric_employer",
    "garda_discrimination",
    "dkit_education",
    "nuig_education",
    "ucl_admission",
    "sodium_valproate",
    "sibling_misdiagnosis",
    "psychiatric_detention",
    "belfast_malpractice",
    "dsp_disability",
    "housing_eviction",
    "elder_abuse",
    "hate_crime",
    "teaching_council",
    "court_staff_perjury",
    "citizenship_cta",
    "medical_cannabis",
    "defamation",
    "hospitality",
    "unclassified",
]


# Heuristic patterns for cohort detection (filename + first-page text).
# Order matters: more specific patterns come first.
COHORT_PATTERNS: list[tuple[str, str]] = [
    (r"\bmedical[\s_-]?malpractice\b|\bclinical[\s_-]?negligence\b|\bmisdiagnos", "medical_malpractice"),
    (r"\bbrain[\s_-]?damage\b|\btbi\b|\btraumatic\b", "medical_malpractice"),
    (r"\bsodium[\s_-]?valproate\b", "medical_malpractice"),
    (r"\bhse\b|\bnhs\b|\bclinical[\s_-]?incident\b", "hse_nhs_complaints"),
    (r"\bdisabilit|\bdsp\b|\bappeal\b", "social_welfare_appeals_unused"),  # WO-3
    (r"\bpiab\b|\binjur", "personal_injury_piab_nhs"),
    (r"\bwrc\b|\bworkplace|\bemployment[\s_-]?tribunal", "workplace_relations_wrc_et"),
    (r"\bjudicial|\bscotcourts\b|\bnicts\b|\bcourts?\b|\bsupreme", "court_judgments_tribunal_decisions"),
    (r"\brulings?\b|\bregulation|\bnisi|\bsi\b|\beli\b|\bact\b|\bstatute", "statutes_si_court_rules"),
    (r"\bdisclosure|\bfoi\b|\bfoia\b", "civil_litigation_forms"),
]

JURISDICTION_PATTERNS: list[tuple[str, Jurisdiction]] = [
    (r"\bnorthern[\s_-]?ireland\b|\bni\b", "NI"),
    (r"\bscotland\b|\bscps\b|\bsheriff\b|\bnhs[\s_-]?scotland", "SCOTLAND"),
    (r"\bwales\b|\bsenedd\b|\bphw\b", "WALES"),
    (r"\bengland\b|\bnhs[\s_-]?england\b|\bjudicial[\s_-]?committee\b", "ENGLAND"),
    (r"\bjersey\b", "JERSEY"),
    (r"\bguernsey\b", "GUERNSEY"),
    (r"\b(isle[\s_-]?of[\s_-]?man|iom)\b", "IOM"),
    (r"\bireland\b|\bhse\b|\bcourts\.ie\b|\bcircuits?\b|\bgoa\b|\bsupreme[\s_-]?court\b|\bspecialist[\s_-]?division|\bgardai\b|\bgarda\b|\bsiptu\b", "IRELAND"),
    (r"\bcross[\s_-]?border\b|\bcta\b|\bcommon[\s_-]?travel", "CROSS_BORDER"),
    (r"\buk[\s_-]?wide\b|\bbritish[\s_-]?isles\b", "UK_WIDE"),
]

# Filename-level cluster hints (the leabharlann naming convention).
CLUSTER_FILENAME_PATTERNS: list[tuple[str, str]] = [
    (r"^qub", "qub_rvh"),
    (r"^brother_misdiagnosis", "sibling_misdiagnosis"),
    (r"^malpractice_belfast", "belfast_malpractice"),
    (r"^ciara_meehan|^medical_malpractice_lawsuit_against_irish_psychiatrist|^galway_mental_health|^mental_health", "psychiatric_detention"),
    (r"^disability|^dsp\b|^understate", "dsp_disability"),
    (r"^landlord_eviction|^english_noise_tenancy|^qub_discrimination_and_eviction", "housing_eviction"),
    (r"^elder_abuse", "elder_abuse"),
    (r"^comprehensive_framework_for_the_recovery_of_digital|^garda_prejudice|^hate_crime", "hate_crime"),
    (r"^teaching_council", "teaching_council"),
    (r"^legal_action_against_court_staff|^perjury", "court_staff_perjury"),
    (r"^comprehensive_jurisprudential|^dual_citizenship|^dual_passport|^irish_passport|^surname|^british_isles_cta", "citizenship_cta"),
    (r"^irish_high_court_echr_medical_cannabis|^ireland_s_medical_cannabis|^accessing_medical_cannabis", "medical_cannabis"),
    (r"^defamation_campaign_damage|^legal_defense_against_false", "defamation"),
    (r"^monroes\b|^taafes\b|^sult\b|^little_collins\b", "hospitality"),
    (r"^sodium_valproate", "sodium_valproate"),
    (r"^dsp_complaint", "dsp_disability"),
    (r"^cbd_discrimination_lawsuit", "civil_litigation_forms"),
    (r"^sinn_f_in\b|^burnham_streeting|^arlene_foster", "citizenship_cta"),
    (r"^irish_sodium_valproate", "sodium_valproate"),
    (r"^farage\b|^clacton_farage|^reform_corruption|^reform_richard_tice", "eric_employer"),
    (r"^sturgeon|^whistleblower_investigates_scottish|^russell_group_whistleblower", "psychiatric_detention"),
    (r"^irish_high_court", "court_judgments_tribunal_decisions"),
]


@dataclass(frozen=True)
class Classification:
    """The classifier's verdict for one PDF."""

    cohort: Cohort
    jurisdiction: Jurisdiction
    case_cluster: CaseCluster
    confidence: float
    matched_pattern: str = ""


def _slugify_basename(pdf_path: Path) -> str:
    """Lowercased basename without the .pdf extension."""
    return pdf_path.stem.lower().replace("_", " ").replace("-", " ")


def classify_by_filename(pdf_path: Path) -> CaseCluster | None:
    """Try filename-based classification first (fast + deterministic)."""
    basename = _slugify_basename(pdf_path)
    for pattern, cluster in CLUSTER_FILENAME_PATTERNS:
        if re.search(pattern, basename):
            return cluster  # type: ignore[return-value]
    return None


def classify_by_text(
    first_n_chars: str,
    filename_hint: CaseCluster | None = None,
) -> tuple[Cohort, Jurisdiction, str]:
    """Classify by first-N-chars of the PDF text."""
    text_lower = first_n_chars.lower()
    cohort = "unclassified"
    matched_pattern = ""
    for pattern, name in COHORT_PATTERNS:
        if re.search(pattern, text_lower):
            cohort = name  # type: ignore[assignment]
            matched_pattern = pattern
            break

    jurisdiction = "UNKNOWN"
    for pattern, name in JURISDICTION_PATTERNS:
        if re.search(pattern, text_lower):
            jurisdiction = name
            break

    return cohort, jurisdiction, matched_pattern


class CohortClassifier:
    """PDF → Classification mapper."""

    def __init__(self, max_text_chars: int = 4000) -> None:
        self.max_text_chars = max_text_chars

    def classify(self, pdf_path: Path) -> Classification:
        """Classify a single PDF."""
        from ._pdf_text import extract_first_n_chars

        filename_cluster = classify_by_filename(pdf_path)
        text = extract_first_n_chars(pdf_path, self.max_text_chars)
        cohort, jurisdiction, pattern = classify_by_text(text, filename_cluster)

        # If filename gave a cluster hint but text didn't match a cohort,
        # inherit the cluster's canonical cohort via a small lookup.
        if cohort == "unclassified" and filename_cluster is not None:
            cohort = self._cohort_for_cluster(filename_cluster)
            pattern = f"filename:{filename_cluster}"

        # Jurisdiction fallback: filename-based heuristics.
        if jurisdiction == "UNKNOWN":
            jurisdiction = self._jurisdiction_for_filename(pdf_path)

        # Confidence: 1.0 if matched via filename + text, lower otherwise.
        if filename_cluster is not None and pattern.startswith("filename:"):
            confidence = 0.7
        elif pattern:
            confidence = 0.85
        else:
            confidence = 0.4

        return Classification(
            cohort=cohort,  # type: ignore[arg-type]
            jurisdiction=jurisdiction,
            case_cluster=filename_cluster or "unclassified",
            confidence=confidence,
            matched_pattern=pattern,
        )

    @staticmethod
    def _cohort_for_cluster(cluster: CaseCluster) -> Cohort:
        """Map a known case_cluster to its primary cohort."""
        mapping: dict[str, str] = {
            "qub_rvh": "medical_malpractice",
            "sibling_misdiagnosis": "medical_malpractice",
            "psychiatric_detention": "medical_malpractice",
            "belfast_malpractice": "medical_malpractice",
            "sodium_valproate": "medical_malpractice",
            "medical_cannabis": "hse_nhs_complaints",
            "dsp_disability": "statutes_si_court_rules",
            "housing_eviction": "statutes_si_court_rules",
            "elder_abuse": "court_judgments_tribunal_decisions",
            "hate_crime": "court_judgments_tribunal_decisions",
            "teaching_council": "court_judgments_tribunal_decisions",
            "court_staff_perjury": "court_judgments_tribunal_decisions",
            "citizenship_cta": "statutes_si_court_rules",
            "defamation": "civil_litigation_forms",
            "hospitality": "workplace_relations_wrc_et",
            "eric_employer": "civil_litigation_forms",
            "unclassified": "unclassified",
        }
        return mapping.get(cluster, "unclassified")  # type: ignore[return-value]

    @staticmethod
    def _jurisdiction_for_filename(pdf_path: Path) -> Jurisdiction:
        basename = pdf_path.stem.lower()
        if "ni_" in basename or "_ni" in basename or basename.startswith("ni"):
            return "NI"
        if "scot" in basename:
            return "SCOTLAND"
        if "wales" in basename or "senedd" in basename:
            return "WALES"
        if "uk_" in basename or "british" in basename:
            return "UK_WIDE"
        return "UNKNOWN"

    def classify_all(
        self, pdf_paths: list[Path]
    ) -> list[tuple[Path, Classification]]:
        """Classify a batch of PDFs (used by the corpus flow + the
        smoke test).
        """
        return [(p, self.classify(p)) for p in pdf_paths]


__all__ = [
    "CaseCluster",
    "Classification",
    "Cohort",
    "CohortClassifier",
    "Jurisdiction",
    "classify_by_filename",
    "classify_by_text",
]