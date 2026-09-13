"""dlt_sources.law.wales — Welsh legal data DLT sources.

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change,
the per-jurisdiction ``law/`` sled was carved out of
``dlt_sources/british_isles/wales/law/`` in cianfhoghlaim into the
dedicated ciandlíthe sister-repo ``dlt_sources/law/<jurisdiction>/``
layout.

**The actual legislation crawler code lives in cianfhoghlaim** under
``dlt_sources/law/wales/british_isles/legislation.py``. That code
stays in cianfhoghlaim until Phase 3.2 (the EU/CW carve-out).

This ``__init__.py`` is the canonical 1-line re-export of the
``wales_law_source`` binding.
"""
from __future__ import annotations

from dlt_sources.law.wales._factory import wales_law_source

__all__ = ["wales_law_source"]