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
cianfhoghlaim.cianfhoghlaim.dlt.british_isles.england.medicine.nice — NICE clinical guidelines.

Source: `https://www.nice.org.uk/guidance` (publicly browseable,
bulk-download behind auth).
"""
from __future__ import annotations
import dlt


from collections.abc import Iterator
from typing import Any

import dlt_sources

from dlt_sources.common.site_crawler import crawl_site

def _crawl_source(*args, **kwargs):
    # The legacy _crawl_source took (source_name, base_url, ...) — source_name
    # was used only for logging in the legacy helper. The new crawl_site
    # primitive has no source_name, so we drop it if present.
    if args and isinstance(args[0], str) and args[0] == kwargs.get("source_name"):
        args = args[1:]
    kwargs.pop("source_name", None)
    for page in crawl_site(*args, **kwargs):
        yield page.to_dict()

NICE_URLS = {
    "guidance_published": "https://www.nice.org.uk/guidance/published",
    "guidance_in_development": "https://www.nice.org.uk/guidance/in-development",
    "about": "https://www.nice.org.uk/about",
}


def _crawl_nice(max_pages: int = 30) -> Iterator[dict[str, Any]]:
    for url_key, url in NICE_URLS.items():
        for page in _crawl_source(
            source_name=f"nice.{url_key}",
            base_url=url,
            include_paths=["/guidance/published/*", "/guidance/in-development/*", "/about/*"],
            max_pages=max_pages,
            max_depth=2,
        ):
            page["nation"] = "en"
            page["domain"] = "medicine"
            page["entity"] = "nice"
            yield page


@dlt.source(name="nice")
def nice_source(max_pages: int = 30):
    @dlt.resource(name="guidelines_pages", write_disposition="merge", primary_key=["url"])
    def pages():
        yield from _crawl_nice(max_pages=max_pages)

    return pages
