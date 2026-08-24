# CIANDLITHE wholesale-copy of cianfhoghlaim/cianchosaint @ main branch + cianfhoghlaim/cianfhoghlaim.
#
# Original: cianfhoghlaim/cianchosaint (per the openspec/changes/cianchosaint-ireland-law-migration-to-ciandlithe-v1/).
# Migrated to ciandlithe: 2026-08-24
# Licence: BUSL-1.1 v2 CIANDLITHE edition (per LICENSE.md)
# Cohort (BLIP v1): civil_litigation_forms | medical_malpractice | personal_injury_piab_nhs |
#                    workplace_relations_wrc_et | hse_nhs_complaints | statutes_si_court_rules |
#                    court_judgments_tribunal_decisions
#
# This file is part of the ciandlithe DLT Irish law source family.
# It is a wholesale-copy of the corresponding Cianchosaint file at
# dlt_sources/ciandlithe/ireland/law/<X>.py, with the destination
# path renamed to dlt_sources/ciandlithe/ireland/law/<X>.py.
#
# Source URLs (e.g. irishstatutebook.ie/eli/<year>/act/<number>/enacted/en/xml)
# are verbatim from the Cianfhoghlaim version. The Irish Statute
# Book / Courts.ie / Department of Justice / Citizens Information /
# Law Reform Commission / Workplace Relations / Injuries Board / GOV.IE
# legal content is public-sector OSINT and falls within the ciandlithe
# OSINT allowlist (per the ciandlithe-repo-foundation-v1 openspec
# change, Requirement: OSINT source URL allowlist).
#
# The wholesale-copy preserves the original implementation including
# the @dlt.source + @dlt.resource decorators + the SOURCE_BASE URLs +
# the content-hash + metadata extraction patterns.

"""
cianfhoghlaim.cianfhoghlaim.dlt.british_isles.ireland.law.workplace_relations —
Workplace Relations Commission (WRC) of Ireland.

Source: `https://workplacerelations.ie/en/` — the ~6,000 published
Adjudication Decisions per year covering unfair dismissal, employment
equality, payment of wages, working time, redundancy, etc.

Covers 2 DLT resources:

- `pages`     — procedures, complaint-type pages, forms, news
- `decisions` — published WRC Adjudication Decisions (merged on `case_ref`)

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/workplacerelations.ie/`.
"""
from __future__ import annotations
import dlt


from collections.abc import Iterator
from typing import Any

import structlog

import dlt_sources

logger = structlog.get_logger(__name__)

from dlt_sources.british_isles.ireland.education.curriculum import (  # type: ignore[import-not-found]
    _crawl_source,
)

WRC_BASE = "https://workplacerelations.ie/en"

# WRC decision database + complaint procedure sub-trees
WRC_PAGES_PATHS = [
    "/complaints-and-disputes/*",
    "/procedures/*",
    "/forms/*",
    "/news/*",
    "/publications/*",
    "/about-us/*",
]

WRC_DECISIONS_PATHS = [
    "/decisions/*",
    "/enforcement-decisions/*",
    "/adjudication-decisions/*",
]


def _crawl_wrc_pages(max_pages: int = 100) -> Iterator[dict[str, Any]]:
    """Crawl the WRC procedure pages (complaint types, forms, news)."""
    for page in _crawl_source(
        source_name="wrc.pages",
        base_url=WRC_BASE,
        include_paths=WRC_PAGES_PATHS,
        max_pages=max_pages,
        max_depth=3,
    ):
        page["nation"] = "ie"
        page["domain"] = "law"
        page["entity"] = "wrc"
        page["entity_type"] = "page"
        yield page


def _crawl_wrc_decisions(max_pages: int = 300) -> Iterator[dict[str, Any]]:
    """Crawl the WRC published Adjudication Decisions database.

    Each decision page typically has a `case_ref` (e.g.
    `ADJ-00012345-2024`) in the URL or as a heading. The BAML fn
    `b.ExtractWRCDecision` will extract the structured fields in L2.
    """
    for page in _crawl_source(
        source_name="wrc.decisions",
        base_url=WRC_BASE,
        include_paths=WRC_DECISIONS_PATHS,
        max_pages=max_pages,
        max_depth=4,
    ):
        page["nation"] = "ie"
        page["domain"] = "law"
        page["entity"] = "wrc"
        page["entity_type"] = "decision"
        yield page


@dlt.source(name="workplace_relations")
def workplace_relations_source(max_pages: int = 300):
    """DLT source for the Workplace Relations Commission (WRC).

    Returns 2 resources:

    - `pages`     — procedures, complaint-type pages, forms
    - `decisions` — published WRC Adjudication Decisions
    """

    @dlt.resource(
        name="pages",
        write_disposition="merge",
        primary_key=["url"],
    )
    def pages():
        yield from _crawl_wrc_pages(max_pages=max_pages // 3)

    @dlt.resource(
        name="decisions",
        write_disposition="merge",
        primary_key=["url"],
    )
    def decisions():
        yield from _crawl_wrc_decisions(max_pages=max_pages)

    return pages, decisions
