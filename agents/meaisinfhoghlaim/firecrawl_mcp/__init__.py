# CIANDLITHE wholesale-copy of cianfhoghlaim/ciandlithe + cianfhoghlaim/cianfhoghlaim @ main branch.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/ciandlithe-repo-bootstrap-v2/specs/ciandlithe-bootstrap-v2/spec.md).
# Migrated to ciandlithe: 2026-08-23
# Licence: BUSL-1.1 v2 CIANDLITHE edition (per LICENSE.md)
#
# Part of the ciandlithe Google ADK agent framework. The 3 PATTERN files
# (tuatha_root_agent.py / celtic_tutor_agent.py / curriculum_comparison_agent.py)
# are wholesale-copied and serve as PATTERNS for the per-constituency
# GA / MET / PSNI root + specialist agents that ship in
# agents/ciandlithe/ (per the follow-up change
# `ciandlithe-per-constituency-agents-v1`).
#
# The 30+ education-specific ADK agents in Cianfhoghlaim (curriculum_agent,
# lc_subject_agent, gcse_subject_agent, alevel_subject_agent, voice_agent,
# mythology_narrator_agent, quest_guide_agent, email_triage_agent, etc.)
# are intentionally EXCLUDED from this wholesale-copy (out of scope for
# the civil-litigation domain).

"""Firecrawl MCP client — the 12-tool wrapper for the agent fleet.

Per the `2026-08-14-firecrawl-mcp-ccc-dual-search-v1` change, this
module is the canonical external search surface of the agent stack.
The `FirecrawlMCPClient` class wraps all 12 Firecrawl MCP tools
(`search`, `scrape`, `crawl`, `map`, `agent`, `interact`,
`batch_scrape`, `monitor_*`, `research_*`, `developer_search`,
`parse`, `ask`) with Pydantic validation + Langfuse `@observe`.

The 3 keyless tools (`firecrawl_search`, `firecrawl_scrape`,
`firecrawl_parse`) work without an API key; the 24 authenticated
tools require `FIRECRAWL_API_KEY` (auto-hydrated via the
Infisical `firecrawl-api-key` secret by the
`bonneagar/dagger/cianfhoghlaim_dagger/__init__.py` InfisicalSecret
contract).

The wrapper is the canonical surface for every agent-side call —
never call `firecrawl_*` tools directly. Per the
[`dual-search-architecture`](../../../openspec/specs/dual-search-architecture/spec.md)
spec.
"""
from __future__ import annotations

from .client import (
    AUTHENTICATED_TOOLS,
    KEYLESS_TOOLS,
    FirecrawlAgentResponse,
    FirecrawlAskResponse,
    FirecrawlBatchResponse,
    FirecrawlCrawlResponse,
    FirecrawlDeveloperSearchResponse,
    FirecrawlDeveloperSearchResult,
    FirecrawlInteractResponse,
    FirecrawlMapResponse,
    FirecrawlMCPClient,
    FirecrawlMonitorCheck,
    FirecrawlMonitorCreate,
    FirecrawlParseResponse,
    FirecrawlResearchPaper,
    FirecrawlResearchSearchResponse,
    FirecrawlScrapeResponse,
    FirecrawlSearchResponse,
    FirecrawlSearchResult,
    tools_available,
)

__all__ = [
    "AUTHENTICATED_TOOLS",
    "KEYLESS_TOOLS",
    "FirecrawlAgentResponse",
    "FirecrawlAskResponse",
    "FirecrawlBatchResponse",
    "FirecrawlCrawlResponse",
    "FirecrawlDeveloperSearchResponse",
    "FirecrawlDeveloperSearchResult",
    "FirecrawlInteractResponse",
    "FirecrawlMapResponse",
    "FirecrawlMCPClient",
    "FirecrawlMonitorCheck",
    "FirecrawlMonitorCreate",
    "FirecrawlParseResponse",
    "FirecrawlResearchPaper",
    "FirecrawlResearchSearchResponse",
    "FirecrawlScrapeResponse",
    "FirecrawlSearchResponse",
    "FirecrawlSearchResult",
    "tools_available",
]