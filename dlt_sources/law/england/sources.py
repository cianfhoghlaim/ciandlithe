"""dlt_sources.law.england.sources — England & Wales law @dlt.source defs.

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change.

SKELETON — the real legislation crawler code (the
``legislation.gov.uk`` XML/HTML walker that yields per-act rows)
lives in cianfhoghlaim at
``dlt_sources/law/england/british_isles/legislation.py`` and stays
there until Phase 3.2 (Subagent Q) moves the EU + Commonwealth
legislation sources into ciandlíthe.

This module is intentionally a placeholder. The Phase 3.2 carve-out
will populate it with the canonical ``england_law`` ``@dlt.source``
+ per-resource defs (acts + statutory-instrument + local-act + as
appropriate). The 8 BI jurisdictions will be populated in
the parallel Phase 3.1 + Phase 3.2 sequence.
"""
from __future__ import annotations

# Phase 3.2 TODO: from dlt_sources.law.england.british_isles.legislation import (
#     en_legislation_source,
# )
#
# For now this module is a no-op re-export of the canonical factory
# binding exposed at __init__.py level.
from dlt_sources.law.england._factory import (
    EnglandLawJurisdictionPipeline,
    england_law_source,
)

__all__ = [
    "EnglandLawJurisdictionPipeline",
    "england_law_source",
]