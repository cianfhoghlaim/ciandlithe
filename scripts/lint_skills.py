#!/usr/bin/env -S uv run --python 3.12 python
# ciandlithe — `scripts/lint_skills.py`
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
ciandlithe — agent skill frontmatter lint.

Validates every `.agents/skills/*/SKILL.md` frontmatter has `name` (≤64
chars) + `description` (≤1024 chars). Exits 1 on any violation.

Per the .agents/skills/INDEXING_AND_COGNITION.md convention (wholesale-
copied from cianfhoghlaim): every agent skill MUST declare its name
and a one-line description; descriptions > 1024 chars are considered
broken (the description is what auto-dispatches the skill to an
agent invocation, and very long descriptions fail to match).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"

NAME_MAX = 64
DESCRIPTION_MAX = 1024

# Frontmatter is the YAML between the first pair of `---` lines.
FRONTMATTER_RE = re.compile(
    r"^---\s*\n(?P<fm>.*?)\n---\s*(?:\n|$)", re.DOTALL
)
FIELD_RE = re.compile(r"^(\w+):\s*(.*?)\s*$", re.MULTILINE)


def parse_frontmatter(text: str) -> dict[str, str]:
    """Parse a minimal YAML frontmatter without depending on pyyaml.

    Handles:
    - top-level `key: value` lines
    - multi-line values (continuation lines indented under the key)
    - quoted values
    - list values (`- item` under a key, joined by spaces)
    """
    match = FRONTMATTER_RE.search(text)
    if not match:
        return {}
    block = match.group("fm")
    fields: dict[str, str] = {}
    current_key: str | None = None
    current_value: list[str] = []

    def flush() -> None:
        nonlocal current_key, current_value
        if current_key is not None and current_value:
            # Join multi-line values with spaces; strip list markers
            joined = " ".join(current_value)
            joined = joined.replace("\n- ", " ").replace("\n  - ", " ")
            fields[current_key] = joined.strip()
        current_key = None
        current_value = []

    for line in block.splitlines():
        raw = line.rstrip()
        if not raw or raw.lstrip().startswith("#"):
            continue
        # Top-level `key: value` line
        field_match = re.match(r"^(\w[\w-]*):\s*(.*?)\s*$", raw)
        if field_match and not raw.startswith(" ") and not raw.startswith("\t"):
            flush()
            current_key = field_match.group(1)
            initial_value = field_match.group(2)
            if (initial_value.startswith('"') and initial_value.endswith('"')) or (
                initial_value.startswith("'") and initial_value.endswith("'")
            ):
                initial_value = initial_value[1:-1]
            current_value = [initial_value] if initial_value else []
            continue
        # Continuation of a multi-line value
        if current_key is not None:
            current_value.append(raw.strip())
    flush()
    return fields


def main() -> int:
    parser = argparse.ArgumentParser(description="ciandlithe agent skill frontmatter lint")
    parser.add_argument("--strict", action="store_true", help="explicit flag (default behaviour)")
    args = parser.parse_args()

    if not SKILLS_DIR.exists():
        print(f"FAIL: skills dir not found at {SKILLS_DIR}", file=sys.stderr)
        return 1

    violations: list[str] = []
    file_count = 0
    for skill_md in SKILLS_DIR.rglob("SKILL.md"):
        file_count += 1
        try:
            text = skill_md.read_text(encoding="utf-8")
        except OSError as exc:
            violations.append(f"{skill_md}: read error: {exc}")
            continue

        fm = parse_frontmatter(text)
        name = fm.get("name", "").strip()
        description = fm.get("description", "").strip()

        if not name:
            violations.append(f"{skill_md}: missing `name` in frontmatter")
        elif len(name) > NAME_MAX:
            violations.append(
                f"{skill_md}: `name` is {len(name)} chars (max {NAME_MAX})"
            )
        if not description:
            violations.append(f"{skill_md}: missing `description` in frontmatter")
        elif len(description) > DESCRIPTION_MAX:
            violations.append(
                f"{skill_md}: `description` is {len(description)} chars (max {DESCRIPTION_MAX})"
            )

    if violations:
        for violation in violations:
            print(f"FAIL: {violation}", file=sys.stderr)
        print(
            f"\n{len(violations)} violation(s) across {file_count} SKILL.md file(s)",
            file=sys.stderr,
        )
        return 1

    print(f"OK: {file_count} SKILL.md file(s) scanned; 0 frontmatter violations")
    return 0


if __name__ == "__main__":
    sys.exit(main())