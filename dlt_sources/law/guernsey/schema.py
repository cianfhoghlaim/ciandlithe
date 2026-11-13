"""dlt_sources.law.guernsey.schema — Guernsey law Pydantic schemas (skeleton).

SKELETON — re-exports the shared ``BritishIslesLegislationRow`` schema.
"""
from __future__ import annotations

from dlt_sources.law.england.schema import (
    BritishIslesLegislationRow,
    legislation_rows,
)

__all__ = ["BritishIslesLegislationRow", "legislation_rows"]