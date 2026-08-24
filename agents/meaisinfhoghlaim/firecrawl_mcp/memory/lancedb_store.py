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

"""LanceDB memory store — the vector-search backend over docs_index.

Per the `2026-08-14-firecrawl-corpus-and-portals` change, this
store queries the `lancedb://md:cianfhoghlaim/firecrawl_corpus/docs_index`
table (the canonical companion table populated by the
`firecrawl_corpus_loader.py`).

The store uses the shared BGE-M3 1024-d embeddings (the canonical
shared embedder from `cocoindex_flows/infrastructure/_lifespan.py`).
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LanceDBHit:
    """One LanceDB search hit."""

    chunk_id: str
    doc_id: str
    package: str
    url: str
    chunk_text: str
    score: float  # cosine similarity, 0..1


class LanceDBMemoryStore:
    """The LanceDB vector search backend.

    The companion table is at
    `lancedb://md:cianfhoghlaim/firecrawl_corpus/docs_index`. The
    embeddings are 1024-d BGE-M3 vectors (the canonical shared
    embedder).
    """

    def __init__(self, *, table_name: str = "firecrawl_corpus_docs_index") -> None:
        self.table_name = table_name

    def _get_table(self) -> Any:
        """Open the LanceDB table (lazy import)."""
        try:
            import lancedb

            db = lancedb.connect("md:cianfhoghlaim")
            return db.open_table(self.table_name)
        except ImportError:  # pragma: no cover
            logger.warning("LanceDBMemoryStore.runtime_unavailable")
            return None

    def search(self, query: str, *, k: int = 5) -> list[LanceDBHit]:
        """Search the corpus for the top-k chunks by vector similarity.

        Args:
            query: The natural-language query.
            k: The number of hits to return (default 5).

        Returns:
            A list of `LanceDBHit` ordered by score descending.
        """
        from agents.meaisinfhoghlaim.firecrawl_mcp.memory.router import (
            _embed_query,
        )

        embedding = _embed_query(query)
        tbl = self._get_table()
        if tbl is None:
            return []

        try:
            results = tbl.search(embedding).limit(k).to_list()
            return [
                LanceDBHit(
                    chunk_id=r["chunk_id"],
                    doc_id=r["doc_id"],
                    package=r["package"],
                    url=r["url"],
                    chunk_text=r["chunk_text"],
                    score=float(r.get("_distance", 0.0)),
                )
                for r in results
            ]
        except Exception as exc:
            logger.warning("LanceDBMemoryStore.search_failed: %s", exc)
            return []


__all__ = ["LanceDBMemoryStore", "LanceDBHit"]