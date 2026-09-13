"""dlt_sources.law.scotland.schema — Scotland law Pydantic schemas (skeleton).

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change.

SKELETON — the canonical ``BritishIslesLegislationRow`` schema is
re-exported from the England schema (the 8 BI jurisdictions share
the same per-act row shape; the ``jurisdiction`` field is the
per-jurisdiction discriminator). Phase 3.2 will replace the
empty ``legislation_rows()`` body with the real Scotland
legislation crawler.
"""
from __future__ import annotations

from dlt_sources.law.england.schema import (
    BritishIslesLegislationRow,
    legislation_rows,
)

__all__ = ["BritishIslesLegislationRow", "legislation_rows"]