"""dlt_sources.law.isle_of_man.sources — IoM law @dlt.source defs (skeleton).

SKELETON — real legislation crawler code lives in cianfhoghlaim at
``dlt_sources/law/isle_of_man/british_isles/legislation.py`` until
Phase 3.2.
"""
from __future__ import annotations

from dlt_sources.law.isle_of_man._factory import (
    IsleOfManLawJurisdictionPipeline,
    isle_of_man_law_source,
)

__all__ = [
    "IsleOfManLawJurisdictionPipeline",
    "isle_of_man_law_source",
]