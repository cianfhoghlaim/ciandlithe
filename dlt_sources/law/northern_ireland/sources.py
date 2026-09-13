"""dlt_sources.law.northern_ireland.sources — NI law @dlt.source defs (skeleton).

SKELETON — real legislation crawler code lives in cianfhoghlaim at
``dlt_sources/law/northern_ireland/british_isles/legislation.py``
until Phase 3.2.
"""
from __future__ import annotations

from dlt_sources.law.northern_ireland._factory import (
    NorthernIrelandLawJurisdictionPipeline,
    northern_ireland_law_source,
)

__all__ = [
    "NorthernIrelandLawJurisdictionPipeline",
    "northern_ireland_law_source",
]