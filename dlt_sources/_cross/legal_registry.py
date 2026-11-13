"""dlt_sources._cross.legal_registry — CIANDLITHE cross-jurisdiction legal registry.

Per the **2026-09-XX-ciandlithe-initial-carveout-v1** openspec change.

This module is the canonical WRC + courts + statutory-law registry for
the 8 British Isles jurisdictions (``england``, ``scotland``, ``wales``,
``northern_ireland``, ``ireland``, ``jersey``, ``guernsey``,
``isle_of_man``). It subclasses
``JurisdictionPipelineBase`` (the Phase 1.3 merged base, wholesale-copied
into ciandlíthe at ``dlt_sources/_cross/jurisdiction_pipeline_base.py``)
and exposes a single ``@dlt.source`` that fans out to the 8 per-jurisdiction
``<jurisdiction>_law_source`` bindings registered under
``dlt_sources/law/<jurisdiction>/_factory.py``.

## Why a separate ``_cross/legal_registry.py`` module

The BIEP v3 cross-cutting registry (``british_isles/_cross/registry_api.py``
+ ``british_isles/_cross/registry_loader.py`` in cianfhoghlaim) covers the
**education** subject cohorts (the 1990 cohort rows from the Phase 1.3
base-class merge). The legal dimension is orthogonal:

- Each of the 8 BI jurisdictions has its own statutory-law source
  (``legislation.gov.uk`` for England/Scotland/Wales/NI,
  ``irishstatutebook.ie`` for Ireland, plus the 3 Crown Dependencies'
  own legislation sources).
- Each jurisdiction has its own court system (with per-court procedural
  rules) and its own WRC-equivalent (Workplace Relations Commission for
  Ireland, Employment Tribunal for England/Scotland/Wales, etc.).

The 1990 cohort rows are the **starting point** for the legal registry:
the per-jurisdiction ``load_<jurisdiction>_subjects()`` loader provides
the cohort shape, and this module wraps each cohort with the 3 legal
dimensions (statute + courts + WRC-equivalent).

## What lives here

- ``LegalCohortRow`` — Pydantic schema (the per-(jurisdiction, stage,
  subject, legal_source) row shape).
- ``LegalRegistryJurisdictionPipeline`` — ``JurisdictionPipelineBase``
  subclass with ``STAGE = "legal_registry"``.
- ``bi_legal_registry_source()`` — canonical ``@dlt.source`` that fans
  out to the 8 per-jurisdiction ``<jurisdiction>_law_source`` bindings.

## SKELETON

The fan-out body is intentionally a no-op for the cross-cutting
``legal_registry`` source today (the 8 per-jurisdiction
``<jurisdiction>_law_source`` bindings are also skeletons — see
``dlt_sources/law/<jurisdiction>/_factory.py``). Phase 3.2 (the
EU/CW carve-out, Subagent Q) will populate the per-jurisdiction
legislation crawlers; once those emit real rows, this
``bi_legal_registry_source()`` will fan them out and union them
into the canonical ``legal_registry`` BIEP v3 cross-cutting view.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, ClassVar

import dlt
import structlog
from pydantic import BaseModel, ConfigDict, Field

from dlt_sources._cross.jurisdiction_pipeline_base import (
    JurisdictionPipelineBase,
    VALID_JURISDICTIONS,
)

logger = structlog.get_logger(__name__)


# ─── Per-jurisdiction law-source imports (lazy) ─────────────────────────
#
# Done lazily so the smoke test can import this module even if one of
# the per-jurisdiction factories has a transient dep issue (Phase 3.2
# will tighten the imports as the real legislation crawlers land).


def _bi_jurisdiction_law_sources() -> dict[str, Any]:
    """Lazy-load the 8 per-jurisdiction ``<jurisdiction>_law_source`` bindings.

    Returns a dict keyed by jurisdiction code (the canonical 8 BI
    jurisdictions). Each binding is a ``@dlt.source`` callable; the
    canonical fan-out yields the union of all 8 per-jurisdiction
    resources into the ``bi_legal_registry`` cross-cutting view.
    """
    sources: dict[str, Any] = {}

    # Phase 3.2 will populate these for real; today they emit 0 rows
    # (the skeleton factory has an empty ``legislation_rows()`` body)
    # but the imports + smoke test succeed.
    try:
        from dlt_sources.law.england import england_law_source

        sources["england"] = england_law_source
    except ImportError:
        logger.warning("legal_registry.england_skipped", exc_info=True)

    try:
        from dlt_sources.law.scotland import scotland_law_source

        sources["scotland"] = scotland_law_source
    except ImportError:
        logger.warning("legal_registry.scotland_skipped", exc_info=True)

    try:
        from dlt_sources.law.wales import wales_law_source

        sources["wales"] = wales_law_source
    except ImportError:
        logger.warning("legal_registry.wales_skipped", exc_info=True)

    try:
        from dlt_sources.law.northern_ireland import northern_ireland_law_source

        sources["northern_ireland"] = northern_ireland_law_source
    except ImportError:
        logger.warning("legal_registry.northern_ireland_skipped", exc_info=True)

    try:
        from dlt_sources.law.ireland import ireland_law_source

        sources["ireland"] = ireland_law_source
    except ImportError:
        logger.warning("legal_registry.ireland_skipped", exc_info=True)

    try:
        from dlt_sources.law.jersey import jersey_law_source

        sources["jersey"] = jersey_law_source
    except ImportError:
        logger.warning("legal_registry.jersey_skipped", exc_info=True)

    try:
        from dlt_sources.law.guernsey import guernsey_law_source

        sources["guernsey"] = guernsey_law_source
    except ImportError:
        logger.warning("legal_registry.guernsey_skipped", exc_info=True)

    try:
        from dlt_sources.law.isle_of_man import isle_of_man_law_source

        sources["isle_of_man"] = isle_of_man_law_source
    except ImportError:
        logger.warning("legal_registry.isle_of_man_skipped", exc_info=True)

    return sources


# ─── Pydantic schema ────────────────────────────────────────────────────


class LegalCohortRow(BaseModel):
    """Canonical per-(jurisdiction, stage, subject, legal_source) row.

    Each BI jurisdiction emits rows in this shape; the ``jurisdiction``
    field discriminates. The ``stage`` field is the BIEP v3 stage
    (e.g. ``leaving_certificate``, ``gcse``, ``as_level``,
    ``national_5``, ``higher``, ``advanced_higher``, ``foundation``,
    ``primary``, ``junior_cycle``, ``senior_cycle``) and ``subject``
    is the BIEP v3 subject slug. The 3 legal dimensions are:

    - ``statute_source``: the per-jurisdiction statutory-law URL
      (e.g. ``https://www.legislation.gov.uk/`` for the UK,
      ``https://www.irishstatutebook.ie/`` for Ireland).
    - ``court_source``: the per-jurisdiction court-system URL
      (e.g. ``https://www.courts.ie/`` for Ireland).
    - ``wrc_source``: the per-jurisdiction workplace-relations URL
      (e.g. ``https://www.workplacerelations.ie/`` for Ireland).
    """

    model_config = ConfigDict(extra="forbid")

    jurisdiction: str = Field(..., description="BI jurisdiction code (england, scotland, wales, northern_ireland, ireland, jersey, guernsey, isle_of_man).")
    stage: str = Field(..., description="BIEP v3 education stage.")
    subject: str = Field(..., description="BIEP v3 subject slug.")
    board: str = Field(default="none", description="Exam board (aqa, ocr, edexcel, wjec, ccea, sqa, ccea_ni, none).")
    qualification_level: str = Field(default="untiered", description="hl / ol / fl / foundation_tier / higher_tier / untiered / year_1 / year_2 / year_3 / ty.")
    language: str = Field(default="en", description="ISO-639-1 language code (en, ga, cy, gd, gv).")
    statute_source: str = Field(..., description="Per-jurisdiction statutory-law URL (the canonical URL of the legislation source).")
    court_source: str = Field(..., description="Per-jurisdiction court-system URL (the canonical URL of the courts service).")
    wrc_source: str = Field(..., description="Per-jurisdiction workplace-relations URL (the WRC, ET, or equivalent).")
    natural_key: str = Field(..., description="Stable merge/dedup key: jurisdiction|stage|subject|board|qualification_level|language.")
    content_sha256: str = Field(..., description="SHA-256 of the canonical 3-tuple (statute_source + court_source + wrc_source).")
    last_verified: str = Field(default_factory=lambda: datetime.now(UTC).isoformat()[:10], description="ISO-8601 date the row was last verified.")
    ingested_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat(), description="ISO-8601 timestamp of ingestion.")


# ─── Per-jurisdiction legal-source defaults ────────────────────────────
#
# These 8-tuples capture the canonical (statute, court, WRC) URLs for
# the 8 BI jurisdictions. The order matches the BIEP v3 canonical
# ISO-style jurisdiction codes (england, scotland, wales, ni, ie, je, gg, iom).


BI_LEGAL_SOURCE_DEFAULTS: dict[str, tuple[str, str, str]] = {
    # (statute_source, court_source, wrc_source)
    "england": (
        "https://www.legislation.gov.uk/",
        "https://www.find-court-tribunal.service.gov.uk/",
        "https://www.gov.uk/government/organisations/hm-courts-and-tribunals-service",
    ),
    "scotland": (
        "https://www.legislation.gov.uk/",
        "https://www.scotcourts.gov.uk/",
        "https://www.employmenttribunals.scotland/",
    ),
    "wales": (
        "https://www.legislation.gov.uk/",
        "https://www.find-court-tribunal.service.gov.uk/",
        "https://www.gov.uk/government/organisations/hm-courts-and-tribunals-service",
    ),
    "northern_ireland": (
        "https://www.legislation.gov.uk/",
        "https://courtsni.nicourts.services/",
        "https://www.employmenttribunalsni.co.uk/",
    ),
    "ireland": (
        "https://www.irishstatutebook.ie/",
        "https://www.courts.ie/",
        "https://www.workplacerelations.ie/",
    ),
    "jersey": (
        "https://www.jerseylaw.je/",
        "https://www.jerseycourts.je/",
        "https://www.gov.je/Working/EmploymentProtection/Pages/default.aspx",
    ),
    "guernsey": (
        "https://www.guernseylegalresources.gg/",
        "https://www.guernseyroyalcourt.gg/",
        "https://www.gov.gg/employmenttribunal",
    ),
    "isle_of_man": (
        "https://legislation.im/",
        "https://www.courts.im/",
        "https://www.gov.im/categories/working/employment",
    ),
}


# ─── The JurisdictionPipelineBase subclass + @dlt.source fan-out ────────


class LegalRegistryJurisdictionPipeline(JurisdictionPipelineBase):
    """CIANDLITHE cross-jurisdiction legal registry pipeline.

    Subclasses ``JurisdictionPipelineBase`` with the implied
    ``STAGE = "legal_registry"`` (the 8 BI jurisdictions are the
    per-jurisdiction discriminator; this subclass is the cross-cutting
    fan-out).

    The pipeline body is intentionally a no-op iterator today (Phase
    3.2 will populate it once the per-jurisdiction legislation crawlers
    land); the cross-cutting fan-out is exposed via
    ``bi_legal_registry_source()`` which composes the 8 per-jurisdiction
    ``<jurisdiction>_law_source`` bindings into one canonical view.
    """

    STAGE: ClassVar[str] = "legal_registry"

    def __init__(self, *, jurisdiction: str = "england", use_md: bool = True) -> None:
        if jurisdiction not in VALID_JURISDICTIONS:
            raise ValueError(
                f"LegalRegistryJurisdictionPipeline.jurisdiction={jurisdiction!r} "
                f"not in {VALID_JURISDICTIONS}"
            )
        super().__init__(jurisdiction, use_md=use_md)
        self.use_md = use_md

    def build_pipeline_resource(self):
        """No-op skeleton — Phase 3.2 will wire the per-jurisdiction fan-out."""
        return iter([])


@dlt.source(name="bi_legal_registry")
def bi_legal_registry_source(use_md: bool = True):
    """Canonical BI legal registry ``@dlt.source`` (the cross-cutting fan-out).

    Composes the 8 per-jurisdiction ``<jurisdiction>_law_source``
    bindings registered under ``dlt_sources/law/<jurisdiction>/_factory.py``
    into one canonical cross-cutting view. Each row carries the 3
    legal dimensions (statute + courts + WRC-equivalent) for the
    per-jurisdiction legislation source.

    **SKELETON**: the per-jurisdiction ``<jurisdiction>_law_source``
    bindings are themselves skeletons (see
    ``dlt_sources/law/<jurisdiction>/_factory.py``); Phase 3.2 (the
    EU/CW carve-out, Subagent Q) will populate them with real
    legislation crawler code, at which point this fan-out will yield
    the union of all 8 per-jurisdiction legislation corpora.
    """

    @dlt.resource(
        name="legal_registry",
        write_disposition="merge",
        primary_key=["natural_key"],
    )
    def legal_registry():
        sources = _bi_jurisdiction_law_sources()
        for jurisdiction, source_callable in sources.items():
            statute_source, court_source, wrc_source = BI_LEGAL_SOURCE_DEFAULTS[jurisdiction]
            try:
                for legislation_resource in source_callable(use_md=use_md).resources:
                    for row in legislation_resource():
                        yield LegalCohortRow(
                            jurisdiction=jurisdiction,
                            stage="law",
                            subject="legislation",
                            board="none",
                            qualification_level="untiered",
                            language=row.language if hasattr(row, "language") else "en",
                            statute_source=row.source_url if hasattr(row, "source_url") else statute_source,
                            court_source=court_source,
                            wrc_source=wrc_source,
                            natural_key=f"{jurisdiction}|law|legislation|statute",
                            content_sha256=row.content_sha256 if hasattr(row, "content_sha256") and row.content_sha256 else "",
                        ).model_dump()
            except (ImportError, AttributeError):
                # Per-jurisdiction binding not yet registered (Phase 3.2).
                logger.warning(
                    "bi_legal_registry.fan_out_skipped",
                    jurisdiction=jurisdiction,
                    exc_info=True,
                )

    return legal_registry


bi_legal_registry_source.__doc__ = (
    "BI cross-jurisdiction legal registry — fan-out of the 8 "
    "per-jurisdiction <jurisdiction>_law_source bindings into one "
    "canonical view. Skeleton until Phase 3.2."
)