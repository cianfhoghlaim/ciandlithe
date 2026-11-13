"""dlt_sources.law.england — England & Wales legal data DLT sources.

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change,
the per-jurisdiction ``law/`` sled was carved out of
``dlt_sources/british_isles/england/law/`` (the cianfhoghlaim
bi-jurisdiction-folder layout, created by the
``2026-08-24-wave-1-dlt-sources-domain-restructure-v1`` wave-1
restructure) into the dedicated ciandlíthe sister-repo
``dlt_sources/law/<jurisdiction>/`` layout.

**The actual legislation crawler code lives in cianfhoghlaim** under
``dlt_sources/law/england/british_isles/legislation.py`` (the
per-domain-folder layout created by wave-1). That code stays in
cianfhoghlaim until Phase 3.2 (the EU/CW carve-out, Subagent Q)
moves the European + Commonwealth legislation sources into
ciandlíthe as a parallel ``dlt_sources/law/<region>/<jurisdiction>/``
top-level layout.

This ``__init__.py`` is the canonical 1-line re-export of the
``england_law_source`` binding exposed by ``_factory.py``. Future
Phase 3.2 work will replace this shim with a direct re-export
of the moved legislation crawler.
"""
from __future__ import annotations

from dlt_sources.law.england._factory import england_law_source

__all__ = ["england_law_source"]