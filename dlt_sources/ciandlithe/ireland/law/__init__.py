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

"""ciandlithe.dlt.british_isles.ireland.law — Ireland legal DLT sources.

Phase 6 of the openspec change. Covers both **statutory** law sources
(`irish_statute_book`, `doj`, `lawreform`) and the **operational** law
sources added in `2026-07-06-ireland-legal-pipeline` (`injuries_ie`,
`courts_ie`, `workplace_relations`, `citizensinformation`,
`gov_ie_law`).
"""
from __future__ import annotations

from dlt_sources.cianchosaint.ireland.law import (
    citizensinformation,
    courts_ie,
    doj,
    gov_ie_law,
    injuries_ie,
    irish_statute_book,
    lawreform,
    workplace_relations,
)

__all__ = [
    "citizensinformation",
    "courts_ie",
    "doj",
    "gov_ie_law",
    "injuries_ie",
    "irish_statute_book",
    "lawreform",
    "workplace_relations",
]
