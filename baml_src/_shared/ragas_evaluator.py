# CIANDLITHE — RAGAS evaluation pipeline (mirror of cianchosaint).
#
# Mirror of the cianchosaint `baml_src/_shared/ragas_evaluator.py` for ciandlithe.
#
# Per the openspec/changes/ciandlithe-ragas-eval-v1/specs/ciandlithe-blig-v1/spec.md.
#
# Used by the ciandlithe composite pilot + the BLIG v1 graph queries + the per-cohort
# BAML extraction schemas.
#
# License: BUSL-1.1 v2 CIANDLITHE edition (per LICENSE.md).

"""CIANDLITHE — RAGAS evaluation pipeline.

Mirror of the cianchosaint `ragas_evaluator.py` for ciandlithe.

Evaluates per-extraction RAGAS metrics for the 7 ciandlithe composite pilots
+ the per-cohort BAML extraction schemas.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


RAGAS_METRICS = [
    "ragas.faithfulness",
    "ragas.answer_relevancy",
    "ragas.context_recall",
    "ragas.context_precision",
    "ragas.context_entity_recall",
]

RAGAS_FAITHFULNESS_THRESHOLD = 0.70


@dataclass
class CiandlitheRAGASExtractionScores:
    """The RAGAS scores for one ciandlithe extraction."""

    extraction_id: str
    pilot_id: str  # The ciandlithe pilot id (e.g. "pilot-qub-rvh")
    cohort: str  # The BLIP v1 cohort (e.g. "medical_malpractice")
    scores: dict[str, float]
    passed_threshold: bool
    evaluated_at: str


class CiandlitheRAGASEvaluator:
    """The canonical RAGAS evaluator for ciandlithe."""

    def __init__(
        self,
        faithfulness_threshold: float = RAGAS_FAITHFULNESS_THRESHOLD,
    ) -> None:
        self.faithfulness_threshold = faithfulness_threshold

    def evaluate_composite_pilot(
        self,
        pilot_id: str,
        cohort: str,
        input_text: str,
        output_text: str,
        query: str = "",
    ) -> CiandlitheRAGASExtractionScores:
        """Evaluate the composite pilot's RAGAS metrics.

        Args:
            pilot_id: the canonical pilot id (e.g. "pilot-qub-rvh")
            cohort: the BLIP v1 cohort (e.g. "medical_malpractice")
            input_text: the leabharlann PDF text (read-only context)
            output_text: the composite pilot dossier JSON

        Returns:
            A CiandlitheRAGASExtractionScores.
        """
        from datetime import datetime, timezone

        # Heuristic evaluation (graceful degradation)
        scores = self._compute_heuristic(input_text, output_text)
        passed_threshold = all(
            scores.get(m, 0.0) >= self.faithfulness_threshold
            for m in RAGAS_METRICS
            if m in scores
        )

        return CiandlitheRAGASExtractionScores(
            extraction_id=pilot_id,
            pilot_id=pilot_id,
            cohort=cohort,
            scores=scores,
            passed_threshold=passed_threshold,
            evaluated_at=datetime.now(timezone.utc).isoformat(),
        )

    def _compute_heuristic(self, input_text: str, output_text: str) -> dict[str, float]:
        """Compute approximate RAGAS metrics via heuristic."""
        input_terms = set(input_text.lower().split())
        output_terms = set(output_text.lower().split())
        if not input_terms or not output_terms:
            return {m: 0.0 for m in RAGAS_METRICS}

        output_in_input = len(output_terms & input_terms)
        faithfulness = output_in_input / len(output_terms) if output_terms else 0.0
        answer_relevancy = min(1.0, len(output_text) / 1000.0) if len(output_text) > 0 else 0.0
        input_in_output = len(input_terms & output_terms)
        context_recall = input_in_output / len(input_terms) if input_terms else 0.0
        context_precision = len(output_terms) / max(len(output_text.split()), 1) if output_text else 0.0

        return {
            "ragas.faithfulness": round(faithfulness, 3),
            "ragas.answer_relevancy": round(answer_relevancy, 3),
            "ragas.context_recall": round(context_recall, 3),
            "ragas.context_precision": round(min(context_precision, 1.0), 3),
            "ragas.context_entity_recall": round(context_recall, 3),
        }

    def report_to_langfuse(
        self,
        scores: CiandlitheRAGASExtractionScores,
        trace_id: str,
    ) -> int:
        """Report the RAGAS scores to Langfuse."""
        try:
            from baml_src._shared.langfuse_client import report_ragas_scores
            return report_ragas_scores(trace_id=trace_id, scores=scores.scores)
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "ciandlithe_report_ragas_to_langfuse_failed",
                extra={"extraction_id": scores.extraction_id, "error": str(exc)},
            )
            return 0


__all__ = [
    "RAGAS_METRICS",
    "RAGAS_FAITHFULNESS_THRESHOLD",
    "CiandlitheRAGASEvaluator",
    "CiandlitheRAGASExtractionScores",
]