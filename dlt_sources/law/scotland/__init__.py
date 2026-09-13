"""dlt_sources.law.scotland — Scottish legal data DLT sources.

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change,
the per-jurisdiction ``law/`` sled was carved out of
``dlt_sources/british_isles/scotland/law/`` in cianfhoghlaim into the
dedicated ciandlíthe sister-repo ``dlt_sources/law/<jurisdiction>/``
layout.

**The actual legislation crawler code lives in cianfhoghlaim** under
``dlt_sources/law/scotland/british_isles/legislation.py`` (the
per-domain-folder layout created by wave-1). That code stays in
cianfhoghlaim until Phase 3.2 (the EU/CW carve-out, Subagent Q)
moves the European + Commonwealth legislation sources into
ciandlíthe as a parallel ``dlt_sources/law/<region>/<jurisdiction>/``
top-level layout.

This ``__init__.py`` is the canonical 1-line re-export of the
``scotland_law_source`` binding exposed by ``_factory.py``.
"""
from __future__ import annotations

from dlt_sources.law.scotland._factory import scotland_law_source

__all__ = ["scotland_law_source"]