"""dlt_sources.law.ireland._factory — Ireland law pipeline factory.

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change.

Subclasses ``JurisdictionPipelineBase`` with ``STAGE = "law"``;
exposes ``ireland_law_source``. SKELETON until Phase 3.2 moves the
8 per-source legislation crawlers from
``dlt_sources/law/ireland/british_isles/`` in cianfhoghlaim.
"""
from __future__ import annotations

from typing import ClassVar

import dlt

from dlt_sources._cross.jurisdiction_pipeline_base import (
    JurisdictionPipelineBase,
    get_dlt_destination,
)
from dlt_sources.law.ireland.schema import (
    BritishIslesLegislationRow,
    legislation_rows,
)


class IrelandLawJurisdictionPipeline(JurisdictionPipelineBase):
    """Ireland legal pipeline (``STAGE = "law"``).

    The Ireland legal corpus has 8 separate OSINT sources
    (see ``__init__.py`` docstring). This subclass is the skeleton
    home for them in ciandlíthe; Phase 3.2 will migrate the 8
    per-source crawlers as parallel ``@dlt.resource`` defs and
    replace the no-op ``build_pipeline_resource()`` body.
    """

    STAGE: ClassVar[str] = "law"

    def __init__(self, *, use_md: bool = True) -> None:
        super().__init__("ireland", use_md=use_md)
        self.destination = get_dlt_destination(use_ducklake=use_md)

    def build_pipeline_resource(self):
        return iter([])


@dlt.source(name="ireland_law")
def ireland_law_source(use_md: bool = True):
    @dlt.resource(
        name="legislation",
        write_disposition="merge",
        primary_key=["jurisdiction", "source_url"],
    )
    def legislation():
        for row in legislation_rows("ireland"):
            yield BritishIslesLegislationRow(**row).model_dump()

    return legislation


ireland_law_source.__doc__ = (
    "Ireland law source — skeleton until Phase 3.2 EU/CW carve-out "
    "(8 per-source OSINT pipelines: irish_statute_book, doj, lawreform, "
    "courts_ie, workplace_relations, injuries_ie, citizensinformation, "
    "gov_ie_law)."
)