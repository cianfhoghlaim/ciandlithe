# CIANDLITHE — BIPP v2 cross-reference resolver.
#
# Per the openspec/changes/ciandlithe-bipp-v2-crossref-v1/specs/ciandlithe-blig-v1/spec.md.
#
# Maps the 7 ciandlithe composite pilots (per docs/case-study/composite-pilot.md)
# to the 7 BIPP v2 thematic cohorts (per cianchosaint/openspec/specs/cianchosaint-bipp-v2/spec.md).
#
# The cross-reference is the load-bearing data that the BLIG v1 graph queries
# (per the new ciandlithe-blig-v1-spec-v1).
#
# License: BUSL-1.1 v2 CIANDLITHE edition (per LICENSE.md).

"""CIANDLITHE — BIPP v2 cross-reference resolver.

The 7 ciandlithe composite pilots → the 7 BIPP v2 thematic cohorts.

| # | ciandlithe pilot | BIPP v2 cohort |
|---|------------------|----------------|
| 1 | pilot-qub-rd (medical_malpractice, NI) | ni_political_accountability |
| 2 | pilot-eric (employer_breach, cross-border) | reform_uk_devolved_branches |
| 3 | pilot-garda (garda_discrimination, ROI) | roi_political_accountability |
| 4 | pilot-dkit (education_discrimination, ROI) | roi_political_accountability |
| 5 | pilot-nuig (education_discrimination, ROI) | roi_political_accountability |
| 6 | pilot-ucl (admission_breach, England) | welsh_london_political_accountability |
| 7 | pilot-sodium-valproate (medical_malpractice, ROI) | roi_political_accountability |

The cross-reference enables the BLIG v1 graph to compose the
ciandlithe civil-litigation dossiers with the cianchosaint
political-accountability context.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class BippV2CohortReference:
    """The BIPP v2 cross-reference for a ciandlithe composite pilot."""

    ciandlithe_pilot_id: str
    ciandlithe_cohort: str  # medical_malpractice | employer_breach | etc
    bipp_v2_cohort_id: str
    bipp_v2_jurisdiction: str
    leabharlann_pdf_urls: list[str]
    related_political_entities: list[str] = field(default_factory=list)
    extraction_confidence: float = 1.0


# The canonical mapping (7 ciandlithe pilots → 7 BIPP v2 cohorts)
PILOT_TO_BIPP_V2_MAP: dict[str, BippV2CohortReference] = {
    "pilot-qub-rvh": BippV2CohortReference(
        ciandlithe_pilot_id="pilot-qub-rvh",
        ciandlithe_cohort="medical_malpractice",
        bipp_v2_cohort_id="ni_political_accountability",
        bipp_v2_jurisdiction="ni",
        leabharlann_pdf_urls=[
            "leabharlann/gemini_deep_research/politics/sinn_f_in_data_funding_and_foreign_influence.pdf",
            "leabharlann/gemini_deep_research/politics/sinn_f_in_history_and_funding_inquiry.pdf",
            "leabharlann/gemini_deep_research/politics/burnham_streeting_compromised_assets.pdf",
            "leabharlann/gemini_deep_research/politics/arlene_foster_research_plan_generation.pdf",
        ],
        related_political_entities=["Sinn Féin", "DUP", "NI Assembly", "Arlene Foster", "Burnham", "Streeting"],
        extraction_confidence=1.0,
    ),
    "pilot-eric": BippV2CohortReference(
        ciandlithe_pilot_id="pilot-eric",
        ciandlithe_cohort="employer_breach",
        bipp_v2_cohort_id="reform_uk_devolved_branches",
        bipp_v2_jurisdiction="cross_border",
        leabharlann_pdf_urls=[
            "leabharlann/gemini_deep_research/politics/farage_clacton_opposition_research_blueprint.md",
        ],
        related_political_entities=["Reform UK", "Richard Tice", "Monroes restaurant"],
        extraction_confidence=1.0,
    ),
    "pilot-garda": BippV2CohortReference(
        ciandlithe_pilot_id="pilot-garda",
        ciandlithe_cohort="garda_discrimination",
        bipp_v2_cohort_id="roi_political_accountability",
        bipp_v2_jurisdiction="ireland",
        leabharlann_pdf_urls=[
            "leabharlann/gemini_deep_research/politics/sinn_f_in_data_funding_and_foreign_influence.pdf",
            "leabharlann/gemini_deep_research/politics/farrell_sinn_f_in_and_united_ireland_rhetoric.pdf",
            "leabharlann/gemini_deep_research/politics/irish_political_strategy_and_performance_analysis.pdf",
        ],
        related_political_entities=["An Garda Síochána", "Sinn Féin", "Fine Gael", "Fianna Fáil"],
        extraction_confidence=1.0,
    ),
    "pilot-dkit": BippV2CohortReference(
        ciandlithe_pilot_id="pilot-dkit",
        ciandlithe_cohort="education_discrimination",
        bipp_v2_cohort_id="roi_political_accountability",
        bipp_v2_jurisdiction="ireland",
        leabharlann_pdf_urls=[
            "leabharlann/gemini_deep_research/politics/irish_education_policy_analysis.pdf",
            "leabharlann/gemini_deep_research/politics/fine_gael_coalition_strategy_analysis.pdf",
        ],
        related_political_entities=["DkIT", "Higher Education Authority", "Department of Further and Higher Education"],
        extraction_confidence=1.0,
    ),
    "pilot-nuig": BippV2CohortReference(
        ciandlithe_pilot_id="pilot-nuig",
        ciandlithe_cohort="education_discrimination",
        bipp_v2_cohort_id="roi_political_accountability",
        bipp_v2_jurisdiction="ireland",
        leabharlann_pdf_urls=[
            "leabharlann/gemini_deep_research/politics/galway_west_estection_candidate_analysis.pdf",
            "leabharlann/gemini_deep_research/politics/varadkar_controversies_and_political_future.pdf",
        ],
        related_political_entities=["University of Galway", "Galway West by-election", "Varadkar"],
        extraction_confidence=1.0,
    ),
    "pilot-ucl": BippV2CohortReference(
        ciandlithe_pilot_id="pilot-ucl",
        ciandlithe_cohort="admission_breach",
        bipp_v2_cohort_id="welsh_london_political_accountability",
        bipp_v2_jurisdiction="england",
        leabharlann_pdf_urls=[
            "leabharlann/gemini_deep_research/politics/london_boroughs_funding_and_cleanliness_investigation.pdf",
            "leabharlann/gemini_deep_research/politics/veolia_outsourcing_and_neglect_investigation.pdf",
        ],
        related_political_entities=["UCL", "London boroughs", "Veolia"],
        extraction_confidence=1.0,
    ),
    "pilot-sodium-valproate": BippV2CohortReference(
        ciandlithe_pilot_id="pilot-sodium-valproate",
        ciandlithe_cohort="medical_malpractice",
        bipp_v2_cohort_id="roi_political_accountability",
        bipp_v2_jurisdiction="ireland",
        leabharlann_pdf_urls=[
            "leabharlann/gemini_deep_research/politics/fine_gael_coalition_strategy_analysis.pdf",
            "leabharlann/gemini_deep_research/politics/varadkar_controversies_and_political_future.pdf",
            "leabharlann/gemini_deep_research/politics/galway_by_election_media_analysis.pdf",
            "leabharlann/gemini_deep_research/politics/irish_political_strategy_and_performance_analysis.pdf",
        ],
        related_political_entities=["HSE", "Fine Gael", "Varadkar", "Galway West by-election", "Department of Health"],
        extraction_confidence=1.0,
    ),
}


class BippV2CrossrefResolver:
    """The BIPP v2 cross-reference resolver for ciandlithe."""

    def resolve_related_cohort(
        self, ciandlithe_pilot_id: str
    ) -> BippV2CohortReference | None:
        """Resolve the BIPP v2 cohort reference for a ciandlithe composite pilot.

        Args:
            ciandlithe_pilot_id: the canonical pilot id (e.g. "pilot-qub-rvh")

        Returns:
            A BippV2CohortReference, or None if not found.
        """
        ref = PILOT_TO_BIPP_V2_MAP.get(ciandlithe_pilot_id)
        if ref is None:
            logger.warning(
                "bipp_v2_crossref_not_found",
                extra={"ciandlithe_pilot_id": ciandlithe_pilot_id},
            )
        return ref

    def resolve_all(self) -> list[BippV2CohortReference]:
        """Resolve all 7 cross-references."""
        return list(PILOT_TO_BIPP_V2_MAP.values())


__all__ = [
    "BippV2CohortReference",
    "BippV2CrossrefResolver",
    "PILOT_TO_BIPP_V2_MAP",
]