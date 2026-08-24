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

"""Polyglot memory layer over the agent reference corpus.

Per the `2026-08-14-firecrawl-corpus-and-portals` change (Phase 4a),
exposes 3 memory backends (Graphiti + LanceDB + Cognee) over the
`cianfhoghlaim.firecrawl_corpus.docs_index` table + a router that
selects the right backend based on the intent of the agent query.

The 3 backends:

| Backend | Strength | Use case |
|:--|:--|:--|
| `Graphiti` | Temporal (bi-temporal) | "What was the Dagster API in version 1.10?" |
| `LanceDB` | Vector (HNSW) | "What's the relevant chunk for this code query?" |
| `Cognee` | Cross-doc graph | "How does BAML ExtractCurriculumSyllabus relate to CocoIndex _lifespan.py?" |

The router: see `router.py:MemoryRouter.route()`.
"""
from __future__ import annotations

from .cognee_store import CogneeMemoryStore
from .graphiti_store import GraphitiMemoryStore
from .lancedb_store import LanceDBMemoryStore
from .router import MemoryRouter, MemoryRouterResult

__all__ = [
    "CogneeMemoryStore",
    "GraphitiMemoryStore",
    "LanceDBMemoryStore",
    "MemoryRouter",
    "MemoryRouterResult",
]