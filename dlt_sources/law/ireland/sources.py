"""dlt_sources.law.ireland.sources — Ireland law @dlt.source defs (skeleton).

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change.

SKELETON — the 8 per-source legislation crawlers live in cianfhoghlaim
at ``dlt_sources/law/ireland/british_isles/``:

1. ``irish_statute_book.py`` — irishstatutebook.ie ELI walker
2. ``doj.py`` — Department of Justice
3. ``lawreform.py`` — Law Reform Commission
4. ``courts_ie.py`` — Courts Service Ireland
5. ``workplace_relations.py`` — WRC + ET (Employment Tribunal)
6. ``injuries_ie.py`` — Personal Injuries Assessment Board
7. ``citizensinformation.py`` — Citizens Information
8. ``gov_ie_law.py`` — gov.ie legal

Phase 3.2 will migrate all 8 as parallel ``@dlt.resource`` defs under
this jurisdiction directory.
"""
from __future__ import annotations

# Phase 3.2 TODO: from dlt_sources.law.ireland.british_isles import (
#     irish_statute_book,
#     doj,
#     lawreform,
#     courts_ie,
#     workplace_relations,
#     injuries_ie,
#     citizensinformation,
#     gov_ie_law,
# )
from dlt_sources.law.ireland._factory import (
    IrelandLawJurisdictionPipeline,
    ireland_law_source,
)

__all__ = [
    "IrelandLawJurisdictionPipeline",
    "ireland_law_source",
]