"""dlt_sources.law.isle_of_man — Isle of Man legal data DLT sources.

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change,
the per-jurisdiction ``law/`` sled was carved out of
``dlt_sources/british_isles/isle_of_man/law/`` in cianfhoghlaim.

Isle of Man is a **Crown Dependency** with its own legal system (Tynwald
the
parliament) and its own statute book (``legislation.im``).

**The actual legislation crawler code lives in cianfhoghlaim** under
``dlt_sources/law/isle_of_man/british_isles/legislation.py``.

This ``__init__.py`` is the canonical 1-line re-export of the
``isle_of_man_law_source`` binding.
"""
from __future__ import annotations

from dlt_sources.law.isle_of_man._factory import isle_of_man_law_source

__all__ = ["isle_of_man_law_source"]