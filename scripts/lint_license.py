#!/usr/bin/env -S uv run --python 3.12 python
# ciandlithe — `scripts/lint_license.py`
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
ciandlithe — OSINT allowlist lint.

AST-based license lint for ciandlithe. Walks
  - dlt_sources/ciandlithe/**
  - agents/ciandlithe/**
looking for @dlt.source / @dlt.resource / Google ADK agent declarations
that reference a source URL. For each URL found:
  1. verifies the URL is in
     dlt_sources/ciandlithe/common/osint_allowlist.yaml
  2. verifies the URL points at a British Isles body

The ciandlithe allowlist format uses `url:` (not the cianchosaint
`source_url:`); this linter is adapted for ciandlithe.

Exits 0 on success, 1 on any violation. Emits structlog-style errors to
stderr.
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from collections.abc import Iterable
from pathlib import Path
from urllib.parse import urlparse

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
DLT_DIR = REPO_ROOT / "dlt_sources" / "ciandlithe"
AGENTS_DIR = REPO_ROOT / "agents" / "ciandlithe"
ALLOWLIST_PATH = REPO_ROOT / "dlt_sources" / "ciandlithe" / "common" / "osint_allowlist.yaml"

# The 30+ canonical British Isles public-sector TLDs. The allowlist
# enforces that every URL on it resolves to one of these.
BRITISH_ISLES_DOMAINS: frozenset[str] = frozenset(
    {
        # United Kingdom
        "gov.uk",
        "police.uk",
        "mod.uk",
        "judiciary.uk",
        "parliament.uk",
        "nhs.uk",
        "bbc.co.uk",
        "ons.gov.uk",
        "hmrc.gov.uk",
        "caa.co.uk",
        "metoffice.gov.uk",
        "cqc.org.uk",
        "nice.org.uk",
        "nscsc.direct.gov.uk",
        "cps.gov.uk",
        "sfo.gov.uk",
        "nca.gov.uk",
        "judicialappointments.gov.uk",
        # Crown Dependencies
        "gov.je",
        "gov.gg",
        "gov.im",
        # Republic of Ireland
        "gov.ie",
        "garda.ie",
        "defenceforces.ie",
        "military.ie",
        "dfa.ie",
        "hse.ie",
        "courts.ie",
        "irishstatutebook.ie",
        "citizensinformation.ie",
        "revenue.ie",
        "cso.ie",
        "met.ie",
        "rte.ie",
        "hpsc.ie",
        "wrc.ie",
        "ihrec.ie",
        "medicalcouncil.ie",
        "nmbi.ie",
        "thepsi.ie",
        "lawsociety.ie",
        "lawsoc-ni.org",
        "rcsi.ie",
        "dentist.ie",
        "pharmacyregulation.gov.ie",
        "scri.ie",
        "vista.ie",
        "irishexaminer.ie",
        "irishtimes.com",
        "thejournal.ie",
        "agriland.ie",
        "thetimes.co.uk",
        "telegraph.co.uk",
        "tribunals.ie",
        "hrca.ie",
        "coru.ie",
        "socialworkireland.ie",
        "teachingcouncil.ie",
        "workplacerelations.ie",
        "injuries.ie",
        "lawreform.ie",
        # Scotland
        "scotcourts.gov.uk",
        "nhsinform.scot",
        "gov.scot",
        "nhs.scot",
        "nhslothian.scot",
        "ggc.scot.nhs.uk",
        "scot.nhs.uk",
        "police.scot",
        "scotland.police.uk",
        "sfc.ac.uk",
        "hes.scot",
        "audit-scotland.gov.uk",
        "spc.scot",
        "scottishcabinetsecretary.gov.scot",
        # Wales
        "gov.wales",
        "phw.nhs.wales",
        "senedd.wales",
        "wales.nhs.uk",
        "wru.wales",
        "cyfoethnasaf.cymru",
        "senedd.cymru",
        # GMC + royal colleges + regulators
        "gmc-uk.org",
        "gmc-uk-education.org",
        "gdc-uk.org",
        "pharmacyregulation.org",
        "hcpc-uk.org",
        "nmc-uk.org",
        "socialworkengland.org",
        "scie.org.uk",
        "nice.org.uk",
        "ahp.org.uk",
        "rcpch.ac.uk",
        "rcplondon.ac.uk",
        "rcsed.ac.uk",
        "rcpsych.ac.uk",
        "rcgp.org.uk",
        "bma.org.uk",
    }
)


def load_allowlist() -> set[str]:
    """Return the set of allowlisted source URLs.

    The ciandlithe allowlist uses the simple `url:` key (one URL per list
    item, optionally followed by indented key/value metadata), unlike
    cianchosaint's `entries: - source_url:` wrapper. This loader handles
    BOTH formats for robustness.
    """
    if not ALLOWLIST_PATH.exists():
        return set()
    raw = ALLOWLIST_PATH.read_text(encoding="utf-8")
    try:
        data = yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        # Fallback: regex-extract every `url: <value>` line
        urls = set()
        for match in re.finditer(r"^\s*-?\s*url:\s*['\"]?([^'\"\s#]+)", raw, re.MULTILINE):
            urls.add(match.group(1).rstrip("'\","))
        return urls
    if isinstance(data, dict) and "entries" in data:
        # cianchosaint format
        return {
            entry.get("source_url") or entry.get("url")
            for entry in data["entries"]
            if isinstance(entry, dict)
        }
    # ciandlithe format: top-level list of dicts
    urls: set[str] = set()
    for entry in data if isinstance(data, list) else []:
        if isinstance(entry, dict):
            u = entry.get("url")
            if u:
                urls.add(u)
    return urls


def is_british_isles_url(url: str) -> bool:
    """Return True iff the URL's host is a British Isles public-sector body."""
    host = (urlparse(url).hostname or "").lower()
    if not host:
        return False
    for domain in BRITISH_ISLES_DOMAINS:
        if host == domain or host.endswith(f".{domain}"):
            return True
    return False


def extract_urls_from_ast(tree: ast.AST) -> Iterable[tuple[str, int]]:
    """Yield (url, lineno) pairs for every HTTP(S) string constant in the tree."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            value = node.value
            if value.startswith(("http://", "https://")):
                yield value, node.lineno


def has_dlt_or_adk_decorator(tree: ast.AST) -> bool:
    """Return True iff the module declares a @dlt.source / @dlt.resource / ADK agent."""
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Attribute):
                    if decorator.attr in {"source", "resource"}:
                        return True
                if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                    if decorator.func.attr in {"source", "resource"}:
                        return True
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in {"root_agent", "LlmAgent", "Agent"}:
                return True
    return False


def walk_python_files(roots: Iterable[Path]) -> Iterable[Path]:
    """Yield every .py file under each existing root directory."""
    for root in roots:
        if not root.exists():
            continue
        yield from root.rglob("*.py")


def lint_file(py_path: Path, allowlist: set[str]) -> list[str]:
    """Return a list of violation strings for the given Python file."""
    try:
        tree = ast.parse(py_path.read_text(encoding="utf-8"))
    except SyntaxError as exc:
        return [f"{py_path}:{exc.lineno}: syntax error: {exc.msg}"]

    if not has_dlt_or_adk_decorator(tree):
        return []

    violations: list[str] = []
    # Pre-compute the set of normalised allowlist URLs (strip trailing
    # slash) so the prefix match handles `https://hse.ie` vs
    # `https://hse.ie/about/` consistently.
    normalised_allowlist = {u.rstrip("/") for u in allowlist}

    for url, lineno in extract_urls_from_ast(tree):
        normalised_url = url.rstrip("/")
        if not any(
            normalised_url == entry or normalised_url.startswith(entry + "/")
            for entry in normalised_allowlist
        ):
            violations.append(
                f"{py_path}:{lineno}: URL not in OSINT allowlist: {url}"
            )
        if not is_british_isles_url(url):
            violations.append(
                f"{py_path}:{lineno}: URL is not a British Isles body: {url}"
            )
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="ciandlithe OSINT allowlist lint")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 on any violation (default behaviour; flag is explicit).",
    )
    args = parser.parse_args()

    if not ALLOWLIST_PATH.exists():
        print(
            f"FAIL: OSINT allowlist not found at {ALLOWLIST_PATH}; "
            "create it before running the lint",
            file=sys.stderr,
        )
        return 1

    allowlist = load_allowlist()
    if not allowlist:
        print(
            f"FAIL: OSINT allowlist at {ALLOWLIST_PATH} contains 0 entries; "
            "populate it before running the lint",
            file=sys.stderr,
        )
        return 1

    all_violations: list[str] = []
    file_count = 0
    for py_path in walk_python_files([DLT_DIR, AGENTS_DIR]):
        file_count += 1
        all_violations.extend(lint_file(py_path, allowlist))

    if all_violations:
        for violation in all_violations:
            print(f"FAIL: {violation}", file=sys.stderr)
        print(
            f"\n{len(all_violations)} violation(s) across {file_count} file(s); "
            "see ciandlithe-toolchain spec § Requirement: The 3 lint scripts",
            file=sys.stderr,
        )
        return 1

    print(
        f"OK: {file_count} file(s) scanned; "
        f"{len(allowlist)} allowlist entries; 0 violations"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())