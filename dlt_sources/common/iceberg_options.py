# CIANDLITHE wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
# CIANDLITHE wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/ciandlithe-repo-bootstrap-v2/specs/ciandlithe-bootstrap-v2/spec.md).
# Migrated to ciandlithe: 2026-08-23
# Licence: BUSL-1.1 v2 CIANDLITHE edition (per LICENSE.md)
#
# This file is part of the ciandlithe DLT common helper layer. The
# namespace rename from cianfhoghlaim -> ciandlithe has NOT been
# applied to the body of this file (yet); the wholesale-copy is
# intentionally verbatim so that the diff against the upstream
# cianfhoghlaim/cianfhoghlaim commit is preserved for traceability.
# Subsequent openspec changes will apply namespace refactors
# incrementally as the per-domain pipeline bases (BIPP v1 / BIDP v1 /
# BIIP v1) are constructed.
#
# Per the openspec/changes/ciandlithe-repo-bootstrap-v2/proposal.md:
# "Each migrated file SHALL start with a comment block stating
# `Original: cianfhoghlaim/cianfhoghlaim @ <commit-sha>` and
# `Migrated to ciandlithe: <date>` and `Licence: BUSL-1.1 v2 CIANDLITHE edition (per LICENSE.md)`"
#

"""Iceberg write path helpers.

Per the 2026-08-07-biep-v3-hardening-v1 change.

The canonical destination factory at
dlt/common/destinations_ciandlithe_compat_cianfhoghlaim.py currently exposes only
DuckLake + plain DuckDB writes. This module adds the parallel
Iceberg write path (for tiering to a hot/warm/cold strategy).
"""
from __future__ import annotations

from typing import Any

import dlt
import dlt_sources


def build_iceberg_local_destination(
    namespace: str = "cianfhoghlaim",
    catalog_uri: str = "http://localhost:8181",
    warehouse: str = "s3://garage/iceberg/",
) -> Any:
    """Build the canonical local Iceberg destination via dlt."""
    return dlt.destinations.iceberg(
        credentials={
            "uri": catalog_uri,
            "warehouse": warehouse,
            "namespace": namespace,
        },
    )


__all__ = ["build_iceberg_local_destination"]
