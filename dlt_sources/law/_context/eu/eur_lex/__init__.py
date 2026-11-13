"""dlt_sources.law._context.eu.eur_lex — EU statute (statute-only).

Per the v2 plan §A, this is **statute-only** EUR-Lex. The English-
Irish alignment subset (``eur_lex_celvic/``) stays in cianfhoghlaim
as BI-context.

Modules
-------

- ``cjeu_case_law`` — CJEU case law
- ``decisions`` — EU institutional decisions
- ``directives`` — EU directives
- ``regulations`` — EU regulations
- ``treaties`` — EU treaties

Back-compat: the cianfhoghlaim (main) repo carries shims at the old
``dlt_sources.european_union.eur_lex.*`` paths that emit
``DeprecationWarning`` at import time.
"""
