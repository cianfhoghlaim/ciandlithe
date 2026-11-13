"""dlt_sources.law.jersey — Jersey legal data DLT sources.

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change,
the per-jurisdiction ``law/`` sled was carved out of
``dlt_sources/british_isles/jersey/law/`` in cianfhoghlaim.

Jersey is a **Crown Dependency** with its own legal system (based on
Norman customary law) and its own legislation source
(``jerseylaw.je`` — Jersey Legal Information Board).

**The actual legislation crawler code lives in cianfhoghlaim** under
``dlt_sources/law/jersey/british_isles/legislation.py``.

This ``__init__.py`` is the canonical 1-line re-export of the
``jersey_law_source`` binding.
"""
from __future__ import annotations

from dlt_sources.law.jersey._factory import jersey_law_source

__all__ = ["jersey_law_source"]