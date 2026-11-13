"""dlt_sources.law.isle_of_man._factory — Isle of Man law pipeline factory.

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change.

Subclasses ``JurisdictionPipelineBase`` with ``STAGE = "law"``;
exposes ``isle_of_man_law_source``. SKELETON until Phase 3.2.
"""
from __future__ import annotations

from typing import ClassVar

import dlt

from dlt_sources._cross.jurisdiction_pipeline_base import (
    JurisdictionPipelineBase,
    get_dlt_destination,
)
from dlt_sources.law.isle_of_man.schema import (
    BritishIslesLegislationRow,
    legislation_rows,
)


class IsleOfManLawJurisdictionPipeline(JurisdictionPipelineBase):
    """Isle of Man legal pipeline (``STAGE = "law"``)."""

    STAGE: ClassVar[str] = "law"

    def __init__(self, *, use_md: bool = True) -> None:
        super().__init__("isle_of_man", use_md=use_md)
        self.destination = get_dlt_destination(use_ducklake=use_md)

    def build_pipeline_resource(self):
        return iter([])


@dlt.source(name="isle_of_man_law")
def isle_of_man_law_source(use_md: bool = True):
    @dlt.resource(
        name="legislation",
        write_disposition="merge",
        primary_key=["jurisdiction", "source_url"],
    )
    def legislation():
        for row in legislation_rows("isle_of_man"):
            yield BritishIslesLegislationRow(**row).model_dump()

    return legislation


isle_of_man_law_source.__doc__ = (
    "Isle of Man law source — skeleton until Phase 3.2. Crown Dependency."
)