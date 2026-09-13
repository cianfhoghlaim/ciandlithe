"""dlt_sources.law.guernsey._factory — Guernsey law pipeline factory.

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change.

Subclasses ``JurisdictionPipelineBase`` with ``STAGE = "law"``;
exposes ``guernsey_law_source``. SKELETON until Phase 3.2.
"""
from __future__ import annotations

from typing import ClassVar

import dlt

from dlt_sources._cross.jurisdiction_pipeline_base import (
    JurisdictionPipelineBase,
    get_dlt_destination,
)
from dlt_sources.law.guernsey.schema import (
    BritishIslesLegislationRow,
    legislation_rows,
)


class GuernseyLawJurisdictionPipeline(JurisdictionPipelineBase):
    """Guernsey legal pipeline (``STAGE = "law"``)."""

    STAGE: ClassVar[str] = "law"

    def __init__(self, *, use_md: bool = True) -> None:
        super().__init__("guernsey", use_md=use_md)
        self.destination = get_dlt_destination(use_ducklake=use_md)

    def build_pipeline_resource(self):
        return iter([])


@dlt.source(name="guernsey_law")
def guernsey_law_source(use_md: bool = True):
    @dlt.resource(
        name="legislation",
        write_disposition="merge",
        primary_key=["jurisdiction", "source_url"],
    )
    def legislation():
        for row in legislation_rows("guernsey"):
            yield BritishIslesLegislationRow(**row).model_dump()

    return legislation


guernsey_law_source.__doc__ = (
    "Guernsey law source — skeleton until Phase 3.2. Crown Dependency."
)