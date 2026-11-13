"""dlt_sources.law — BI legal system + EU + Commonwealth + European-context legal data.

This is the canonical sister-repo surface for the ``dlt_sources/law/``
subtree of ciandlíthe (the BI legal system sister repo).

Sub-trees
---------

- ``ciandlithe.<jurisdiction>.law`` — the **primary** BI jurisdiction law
  content (England, Wales, Scotland, Northern Ireland, Ireland, Jersey,
  Guernsey, Isle of Man). Added in Phase 3.1 of the
  ``2026-08-24-dlt-sources-to-multi-repo-scaffold-v1`` change.

- ``dlt_sources/law/_context/`` — the **context-data** layer (Phase 3.3):

  - ``_context/eu/eur_lex/`` — EU statute (CELVIC English-Irish
    alignment subset stays in cianfhoghlaim as BI-context; this dir is
    the **statute-only** EUR-Lex surface).
  - ``_context/commonwealth/<nation>/`` — Commonwealth law for the 6
    primary nations (australia, canada, india, new_zealand, nigeria,
    south_africa). Canadian provinces + Nigerian states are flattened
    one level deeper: ``_context/commonwealth/canada/<province>/``,
    ``_context/commonwealth/nigeria/<state>/``.
  - ``_context/european_nations/<nation>/`` — European-context legal
    data for the 40 non-BI European nations. Lower priority than the
    BI jurisdiction content per the v2 plan §A "context data" rules.

Per the v2 plan §A, the BI jurisdiction content is the primary surface
and the ``_context/`` layer is secondary context (lower priority, read-
mostly). Per the v2 plan §B the BI jurisdictions are the canonical home
for British / Irish / Celtic-nation law content; the ``_context/`` layer
is for legal data from jurisdictions that are NOT a primary British /
Irish / Celtic-nation educational entity (NCCA / SQA / WJEC / CCEA /
IoM / Jersey / Guernsey / UoG / NUI).

Back-compat shims
-----------------

The cianfhoghlaim (main) repo carries back-compat shims at the old
``dlt_sources.{european_union.eur_lex, commonwealth.<n>.law,
european_nations.<n>.law}`` paths that emit ``DeprecationWarning`` at
import time. The canonical implementations live here in ciandlíthe's
``dlt_sources/law/_context/``.

Per ``openspec/changes/2026-08-24-dlt-sources-to-multi-repo-scaffold-v1``
Phase 3.3 + the per-area AGENTS.md convention in
``dlt_sources/DATA_PLATFORM_ROUTER.md``.
"""
