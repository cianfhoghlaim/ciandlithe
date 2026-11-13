"""dlt_sources.law.ireland.schema — Ireland law Pydantic schemas (skeleton).

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change.

SKELETON — re-exports the shared ``BritishIslesLegislationRow`` schema.
Phase 3.2 will add the per-source Pydantic models (one per OSINT
source: ``IrishStatuteBookRow``, ``DOJRow``, ``LawReformRow``,
`` ``CourtsIERow``, ``WorkplaceRelationsRow``, ``InjuriesIERow``,
`` ``CitizensInformationRow``, ``GovIeLawRow``).
"""
from __future__ import annotations

from dlt_sources.law.england.schema import (
    BritishIslesLegislationRow,
    legislation_rows,
)

__all__ = ["BritishIslesLegislationRow", "legislation_rows"]