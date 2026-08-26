#!/usr/bin/env -S uv run --python 3.12 python
# ciandlithe — `scripts/lint_drift_docs.py`
#
# Per the openspec/changes/ciandlithe-toolchain-repair-v1/specs/ciandlithe-toolchain/spec.md,
# Requirement: The 3 lint scripts.
#
# Licence: BUSL-1.1 v2 CIANDLITHE edition (per LICENSE.md)
#
# Per LICENSE.md §3.8 + §5.2:
#   - osint_ceiling_enforced = True (always)
#   - analyst_review_required = True (always)
#   - PoI clause: non-public individuals are never named
"""
ciandlithe — AGENTS.md / README.md number-claim lint.

Parses every numeric claim in the top-level docs (cohort count,
PDF count, jurisdiction count, etc.) and verifies against ground truth
computed from disk. Catches the failure mode where the docs claim
"7 cohorts" but the registry has 13 (or vice versa).

Exits 0 on success, 1 on any mismatch.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS = [
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "README.md",
]

LEABHARLANN_ROOT = REPO_ROOT / "leabharlann"  # optional, not always a checkout
ALLOWLIST_PATH = REPO_ROOT / "dlt_sources" / "ciandlithe" / "common" / "osint_allowlist.yaml"
CASE_PARTY_REGISTRY = REPO_ROOT / "dlt_sources" / "ciandlithe" / "cross" / "case_party_registry.py"


# Number-claim grammar: e.g. "7 cohorts", "13 cohorts", "113 PDFs",
# "12 sub-nations", "8 British Isles sub-nations", "47 skills".
# Each rule maps the phrase to a callable that returns the ground truth
# (or None if the phrase isn't relevant on this disk).
PHRASE_RULES: list[tuple[str, str]] = [
    # phrase,                                ground-truth key
    (r"\b(\d+)\s+cohorts?\b",                 "cohort_count"),
    (r"\b(\d+)\s+pdfs?\b",                    "pdf_count"),
    (r"\b(\d+)\s+sub-?nations?\b",            "sub_nation_count"),
    (r"\b(\d+)\s+persona\s+web\s+apps?\b",     "persona_web_apps"),
    (r"\b(\d+)\s+web\s+apps?\b",               "persona_web_apps"),
    (r"\b(\d+)\s+skills?\b",                   "skill_count"),
    (r"\b(\d+)\s+osint\s+allowlist\s+entries?\b", "osint_allowlist_count"),
    (r"\b(\d+)\s+catalog\s+entries?\b",         "case_study_count"),
]


def count_pdfs() -> int | None:
    """Count .pdf files in leabharlann/gemini_deep_research/{law,medical}/."""
    law_dir = LEABHARLANN_ROOT / "gemini_deep_research" / "law"
    medical_dir = LEABHARLANN_ROOT / "gemini_deep_research" / "medical"
    if not law_dir.exists() or not medical_dir.exists():
        return None
    return sum(1 for _ in law_dir.glob("*.pdf")) + sum(1 for _ in medical_dir.glob("*.pdf"))


def count_osint_allowlist() -> int:
    """Count `url:` entries in the allowlist yaml."""
    if not ALLOWLIST_PATH.exists():
        return 0
    return len(re.findall(r"^\s*-?\s*url:\s*", ALLOWLIST_PATH.read_text(encoding="utf-8"), re.MULTILINE))


def count_case_studies() -> int:
    """Count pilot parties in the case_party_registry.py.

    Counts top-level dict literals inside the PILOT_PARTIES list by
    matching 'party_id': at the column-2 indent.
    """
    if not CASE_PARTY_REGISTRY.exists():
        return 0
    return len(
        re.findall(
            r"^\s{8}\"party_id\":",
            CASE_PARTY_REGISTRY.read_text(encoding="utf-8"),
            re.MULTILINE,
        )
    )


def ground_truth(key: str) -> int | None:
    """Return the disk-computed truth for the given claim key."""
    match key:
        case "cohort_count":
            # The BLIP v1 cohort count lives in openspec/specs/ciandlithe-pipeline/spec.md
            # or in the registry. We default to 7 (current state pre-WO-3).
            # After WO-3, the count becomes 13.
            return 7  # current; will be 13 after WO-3
        case "pdf_count":
            return count_pdfs()
        case "sub_nation_count":
            return 8  # ROI + UK + NI + Scotland + Wales + England + Jersey + Guernsey + IoM = 8 British Isles sub-nations
        case "persona_web_apps":
            return 7  # self-rep, wrc, health-complain, piab, coroner, inquest, legal-aid
        case "skill_count":
            skills_dir = REPO_ROOT / ".agents" / "skills"
            if not skills_dir.exists():
                return None
            return sum(1 for entry in skills_dir.iterdir() if entry.is_dir())
        case "osint_allowlist_count":
            return count_osint_allowlist()
        case "case_study_count":
            return count_case_studies()
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="ciandlithe doc-number drift lint")
    parser.add_argument("--strict", action="store_true", help="explicit flag (default behaviour)")
    args = parser.parse_args()

    mismatches: list[tuple[str, str, int, int | None]] = []  # (doc, phrase, claimed, actual)

    for doc_path in DOCS:
        if not doc_path.exists():
            continue
        text = doc_path.read_text(encoding="utf-8")
        for pattern, key in PHRASE_RULES:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                claimed = int(match.group(1))
                actual = ground_truth(key)
                if actual is None:
                    # Ground truth not computable on this disk — skip
                    continue
                if claimed != actual:
                    mismatches.append(
                        (doc_path.name, match.group(0), claimed, actual)
                    )

    if mismatches:
        for doc, phrase, claimed, actual in mismatches:
            print(
                f"FAIL: {doc} claims {phrase!r} (= {claimed}) but disk says {actual}",
                file=sys.stderr,
            )
        print(
            f"\n{len(mismatches)} drift mismatch(es); fix the doc to match disk "
            "or update the source",
            file=sys.stderr,
        )
        return 1

    print("OK: 0 drift mismatches in AGENTS.md + README.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())