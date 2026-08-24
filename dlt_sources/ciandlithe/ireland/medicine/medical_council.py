# CIANDLITHE wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/official-law-pipeline-migration-to-ciandlithe-v1/).
# Migrated to ciandlithe: 2026-08-24
# Licence: BUSL-1.1 v2 CIANDLITHE edition (per LICENSE.md)
# Cohort (BLIP v1): medical_malpractice | hse_nhs_complaints | statutes_si_court_rules | court_judgments_tribunal_decisions
# Ciandlithe constraints (per LICENSE.md §3.8 + §5.2):
#   - osint_ceiling_enforced = True (every extraction gated by the OSINT allowlist)
#   - analyst_review_required = True (every result marked for manual review)
#   - PoI clause: extractions naming non-public individuals fail
#   - No automated form submission to courts.ie / irishstatutebook.ie
#
# This file is part of the ciandlithe DLT British-Isles medicine source family.
# Source URLs (e.g. hse.ie / nhs.uk / gmc-uk.org / legislation.gov.uk / nidirect.gov.uk / scot.nhs.uk / phw.nhs.wales)
# are verbatim from the Cianfhoghlaim version. These public-sector bodies are named in the ciandlithe
# OSINT allowlist (per the ciandlithe-repo-foundation-v1 openspec change, Requirement: OSINT source URL allowlist).
#
"""
cianfhoghlaim.cianfhoghlaim.dlt.british_isles.ireland.medicine.medical_council — Medical Council of Ireland.

Source: `https://www.medicalcouncil.ie/register/` (public search).
This is a *public search* source (not the authenticated register
download — that is reserved for the future
`domain-source-registry/v2` change).
"""
from __future__ import annotations
import dlt


from collections.abc import Iterator
from datetime import UTC, datetime
from typing import Any

import dlt_sources
import structlog

logger = structlog.get_logger(__name__)


MEDICAL_COUNCIL_URLS = {
    "register_search": "https://www.medicalcouncil.ie/register/",
    "doctors_search": "https://www.medicalcouncil.ie/public-information/register-of-medical-practitioners/",
}


def _scrape_register(max_pages: int = 20) -> Iterator[dict[str, Any]]:
    """Scrape the public register page. Per-record practitioner lookups
    require authenticated access; the public search page yields the
    searchable structure."""
    for url_key, url in MEDICAL_COUNCIL_URLS.items():
        try:
            import httpx

            response = httpx.get(url, timeout=30.0)
            response.raise_for_status()
        except (httpx.HTTPError, httpx.TimeoutException) as exc:
            logger.warning(
                "medical_council_fetch_failed",
                url=url,
                error=str(exc),
            )
            yield {
                "url": url,
                "status": "error",
                "error": str(exc),
                "nation": "ie",
                "domain": "medicine",
                "entity": "medical_council",
                "fetched_at": datetime.now(UTC).isoformat(),
            }
            continue
        yield {
            "url": url,
            "page_key": url_key,
            "title": "Medical Council of Ireland — Public register",
            "html": response.text,
            "status": "success",
            "nation": "ie",
            "domain": "medicine",
            "entity": "medical_council",
            "fetched_at": datetime.now(UTC).isoformat(),
        }


@dlt.source(name="medical_council_ie")
def medical_council_source(max_pages: int = 20):
    """DLT source for the Medical Council of Ireland (public search)."""

    @dlt.resource(
        name="register_pages",
        write_disposition="merge",
        primary_key=["url"],
    )
    def register_pages():
        yield from _scrape_register(max_pages=max_pages)

    return register_pages
