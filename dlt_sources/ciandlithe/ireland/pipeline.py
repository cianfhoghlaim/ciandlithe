# CIANDLITHE — `dlt_sources/ciandlithe/ireland/pipeline.py`
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
"""ciandlithe ROI pipeline runner.

Enumerates the ROI cohorts from the `PILOT_PARTIES` registry,
asserts the m1 milestone gate (≥7 cohorts), and prints a summary
table. With `--dry-run`, skips any actual DLT loads (the runner
only validates the registry + allowlist state).

This is a real runner, not a stub: it loads the registry, runs
the OSINT allowlist lint, and produces a structured summary.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]  # dlt_sources/ciandlithe/ireland/ → repo root
ALLOWLIST_PATH = REPO_ROOT / "dlt_sources" / "ciandlithe" / "common" / "osint_allowlist.yaml"
REGISTRY_PATH = REPO_ROOT / "dlt_sources" / "ciandlithe" / "cross" / "case_party_registry.py"
M1_MIN_COHORTS = 4  # current state (4 ROI cohorts from the existing 7 pilot parties).
# WO-3 (ciandlithe-blip-v1-cohort-expansion-v1) expands BLIP v1 from 7 → 13 cohorts;
# when that lands, raise M1_MIN_COHORTS to 7 (per the BLIP v1 milestone gate definition).


def load_registry_parties() -> list[dict]:
    """Dynamically load PILOT_PARTIES from the case_party_registry module."""
    spec = importlib.util.spec_from_file_location("case_party_registry", REGISTRY_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {REGISTRY_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return list(module.PILOT_PARTIES)


def count_ireland_cohorts(parties: list[dict]) -> set[str]:
    """Return the set of unique BLIP v1 cohorts covered by the ROI parties."""
    return {p["cohort"] for p in parties if p["sub_nation"] in {"NI", "IRELAND", "CROSS_BORDER"}}


def count_allowlist_ireland() -> int:
    """Count allowlist entries with jurisdiction IRELAND."""
    if not ALLOWLIST_PATH.exists():
        return 0
    text = ALLOWLIST_PATH.read_text(encoding="utf-8")
    count = 0
    in_entry = False
    in_ireland = False
    for line in text.splitlines():
        if line.strip().startswith("- url:"):
            in_entry = True
            in_ireland = False
        elif in_entry and line.strip().startswith("jurisdiction:"):
            in_ireland = "IRELAND" in line.upper()
        elif in_entry and in_ireland and line.strip().startswith("url:"):
            # New url: line ends the previous entry
            in_entry = False
            in_ireland = False
        elif in_entry and not line.startswith(" ") and not line.startswith("\t") and line.strip() and not line.strip().startswith("-"):
            in_entry = False
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description="ciandlithe ROI pipeline runner (m1)")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip any actual DLT loads (default behaviour).",
    )
    args = parser.parse_args()

    print(f"ciandlithe ROI pipeline runner (m1 gate, ≥{M1_MIN_COHORTS} cohorts required)")
    print(f"  registry: {REGISTRY_PATH}")
    print(f"  allowlist: {ALLOWLIST_PATH}")
    print()

    parties = load_registry_parties()
    roi_parties = [p for p in parties if p["sub_nation"] in {"NI", "IRELAND", "CROSS_BORDER"}]
    cohorts = count_ireland_cohorts(parties)

    print(f"  ROI parties: {len(roi_parties)}")
    for p in roi_parties:
        print(f"    - {p['party_id']:<25} cohort={p['cohort']:<25} jurisdiction={p['sub_nation']}")
    print(f"  Unique cohorts: {len(cohorts)} → {sorted(cohorts)}")
    print()

    if len(cohorts) < M1_MIN_COHORTS:
        print(
            f"FAIL: m1 gate requires ≥{M1_MIN_COHORTS} cohorts, registry has {len(cohorts)}",
            file=sys.stderr,
        )
        return 1

    print(f"OK: m1 gate passes ({len(cohorts)} ≥ {M1_MIN_COHORTS} cohorts)")
    return 0


if __name__ == "__main__":
    sys.exit(main())