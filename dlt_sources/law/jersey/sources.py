"""dlt_sources.law.jersey.sources — Jersey law @dlt.source defs (skeleton).

SKELETON — real legislation crawler code lives in cianfhoghlaim at
``dlt_sources/law/jersey/british_isles/legislation.py`` until Phase 3.2.
"""
from __future__ import annotations

from dlt_sources.law.jersey._factory import (
    JerseyLawJurisdictionPipeline,
    jersey_law_source,
)

__all__ = [
    "JerseyLawJurisdictionPipeline",
    "jersey_law_source",
]