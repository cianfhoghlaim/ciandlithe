"""dlt_sources.law._context.european_nations — European-context legal data.

Lower-priority context for the BI jurisdiction pipelines per the v2
plan §A "context data" rules. Covers the 40 non-BI European nations
(Germany, France, Spain, etc.).

The European BI nations (UK + Ireland) do **not** live here — their law
content is the primary BI jurisdiction surface under
``dlt_sources/law/<jurisdiction>/law/`` (Phase 3.1).

Back-compat: the cianfhoghlaim (main) repo carries shims at the old
``dlt_sources.european_nations.<n>.law.*`` paths that emit
``DeprecationWarning`` at import time.
"""
