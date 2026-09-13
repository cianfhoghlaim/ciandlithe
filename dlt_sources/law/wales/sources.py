"""dlt_sources.law.wales.sources — Wales law @dlt.source defs (skeleton).

SKELETON — real legislation crawler code lives in cianfhoghlaim at
``dlt_sources/law/wales/british_isles/legislation.py`` until
Phase 3.2.
"""
from __future__ import annotations

from dlt_sources.law.wales._factory import (
    WalesLawJurisdictionPipeline,
    wales_law_source,
)

__all__ = [
    "WalesLawJurisdictionPipeline",
    "wales_law_source",
]