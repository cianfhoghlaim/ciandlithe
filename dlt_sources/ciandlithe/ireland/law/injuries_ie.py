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
cianfhoghlaim.cianfhoghlaim.dlt.british_isles.ireland.law.injuries_ie — Personal
Injuries Assessment Board (PIAB) of Ireland.

Source: `https://www.injuries.ie/eng/` — the front-door for every personal
injury claim in Ireland. The PIAB process (Application → Assessment →
Award / Section 14 Notice of Permission to Seek Judicial Review) gates
~90% of High Court personal-injury litigation.

Covers 2 DLT resources:

- `pages`  — crawled process / forms / news / about pages
- `forms`  — PIAB forms catalogue (Application form A/B, consent forms,
            medical report forms, etc.)

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/injuries.ie/`.
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

PIAB_BASE = "https://www.injuries.ie/eng"

# Public-facing routes. The PIAB site has 4 logical sub-trees we crawl.
PIAB_PAGE_PATHS = [
    "/the-personal-injuries-assessment-board/*",
    "/about-us/*",
    "/services/*",
    "/application-process/*",
    "/contact-us/*",
    "/news/*",
]

PIAB_FORM_PATHS = [
    "/forms/*",
    "/application-form/*",
]


def _crawl_piab_pages(max_pages: int = 80) -> Iterator[dict[str, Any]]:
    """Crawl the PIAB informational pages (process, about, news)."""
    for page in _crawl_source(
        source_name="injuries_ie.pages",
        base_url=PIAB_BASE,
        include_paths=PIAB_PAGE_PATHS,
        max_pages=max_pages,
        max_depth=3,
    ):
        page["nation"] = "ie"
        page["domain"] = "law"
        page["entity"] = "piab"
        page["entity_type"] = "page"
        yield page


def _crawl_piab_forms(max_pages: int = 40) -> Iterator[dict[str, Any]]:
    """Crawl the PIAB forms catalogue (PDFs + form metadata pages)."""
    for page in _crawl_source(
        source_name="injuries_ie.forms",
        base_url=PIAB_BASE,
        include_paths=PIAB_FORM_PATHS,
        max_pages=max_pages,
        max_depth=3,
    ):
        page["nation"] = "ie"
        page["domain"] = "law"
        page["entity"] = "piab"
        page["entity_type"] = "form"
        yield page


@dlt.source(name="injuries_ie")
def injuries_ie_source(max_pages: int = 80):
    """DLT source for the Personal Injuries Assessment Board (PIAB).

    Returns 2 resources:

    - `pages` — process / about / news pages
    - `forms` — PIAB forms catalogue
    """

    @dlt.resource(
        name="pages",
        write_disposition="merge",
        primary_key=["url"],
    )
    def pages():
        yield from _crawl_piab_pages(max_pages=max_pages)

    @dlt.resource(
        name="forms",
        write_disposition="merge",
        primary_key=["url"],
    )
    def forms():
        yield from _crawl_piab_forms(max_pages=max_pages // 2)

    return pages, forms
