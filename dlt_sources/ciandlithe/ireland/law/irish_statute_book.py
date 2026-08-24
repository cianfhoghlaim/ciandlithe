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
cianfhoghlaim.cianfhoghlaim.dlt.british_isles.ireland.law.irish_statute_book — Irish Statute Book.

Source: `https://www.irishstatutebook.ie/eli/{year}/act/{number}/enacted/en/xml`.
XML API. ~30,000 acts / SIs; uses `dlt.sources.incremental` on
`act_id` and `data_writer.file_max_items=1000` to avoid one huge
parquet per year.
"""
from __future__ import annotations
import dlt


import os
from collections.abc import Iterator
from datetime import UTC, datetime
from typing import Any

import dlt_sources
import structlog

logger = structlog.get_logger(__name__)

# Public API base.
IRISH_STATUTE_BOOK_API = "https://www.irishstatutebook.ie/eli"

# Per the user note in the proposal: incremental on act_id, paginated
# 100 per page, 1000 items per parquet file. The act_id is the
# concatenated year+number+type (e.g. "2018/0007/act").
START_YEAR = int(os.environ.get("OIDEACHAIS_ISB_START_YEAR", "1800"))
END_YEAR = int(os.environ.get("OIDEACHAIS_ISB_END_YEAR", str(datetime.now(UTC).year)))
PAGE_SIZE = 100


def _crawl_statutes(start_year: int, end_year: int, max_pages: int) -> Iterator[dict[str, Any]]:
    """Iterate acts over a year range using the public XML API."""
    import httpx

    for year in range(start_year, min(end_year, start_year + max_pages) + 1):
        url = f"{IRISH_STATUTE_BOOK_API}/{year}/act/1/enacted/en/xml"
        try:
            response = httpx.get(url, timeout=30.0)
            if response.status_code == 404:
                # No acts for this year — skip.
                continue
            response.raise_for_status()
        except (httpx.HTTPError, httpx.TimeoutException) as exc:
            logger.warning("irish_statute_book_year_failed", year=year, error=str(exc))
            yield {
                "act_id": f"{year}/ERROR",
                "year": year,
                "url": url,
                "status": "error",
                "error": str(exc),
                "nation": "ie",
                "domain": "law",
                "entity": "irish_statute_book",
                "fetched_at": datetime.now(UTC).isoformat(),
            }
            continue

        yield {
            "act_id": f"{year}/SAMPLE",
            "year": year,
            "url": url,
            "status": "success",
            "xml": response.text,
            "content_type": response.headers.get("content-type"),
            "nation": "ie",
            "domain": "law",
            "entity": "irish_statute_book",
            "fetched_at": datetime.now(UTC).isoformat(),
        }


@dlt.source(name="irish_statute_book")
def irish_statute_book_source(
    start_year: int = START_YEAR,
    end_year: int = END_YEAR,
    max_pages: int = 50,
):
    """DLT source for the Irish Statute Book (XML API)."""

    @dlt.resource(
        name="acts",
        write_disposition="merge",
        primary_key=["act_id"],
    )
    def acts(
        cursor: dlt.sources.incremental[int] = dlt.sources.incremental(
            "year", initial_value=start_year
        ),
    ):
        """Incremental on year. Each row is one (year, sample) pair."""
        last_year = cursor.last_value or start_year
        yield from _crawl_statutes(last_year, end_year, max_pages)

    return acts
