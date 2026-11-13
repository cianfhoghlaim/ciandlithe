"""dlt_sources.law._context — EU + Commonwealth + European-context legal data.

This is the **context-data** layer (Phase 3.3 of the
``2026-08-24-dlt-sources-to-multi-repo-scaffold-v1`` change). Per the
v2 plan §A "context data" rules, this layer is **lower priority** than
the BI jurisdiction law content that lives at
``dlt_sources/law/<jurisdiction>/law/`` (Phase 3.1).

Structure
---------

- ``eu/eur_lex/`` — EU statute (CELVIC English-Irish alignment subset
  stays in cianfhoghlaim as BI-context; this is the **statute-only**
  EUR-Lex surface).
- ``commonwealth/<nation>/`` — Commonwealth law for the 6 primary
  nations: australia, canada, india, new_zealand, nigeria,
  south_africa. Canadian provinces + Nigerian states are flattened
  one level deeper: ``commonwealth/canada/<province>/``,
  ``commonwealth/nigeria/<state>/``.
- ``european_nations/<nation>/`` — European-context legal data for
  the 40 non-BI European nations (Germany, France, Spain, etc.).

Per the v2 plan §A + §B, this layer is for legal data from
jurisdictions that are NOT a primary British / Irish / Celtic-nation
educational entity (NCCA / SQA / WJEC / CCEA / IoM / Jersey /
Guernsey / UoG / NUI). The BI jurisdiction law content is the
primary surface; this ``_context/`` layer is secondary context.

The cianfhoghlaim (main) repo carries back-compat shims at the old
``dlt_sources.{european_union.eur_lex, commonwealth.<n>.law,
european_nations.<n>.law}`` paths that emit ``DeprecationWarning``
at import time.
"""
