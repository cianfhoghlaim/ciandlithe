# CIANDLITHE wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/ciandlithe-repo-bootstrap-v2/specs/ciandlithe-bootstrap-v2/spec.md).
# Migrated to ciandlithe: 2026-08-23
# Licence: BUSL-1.1 v2 CIANDLITHE edition (per LICENSE.md)
#
# This file is part of the ciandlithe DLT cross-jurisdiction framework.
# It implements the 5-stage pipeline pattern (Ingestion -> Extraction ->
# Embedding -> ibis logging -> Analytics) wholesale-copied from the
# Cianfhoghlaim BIEP v3 implementation and refactored for the
# ciandlithe BIPP v1 / BIDP v1 / BIIP v1 verticals.
#
# The biep_4_path_ensemble_runner.py was renamed to 5_stage_runner.py
# (the BIEP v3 "4-path ensemble" became the ciandlithe "5-stage
# pipeline").
# The biep_4_stage_registry.py was renamed to 5_stage_registry.py
# (same reasoning).
# The jurisdiction_pipeline_base.py is wholesale-copied verbatim
# (the JurisdictionPipelineBase subclass pattern is generic).

"""British Isles subject registry (BIEP v3 cross-cutting).

Per the 2026-07-27-biep-v3-canonical-registry-v1 change.
"""
from dlt_sources.british_isles._cross.registry_api import (
    SubjectRegistryRow,
    query_by_jurisdiction,
    query_by_concept,
    query_by_stage,
    query_cross_jurisdiction_bridges,
    insert_subject,
)

__all__ = [
    "SubjectRegistryRow",
    "query_by_jurisdiction",
    "query_by_concept",
    "query_by_stage",
    "query_cross_jurisdiction_bridges",
    "insert_subject",
]