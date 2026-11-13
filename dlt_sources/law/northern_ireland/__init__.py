"""dlt_sources.law.northern_ireland — Northern Ireland legal DLT sources.

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change,
the per-jurisdiction ``law/`` sled was carved out of
``dlt_sources/british_isles/northern_ireland/law/`` in cianfhoghlaim.

**The actual legislation crawler code lives in cianfhoghlaim** under
``dlt_sources/law/northern_ireland/british_isles/legislation.py``
(Northern Ireland uses UK statute + some Scottish law via the Good
Friday Agreement).

This ``__init__.py`` is the canonical 1-line re-export of the
``northern_ireland_law_source`` binding.
"""
from __future__ import annotations

from dlt_sources.law.northern_ireland._factory import northern_ireland_law_source

__all__ = ["northern_ireland_law_source"]