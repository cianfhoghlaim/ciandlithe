# CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Part of the cianchosaint Google ADK agent framework. The 3 PATTERN files
# (tuatha_root_agent.py / celtic_tutor_agent.py / curriculum_comparison_agent.py)
# are wholesale-copied and serve as PATTERNS for the per-constituency
# GA / MET / PSNI root + specialist agents that ship in
# agents/cianchosaint/ (per the follow-up change
# `cianchosaint-per-constituency-agents-v1`).
#
# The 30+ education-specific ADK agents in Cianfhoghlaim (curriculum_agent,
# lc_subject_agent, gcse_subject_agent, alevel_subject_agent, voice_agent,
# mythology_narrator_agent, quest_guide_agent, email_triage_agent, etc.)
# are intentionally EXCLUDED from this wholesale-copy (out of scope for
# the defence / policing / intelligence-oversight domain).

"""Cognee memory store — the cross-doc graph backend.

Per the `2026-08-14-firecrawl-corpus-and-portals` change, this
store wraps the canonical Cognee pipeline with a docs_index facade.
Use for cross-doc graph queries like "How does BAML
ExtractCurriculumSyllabus relate to CocoIndex _lifespan.py?".

Per the `agent-memory-systems` spec, Cognee is the canonical
knowledge graph (Neo4j-backed) for the 7-cluster corpus.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CogneeHit:
    """One Cognee graph hit."""

    entity_id: str
    name: str
    type: str
    description: str
    related_entities: list[str]
    score: float = 0.0


class CogneeMemoryStore:
    """The Cognee cross-doc graph backend."""

    def __init__(self, *, dataset: str = "firecrawl_corpus") -> None:
        self.dataset = dataset

    def _get_client(self) -> Any:
        """Lazy-import the Cognee client."""
        try:
            import cognee  # type: ignore[import-not-found]

            return cognee
        except ImportError:  # pragma: no cover — CI fallback
            logger.warning("CogneeMemoryStore.runtime_unavailable")
            return None

    def search(self, query: str, *, k: int = 5) -> list[CogneeHit]:
        """Search the cross-doc graph for the top-k entities.

        Args:
            query: The natural-language query.
            k: The number of hits to return (default 5).

        Returns:
            A list of `CogneeHit` ordered by score descending.
        """
        client = self._get_client()
        if client is None:
            return []

        try:
            # The canonical Cognee search API
            results = client.search(query, top_k=k)
            return [
                CogneeHit(
                    entity_id=str(r.get("id", "")),
                    name=r.get("name", ""),
                    type=r.get("type", "entity"),
                    description=r.get("description", ""),
                    related_entities=r.get("related", []),
                    score=float(r.get("score", 0.0)),
                )
                for r in results
            ]
        except Exception as exc:
            logger.warning("CogneeMemoryStore.search_failed: %s", exc)
            return []


__all__ = ["CogneeMemoryStore", "CogneeHit"]