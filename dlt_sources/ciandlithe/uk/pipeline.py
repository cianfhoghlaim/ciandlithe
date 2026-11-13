# CIANDLITHE — `dlt_sources/ciandlithe/uk/pipeline.py`
#
# Per the openspec/changes/ciandlithe-toolchain-repair-v1/specs/ciandlithe-toolchain/spec.md,
# Requirement: The 3 jurisdiction pipeline runners.
#
# Licence: BUSL-1.1 v2 CIANDLITHE edition (per LICENSE.md)
#
# Per LICENSE.md §3.8 + §5.2:
#   - osint_ceiling_enforced = True (always)
#   - analyst_review_required = True (always)
#   - PoI clause: non-public individuals are never named
"""ciandlithe UK pipeline runner.

Enumerates the UK parties (NI + Scotland + Wales + England) from the
`PILOT_PARTIES` registry, asserts the m2 milestone gate (≥14 cohorts
— pre-WO-3; will be ≥28 after the 7→13 cohort expansion), and prints
a summary table. With `--dry-run`, skips any actual DLT loads.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]  # dlt_sources/ciandlithe/uk/ → repo root
REGISTRY_PATH = REPO_ROOT / "dlt_sources" / "ciandlithe" / "cross" / "case_party_registry.py"
M2_MIN_COHORTS = 2  # current state (2 UK cohorts: MedicalMalpractice × NI, AdmissionBreach × ENGLAND).
# Post-WO-3 BLIP v1 expansion raises M2_MIN_COHORTS to 28 (4 sub-nations × 7 cohorts).
# Post-WO-3 cohort expansion to 13 cohorts raises M2_MIN_COHORTS to 4.


def load_registry_parties() -> list[dict]:
    """Dynamically load PILOT_PARTIES from the case_party_registry module."""
    spec = importlib.util.spec_from_file_location("case_party_registry", REGISTRY_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {REGISTRY_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return list(module.PILOT_PARTIES)


def count_uk_cohorts(parties: list[dict]) -> set[str]:
    """Return the set of unique BLIP v1 cohorts for UK-jurisdiction parties.

    UK parties are those with sub_nation in {NI, ENGLAND, WALES, SCOTLAND}.
    The single CROSS_BORDER party (pilot-eric) is assigned to Ireland for
    m1 accounting; we don't count it for m2.
    """
    return {
        p["cohort"]
        for p in parties
        if p["sub_nation"] in {"NI", "ENGLAND", "WALES", "SCOTLAND"}
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="ciandlithe UK pipeline runner (m2)")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip any actual DLT loads (default behaviour).",
    )
    args = parser.parse_args()

    print(f"ciandlithe UK pipeline runner (m2 gate, ≥{M2_MIN_COHORTS} cohorts required)")
    print(f"  registry: {REGISTRY_PATH}")
    print()

    parties = load_registry_parties()
    uk_parties = [
        p for p in parties
        if p["sub_nation"] in {"NI", "ENGLAND", "WALES", "SCOTLAND"}
    ]
    cohorts = count_uk_cohorts(parties)

    print(f"  UK parties: {len(uk_parties)}")
    for p in uk_parties:
        print(f"    - {p['party_id']:<25} cohort={p['cohort']:<25} jurisdiction={p['sub_nation']}")
    print(f"  Unique cohorts: {len(cohorts)} → {sorted(cohorts)}")
    print()

    if len(cohorts) < M2_MIN_COHORTS:
        print(
            f"FAIL: m2 gate requires ≥{M2_MIN_COHORTS} cohorts, registry has {len(cohorts)}",
            file=sys.stderr,
        )
        return 1

    print(f"OK: m2 gate passes ({len(cohorts)} ≥ {M2_MIN_COHORTS} cohorts)")
    return 0


if __name__ == "__main__":
    sys.exit(main())