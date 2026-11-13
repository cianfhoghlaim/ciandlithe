"""dlt_sources.law.guernsey.sources — Guernsey law @dlt.source defs (skeleton).

SKELETON — real legislation crawler code lives in cianfhoghlaim at
``dlt_sources/law/guernsey/british_isles/legislation.py`` until Phase 3.2.
"""
from __future__ import annotations

from dlt_sources.law.guernsey._factory import (
    GuernseyLawJurisdictionPipeline,
    guernsey_law_source,
)

__all__ = [
    "GuernseyLawJurisdictionPipeline",
    "guernsey_law_source",
]