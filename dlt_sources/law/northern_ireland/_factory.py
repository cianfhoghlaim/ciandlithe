"""dlt_sources.law.northern_ireland._factory — Northern Ireland law pipeline.

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change.

Subclasses ``JurisdictionPipelineBase`` with ``STAGE = "law"``;
exposes ``northern_ireland_law_source``. SKELETON until Phase 3.2
moves the real legislation crawler.
"""
from __future__ import annotations

from typing import ClassVar

import dlt

from dlt_sources._cross.jurisdiction_pipeline_base import (
    JurisdictionPipelineBase,
    get_dlt_destination,
)
from dlt_sources.law.northern_ireland.schema import (
    BritishIslesLegislationRow,
    legislation_rows,
)


class NorthernIrelandLawJurisdictionPipeline(JurisdictionPipelineBase):
    """Northern Ireland legal pipeline (``STAGE = "law"``)."""

    STAGE: ClassVar[str] = "law"

    def __init__(self, *, use_md: bool = True) -> None:
        super().__init__("northern_ireland", use_md=use_md)
        self.destination = get_dlt_destination(use_ducklake=use_md)

    def build_pipeline_resource(self):
        return iter([])


@dlt.source(name="northern_ireland_law")
def northern_ireland_law_source(use_md: bool = True):
    @dlt.resource(
        name="legislation",
        write_disposition="merge",
        primary_key=["jurisdiction", "source_url"],
    )
    def legislation():
        for row in legislation_rows("northern_ireland"):
            yield BritishIslesLegislationRow(**row).model_dump()

    return legislation


northern_ireland_law_source.__doc__ = (
    "Northern Ireland law source — skeleton until Phase 3.2."
)