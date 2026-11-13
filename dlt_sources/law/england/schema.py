"""dlt_sources.law.england.schema — England & Wales law Pydantic schemas.

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change.

SKELETON — the canonical ``BritishIslesLegislationRow`` schema
describes the per-act row shape that Phase 3.2 will populate from
the ``legislation.gov.uk`` crawler. Today the schema is the
single source of truth for the per-jurisdiction table shape;
``legislation_rows()`` returns an empty list until Phase 3.2.
"""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class BritishIslesLegislationRow(BaseModel):
    """Canonical per-act row shape for the BI jurisdiction law sled.

    The 8 BI jurisdictions (``england``, ``scotland``, ``wales``,
    ``northern_ireland``, ``ireland``, ``jersey``, ``guernsey``,
    ``isle_of_man``) all emit rows in this shape; the
    ``jurisdiction`` field is the per-jurisdiction discriminator
    (set to the canonical ISO-style jurisdiction code, e.g.
    ``england``, ``ie``, ``sct``, ``wls``, ``ni``, ``je``, ``gg``,
    ``iom``).
    """

    model_config = ConfigDict(extra="forbid")

    jurisdiction: str = Field(..., description="Per-jurisdiction code (england, sct, wls, ni, ie, je, gg, iom).")
    stage: str = Field(default="law", description="Vertical — always ``law`` for this sled.")
    source_url: str = Field(..., description="Canonical URL of the act / instrument on the legislation source.")
    title: str = Field(..., description="Long title of the act / instrument.")
    act_number: str | None = Field(default=None, description="Chapter / number / year identifier.")
    year: int | None = Field(default=None, description="Year of enactment.")
    language: str = Field(default="en", description="ISO-639-1 language code of the source.")
    last_verified: str | None = Field(default=None, description="ISO-8601 date the row was last verified.")
    content_sha256: str | None = Field(default=None, description="SHA-256 of the act's full text (populated by Phase 3.2).")


def legislation_rows(jurisdiction: str) -> list[dict[str, Any]]:
    """Return the per-jurisdiction legislation rows (skeleton — empty list).

    Phase 3.2 will replace this with the real per-jurisdiction
    legislation crawler (e.g. for ``england``: walk
    ``legislation.gov.uk`` ``/uksi/*`` + ``/ukpga/*`` + ``/ukla/*``
    + ``/uksro/*``).
    """
    return []