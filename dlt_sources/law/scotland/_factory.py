"""dlt_sources.law.scotland._factory — Scotland law pipeline factory.

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change.

This module subclasses ``JurisdictionPipelineBase`` (the Phase 1.3
merged base from cianfhoghlaim/cianchosaint, wholesale-copied into
ciandlíthe at ``dlt_sources/_cross/jurisdiction_pipeline_base.py``)
with ``STAGE = "law"`` and exposes the canonical
``scotland_law_source`` binding consumed by ``__init__.py``.

**SKELETON**: the per-jurisdiction law pipeline is a placeholder
until Phase 3.2 moves the legislation crawler code from
``dlt_sources/law/scotland/british_isles/legislation.py`` (in
cianfhoghlaim) into ciandlíthe.
"""
from __future__ import annotations

from typing import ClassVar

import dlt

from dlt_sources._cross.jurisdiction_pipeline_base import (
    JurisdictionPipelineBase,
    get_dlt_destination,
)
from dlt_sources.law.scotland.schema import (
    BritishIslesLegislationRow,
    legislation_rows,
)


class ScotlandLawJurisdictionPipeline(JurisdictionPipelineBase):
    """Scotland legal pipeline (``STAGE = "law"``)."""

    STAGE: ClassVar[str] = "law"

    def __init__(self, *, use_md: bool = True) -> None:
        super().__init__("scotland", use_md=use_md)
        self.destination = get_dlt_destination(use_ducklake=use_md)

    def build_pipeline_resource(self):
        return iter([])


@dlt.source(name="scotland_law")
def scotland_law_source(use_md: bool = True):
    @dlt.resource(
        name="legislation",
        write_disposition="merge",
        primary_key=["jurisdiction", "source_url"],
    )
    def legislation():
        for row in legislation_rows("scotland"):
            yield BritishIslesLegislationRow(**row).model_dump()

    return legislation


scotland_law_source.__doc__ = (
    "Scotland law source — skeleton until Phase 3.2 EU/CW carve-out."
)