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

"""Graphiti memory store — the temporal knowledge graph backend.

Per the `2026-08-14-firecrawl-corpus-and-portals` change, this
store wraps Graphiti (the canonical temporal knowledge graph
backend) with a docs_index facade. Use for temporal queries like
"What was the Dagster API in version 1.10?".

Per the `agent-memory-systems` spec, Graphiti is the recommended
default for temporal versioning because of the bi-temporal model
(event time + ingestion time).
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GraphitiHit:
    """One Graphiti temporal-graph hit."""

    entity_id: str
    entity_name: str
    entity_type: str
    valid_at: str  # event time
    ingested_at: str  # ingestion time
    summary: str
    score: float = 0.0


class GraphitiMemoryStore:
    """The Graphiti temporal knowledge graph backend.

    Uses the canonical `graphiti_core` package with the canonical
    FalkorDB driver (per the `.agents/skills/agent-memory-systems/SKILL.md`).
    """

    def __init__(self, *, group_id: str = "firecrawl_corpus") -> None:
        self.group_id = group_id

    def _get_client(self) -> Any:
        """Lazy-import the Graphiti client (CI-safe)."""
        try:
            from graphiti_core import Graphiti  # type: ignore[import-not-found]

            return Graphiti(
                uri="falkor://localhost:6379",
                group_id=self.group_id,
            )
        except ImportError:  # pragma: no cover — CI fallback
            logger.warning("GraphitiMemoryStore.runtime_unavailable")
            return None

    def search(self, query: str, *, k: int = 5) -> list[GraphitiHit]:
        """Search the temporal graph for the top-k entities.

        Args:
            query: The natural-language query (e.g.
                "What was the Dagster API in version 1.10?").
            k: The number of hits to return (default 5).

        Returns:
            A list of `GraphitiHit` ordered by score descending.
        """
        client = self._get_client()
        if client is None:
            return []

        try:
            results = client.search(query, limit=k)
            return [
                GraphitiHit(
                    entity_id=str(r.uuid),
                    entity_name=r.name,
                    entity_type=str(r.labels[0]) if r.labels else "entity",
                    valid_at=str(r.created_at),
                    ingested_at=str(r.created_at),
                    summary=r.summary,
                    score=float(r.score) if hasattr(r, "score") else 0.0,
                )
                for r in results
            ]
        except Exception as exc:
            logger.warning("GraphitiMemoryStore.search_failed: %s", exc)
            return []


__all__ = ["GraphitiMemoryStore", "GraphitiHit"]