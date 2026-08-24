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
cianfhoghlaim.cianfhoghlaim.dlt.british_isles.scotland.law.legislation — Scottish legislation.
Phase 7 of the openspec change.
"""
from __future__ import annotations
import dlt


import dlt_sources
from dlt_sources.law._legislation_helper import _crawl_legislation


@dlt.source(name="sct_legislation")
def sct_legislation_source(max_pages: int = 50):
    @dlt.resource(
        name="acts",
        write_disposition="merge",
        primary_key=["url"],
    )
    def acts():
        yield from _crawl_legislation(
            jurisdiction_code="sct",
            include_paths=["/asp/*", "/ssi/*", "/sdsi/*"],
            max_pages=max_pages,
        )

    return acts
