"""dlt_sources.law._context.commonwealth — Commonwealth law context.

Lower-priority context for the BI jurisdiction pipelines per the v2
plan §A "context data" rules.

Six primary nations: australia, canada, india, new_zealand, nigeria,
south_africa. Canadian provinces + Nigerian states are flattened one
level deeper: ``canada/<province>/``, ``nigeria/<state>/``.

Back-compat: the cianfhoghlaim (main) repo carries shims at the old
``dlt_sources.commonwealth.<n>.law.*`` paths that emit
``DeprecationWarning`` at import time.
"""
