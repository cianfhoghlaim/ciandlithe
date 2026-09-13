# CIANDLITHE — `cocoindex_flows/_shared/__init__.py`
#
# Per the openspec/changes/ciandlithe-repo-foundation-v1/
# specs/ciandlithe-pipeline/spec.md, Requirement: The R1–R4
# CocoIndex v1 contract.
#
# The shared lifespan + ContextKeys for ciandlithe CocoIndex flows.
# Wholesale-copied from cianfhoghlaim/cocoindex_flows/_shared/_lifespan.py
# pattern (see openspec/changes/cianchosaint-repo-bootstrap-v2 for the
# wholesale-copy lineage).
#
# Licence: BUSL-1.1 v2 CIANDLITHE edition (per LICENSE.md)
#
# Per LICENSE.md §3.8 + §5.2:
#   - osint_ceiling_enforced = True (always)
#   - analyst_review_required = True (always)
#   - PoI clause: non-public individuals are never named
"""Shared CocoIndex v1 lifespan + ContextKeys for ciandlithe.

R1 contract: every CocoIndex flow imports `shared_lifespan, EMBEDDER, LANCE_DB`
   from `._lifespan`.
R2 contract: every CocoIndex flow declares `app = coco.App(coco.AppConfig(name=...))`
   at module scope (callers then pass `app_main, **kwargs`).
R3 contract: `lancedb.mount_table_target(LANCE_DB, ...)` for the vector store.
R4 contract: `target.declare_vector_index(column="embedding")` for the HNSW index
   + `create_fts_index` for hybrid RRF search.

CocoIndex is optional — degrade gracefully if not installed (same pattern
as the langfuse_prompt_resolver graceful fallback).
"""

from __future__ import annotations

import logging
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

logger = logging.getLogger(__name__)


try:
    from cocoindex.connectors import lancedb  # type: ignore[import-not-found]
    import cocoindex as coco  # type: ignore[import-not-found]
    from cocoindex.ops.sentence_transformers import (  # type: ignore[import-not-found]
        SentenceTransformerEmbedder,
    )
    COCOINDEX_AVAILABLE = True
except ImportError as exc:
    logger.warning("cocoindex_v1_not_available: %s", exc)
    COCOINDEX_AVAILABLE = False
    coco = None  # type: ignore[assignment]
    lancedb = None  # type: ignore[assignment]
    SentenceTransformerEmbedder = None  # type: ignore[assignment]


# The canonical 3 ContextKeys. A CocoIndex flow references these by name.
EMBEDDER = coco.ContextKey[Any]("embedder", detect_change=True) if COCOINDEX_AVAILABLE else "embedder"
LANCE_DB = coco.ContextKey[Any]("lance_db", detect_change=True) if COCOINDEX_AVAILABLE else "lance_db"
RESOLVED_FILE_REGISTRY = coco.ContextKey[Any]("resolved_file_registry", detect_change=True) if COCOINDEX_AVAILABLE else "resolved_file_registry"


# The canonical BAAI/bge-m3 1024-d embedder (per the cianfhoghlaim convention;
# multilingual, supports English + Irish + Scots + Welsh + French).
DEFAULT_EMBED_MODEL = "BAAI/bge-m3"


# Where the LanceDB store sits on disk (per-flow; defaults to a project-local
# `./.lance` directory).
DEFAULT_LANCE_DIR = os.environ.get("CIANDLITHE_LANCE_DIR", "./.lance")


@asynccontextmanager
async def shared_lifespan(builder: Any) -> AsyncIterator[None]:
    """R1 contract: the canonical CocoIndex lifespan.

    Provides the shared embedder (BGE-M3 1024-d) + the LanceDB connection.
    Per-flow callers receive these via `coco.use_context(EMBEDDER)` /
    `coco.use_context(LANCE_DB)`.

    If CocoIndex is not installed, the yield still proceeds (the per-flow
    code paths that do not touch CocoIndex continue to work; the flows that
    DO touch CocoIndex raise a clear ImportError at the call site, not at
    lifespan setup).
    """
    if not COCOINDEX_AVAILABLE:
        logger.warning("cocoindex_unavailable_skipping_shared_lifespan")
        yield
        return

    # The local embedder (instantiated once, shared across flows)
    embedder = SentenceTransformerEmbedder(model=DEFAULT_EMBED_MODEL)
    builder.provide(EMBEDDER, embedder)

    # The local LanceDB connection (instantiated once, shared across flows)
    import lancedb  # the second time
    os.makedirs(DEFAULT_LANCE_DIR, exist_ok=True)
    lancedb_conn = await lancedb.connect_async(f"{DEFAULT_LANCE_DIR}/ciandlithe.lance")
    builder.provide(LANCE_DB, lancedb_conn)

    yield


__all__ = [
    "COCOINDEX_AVAILABLE",
    "DEFAULT_EMBED_MODEL",
    "DEFAULT_LANCE_DIR",
    "EMBEDDER",
    "LANCE_DB",
    "RESOLVED_FILE_REGISTRY",
    "shared_lifespan",
]