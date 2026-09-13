"""dlt_sources.law.scotland.sources — Scotland law @dlt.source defs (skeleton).

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change.

SKELETON — real legislation crawler code lives in cianfhoghlaim at
``dlt_sources/law/scotland/british_isles/legislation.py`` and stays
there until Phase 3.2 (Subagent Q) moves the EU + Commonwealth
legislation sources into ciandlíthe.
"""
from __future__ import annotations

from dlt_sources.law.scotland._factory import (
    ScotlandLawJurisdictionPipeline,
    scotland_law_source,
)

__all__ = [
    "ScotlandLawJurisdictionPipeline",
    "scotland_law_source",
]