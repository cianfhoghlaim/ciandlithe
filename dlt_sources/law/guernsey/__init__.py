"""dlt_sources.law.guernsey — Guernsey legal data DLT sources.

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change,
the per-jurisdiction ``law/`` sled was carved out of
``dlt_sources/british_isles/guernsey/law/`` in cianfhoghlaim.

Guernsey is a **Crown Dependency** with its own legal system and its
own legislation source (``guernseylegalresources.gg`` — the Royal
Court of Guernsey).

**The actual legislation crawler code lives in cianfhoghlaim** under
``dlt_sources/law/guernsey/british_isles/legislation.py``.

This ``__init__.py`` is the canonical 1-line re-export of the
``guernsey_law_source`` binding.
"""
from __future__ import annotations

from dlt_sources.law.guernsey._factory import guernsey_law_source

__all__ = ["guernsey_law_source"]