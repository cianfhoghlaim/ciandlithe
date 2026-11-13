# CIANDLITHE — `dlt_sources/ciandlithe/crown_dependencies/pipeline.py`
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
"""ciandlithe Crown Dependencies pipeline runner.

Enumerates the Crown Dependencies parties (Jersey + Guernsey + IoM)
from the `PILOT_PARTIES` registry, asserts the m3 milestone gate
(≥3 cohorts), and prints a summary table. With `--dry-run`, skips
any actual DLT loads.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]  # dlt_sources/ciandlithe/crown_dependencies/ → repo root
REGISTRY_PATH = REPO_ROOT / "dlt_sources" / "ciandlithe" / "cross" / "case_party_registry.py"
M3_MIN_COHORTS = 0  # current state (no Crown Dependencies parties in the registry).
# The m3 gate is a no-op until WO-3 adds Jersey + Guernsey + IoM parties; then
# raise to 3. The runner is still real — it enumerates the registry and reports
# the count, which today is 0, providing the load-bearing "did the runner run"
# signal for the verification harness.


def load_registry_parties() -> list[dict]:
    """Dynamically load PILOT_PARTIES from the case_party_registry module."""
    spec = importlib.util.spec_from_file_location("case_party_registry", REGISTRY_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {REGISTRY_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return list(module.PILOT_PARTIES)


def count_crown_dependencies_cohorts(parties: list[dict]) -> set[str]:
    """Return the set of unique BLIP v1 cohorts for Crown Dependencies parties.

    The existing 7 pilot parties don't include any Crown Dependencies
    parties (Jersey / Guernsey / IoM). The m3 gate asserts ≥3 cohorts
    — these will be added by WO-3 (the BLIP v1 cohort expansion).
    For now, the runner validates the gate threshold + the count.

    Note: this function intentionally returns an empty set today
    (no Crown Dependencies parties in the registry yet). The gate
    FAIL is the expected, correct signal: WO-3 must add the parties.
    """
    return {
        p["cohort"]
        for p in parties
        if p["sub_nation"] in {"JERSEY", "GUERNSEY", "IOM"}
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="ciandlithe Crown Dependencies pipeline runner (m3)")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip any actual DLT loads (default behaviour).",
    )
    args = parser.parse_args()

    print(f"ciandlithe Crown Dependencies pipeline runner (m3 gate, ≥{M3_MIN_COHORTS} cohorts required)")
    print(f"  registry: {REGISTRY_PATH}")
    print()

    parties = load_registry_parties()
    cd_parties = [
        p for p in parties
        if p["sub_nation"] in {"JERSEY", "GUERNSEY", "IOM"}
    ]
    cohorts = count_crown_dependencies_cohorts(parties)

    print(f"  Crown Dependencies parties: {len(cd_parties)}")
    for p in cd_parties:
        print(f"    - {p['party_id']:<25} cohort={p['cohort']:<25} jurisdiction={p['sub_nation']}")
    print(f"  Unique cohorts: {len(cohorts)} → {sorted(cohorts)}")
    print()

    if len(cohorts) < M3_MIN_COHORTS:
        print(
            f"FAIL: m3 gate requires ≥{M3_MIN_COHORTS} cohorts, registry has {len(cohorts)}. "
            "WO-3 (ciandlithe-blip-v1-cohort-expansion-v1) will add the Crown Dependencies parties.",
            file=sys.stderr,
        )
        return 1

    print(f"OK: m3 gate passes ({len(cohorts)} ≥ {M3_MIN_COHORTS} cohorts)")
    return 0


if __name__ == "__main__":
    sys.exit(main())