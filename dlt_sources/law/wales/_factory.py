"""dlt_sources.law.wales._factory — Wales law pipeline factory.

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change.

Subclasses ``JurisdictionPipelineBase`` with ``STAGE = "law"``;
exposes ``wales_law_source``. SKELETON until Phase 3.2 moves the
real legislation crawler.
"""
from __future__ import annotations

from typing import ClassVar

import dlt

from dlt_sources._cross.jurisdiction_pipeline_base import (
    JurisdictionPipelineBase,
    get_dlt_destination,
)
from dlt_sources.law.wales.schema import (
    BritishIslesLegislationRow,
    legislation_rows,
)


class WalesLawJurisdictionPipeline(JurisdictionPipelineBase):
    """Wales legal pipeline (``STAGE = "law"``)."""

    STAGE: ClassVar[str] = "law"

    def __init__(self, *, use_md: bool = True) -> None:
        super().__init__("wales", use_md=use_md)
        self.destination = get_dlt_destination(use_ducklake=use_md)

    def build_pipeline_resource(self):
        return iter([])


@dlt.source(name="wales_law")
def wales_law_source(use_md: bool = True):
    @dlt.resource(
        name="legislation",
        write_disposition="merge",
        primary_key=["jurisdiction", "source_url"],
    )
    def legislation():
        for row in legislation_rows("wales"):
            yield BritishIslesLegislationRow(**row).model_dump()

    return legislation


wales_law_source.__doc__ = (
    "Wales law source — skeleton until Phase 3.2 EU/CW carve-out."
)