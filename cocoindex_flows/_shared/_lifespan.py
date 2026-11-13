# CIANDLITHE — `cocoindex_flows/_shared/_lifespan.py`
#
# Re-export shim for backwards compatibility (the canonical convention is
# `from ._shared import shared_lifespan, EMBEDDER, LANCE_DB`).
#
# Per the openspec/changes/ciandlithe-repo-foundation-v1/
# specs/ciandlithe-pipeline/spec.md, Requirement: R1 — `from ..._shared
# ._lifespan import shared_lifespan`.
#
# Licence: BUSL-1.1 v2 CIANDLITHE edition (per LICENSE.md)
#
# Per LICENSE.md §3.8 + §5.2:
#   - osint_ceiling_enforced = True (always)
#   - analyst_review_required = True (always)
#   - PoI clause: non-public individuals are never named
"""Re-export shim for the canonical CocoIndex lifespan + ContextKeys.

Mirrors the cianfhoghlaim convention (per the wholesale-copy lineage).
"""
from __future__ import annotations

from . import (  # noqa: F401  (re-export)
    COCOINDEX_AVAILABLE,
    DEFAULT_EMBED_MODEL,
    DEFAULT_LANCE_DIR,
    EMBEDDER,
    LANCE_DB,
    RESOLVED_FILE_REGISTRY,
    shared_lifespan,
)

__all__ = [
    "COCOINDEX_AVAILABLE",
    "DEFAULT_EMBED_MODEL",
    "DEFAULT_LANCE_DIR",
    "EMBEDDER",
    "LANCE_DB",
    "RESOLVED_FILE_REGISTRY",
    "shared_lifespan",
]