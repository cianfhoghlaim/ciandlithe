"""dlt_sources.law.ireland — Irish legal data DLT sources.

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change,
the per-jurisdiction ``law/`` sled was carved out of
``dlt_sources/british_isles/ireland/law/`` in cianfhoghlaim.

**The actual legislation crawler code lives in cianfhoghlaim** under
``dlt_sources/law/ireland/british_isles/`` — covering:

- ``irish_statute_book.py`` (the irishstatutebook.ie ELI walker)
- ``doj.py`` (Department of Justice)
- ``lawreform.py`` (Law Reform Commission)
- ``courts_ie.py`` (Courts Service Ireland)
- ``workplace_relations.py`` (WRC + ET)
- ``injuries_ie.py`` (Personal Injuries Assessment Board)
- ``citizensinformation.py`` (Citizens Information)
- ``gov_ie_law.py`` (gov.ie legal)

The Irish law corpus is the **richest** of the 8 BI jurisdictions
(it has 8 separate OSINT sources vs. the UK's 1 legislation.gov.uk
walker). Phase 3.2 will move all 8 sources into ciandlíthe as
parallel ``@dlt.resource`` defs under this jurisdiction directory.

This ``__init__.py`` is the canonical 1-line re-export of the
``ireland_law_source`` binding.
"""
from __future__ import annotations

from dlt_sources.law.ireland._factory import ireland_law_source

__all__ = ["ireland_law_source"]