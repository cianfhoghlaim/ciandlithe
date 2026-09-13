"""dlt_sources.law.england._factory — England & Wales law pipeline factory.

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change.

This module subclasses ``JurisdictionPipelineBase`` (the Phase 1.3
merged base from cianfhoghlaim/cianchosaint, wholesale-copied into
ciandlíthe at ``dlt_sources/_cross/jurisdiction_pipeline_base.py``)
with ``STAGE = "law"`` and exposes the canonical
``england_law_source`` binding consumed by ``__init__.py``.

**SKELETON**: the per-jurisdiction law pipeline is a placeholder until
Phase 3.2 (the EU/CW carve-out) moves the legislation crawler code
from ``dlt_sources/law/england/british_isles/legislation.py`` (in
cianfhoghlaim) into ciandlíthe. This factory emits the
``england_law`` ``@dlt.source`` of the canonical
``BritishIslesLegislationRow`` schema (see ``schema.py``) but the
``build_pipeline_resource()`` body is intentionally a no-op
``return iter([])`` so the smoke test imports succeed today.
"""
from __future__ import annotations

from typing import ClassVar

import dlt
import dlt_sources

from dlt_sources._cross.jurisdiction_pipeline_base import (
    JurisdictionPipelineBase,
    get_dlt_destination,
)
from dlt_sources.law.england.schema import (
    BritishIslesLegislationRow,
    legislation_rows,
)


class EnglandLawJurisdictionPipeline(JurisdictionPipelineBase):
    """England & Wales legal pipeline (``STAGE = "law"``).

    The England & Wales legal corpus lives at
    ``dlt_sources/law/england/british_isles/legislation.py`` in
    cianfhoghlaim today. This subclass is the skeleton home for it
    in ciandlíthe; Phase 3.2 will migrate the legislation crawler
    into this jurisdiction directory and replace the no-op
    ``build_pipeline_resource()`` body.
    """

    STAGE: ClassVar[str] = "law"

    def __init__(self, *, use_md: bool = True) -> None:
        super().__init__("england", use_md=use_md)
        self.destination = get_dlt_destination(use_ducklake=use_md)

    def build_pipeline_resource(self):
        """No-op skeleton — Phase 3.2 will wire the legislation crawler."""
        # Phase 3.2 TODO: yield from legislation_rows("england", self.STAGE).
        return iter([])


@dlt.source(name="england_law")
def england_law_source(use_md: bool = True):
    """Canonical England & Wales law ``@dlt.source``.

    Skeleton for Phase 3.2; emits no rows today but the schema is
    the canonical ``BritishIslesLegislationRow`` (see ``schema.py``)
    that future Phase 3.2 work will populate.
    """

    @dlt.resource(
        name="legislation",
        write_disposition="merge",
        primary_key=["jurisdiction", "source_url"],
    )
    def legislation():
        for row in legislation_rows("england"):
            yield BritishIslesLegislationRow(**row).model_dump()

    return legislation


england_law_source.__doc__ = (
    "England & Wales law source — skeleton until Phase 3.2 EU/CW carve-out."
)