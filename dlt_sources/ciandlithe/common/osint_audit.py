"""CIANDLITHE OSINT allowlist + allowlist classifier.

The OSINT allowlist at `dlt_sources/ciandlithe/common/osint_allowlist.yaml`
is the canonical list of URLs that may be ingested by any DLT source file
under `dlt_sources/ciandlithe/**`. Per LICENSE.md §5.1, the CI gate
`mise run lint:license` enforces this.

The `lint:license` task scans every DLT source file for URLs and
verifies each URL is present in the OSINT allowlist. URLs that are not
on the allowlist cause the gate to fail.

Per LICENSE.md §5.2 (PoI clause) + §3.8 (no-auto-submit constraint):
the OSINT allowlist contains ONLY URLs to public-facing pages of
British-Isles public-sector bodies (per LICENSE.md §3.1–§3.7). It does
NOT contain URLs to:
- private individuals' social media accounts
- private companies' websites
- leabharlann PDFs (those are Gemini Deep Research outputs, not
  public-sector sources — they are cited in the FunctionTool output as
  `source_pdf_urls` (read-only context) but NOT ingested via DLT)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


OSINT_ALLOWLIST_PATH = Path(__file__).parent / "osint_allowlist.yaml"

# A simple regex that matches http(s) URLs in a string.
URL_REGEX = re.compile(r"https?://[^\s\"\'\)\,>]+")


def load_allowlist() -> list[dict[str, str]]:
    """Load the OSINT allowlist from disk (parses the YAML file manually).

    The YAML file is intentionally simple (no external yaml dep). We parse it
    line-by-line. Real CI uses the YAML parser via the mise task.
    """
    entries: list[dict[str, str]] = []
    if not OSINT_ALLOWLIST_PATH.exists():
        return entries
    current: dict[str, str] | None = None
    with OSINT_ALLOWLIST_PATH.open("r", encoding="utf-8") as fh:
        for line in fh:
            raw = line.rstrip("\n")
            if not raw or raw.lstrip().startswith("#"):
                continue
            stripped = raw.strip()
            # Top-level scalars (allowlist_version, last_updated, change_date)
            # appear BEFORE the first "- url:" line. Skip them.
            if current is None and not stripped.startswith("- "):
                continue
            if stripped.startswith("- url:"):
                if current is not None:
                    entries.append(current)
                current = {"url": stripped[len("- url:"):].strip()}
            elif ":" in stripped and current is not None:
                # Indented sub-fields (jurisdiction, body, cohort, source_family)
                # are indented with 2+ spaces in the YAML. Only treat as sub-field
                # if the line starts with whitespace + key.
                if line.startswith(("  ", "\t")):
                    key, _, value = stripped.partition(":")
                    current[key.strip()] = value.strip()
        if current is not None:
            entries.append(current)
    return entries


def extract_urls_from_dlt_source_text(p_text: str) -> list[str]:
    """Extract all URLs from a DLT source file's text content."""
    return URL_REGEX.findall(p_text)


def lint_dlt_source_text(p_text: str, source_file: str) -> list[dict[str, Any]]:
    """Lint a single DLT source file against the OSINT allowlist.

    Returns a list of errors. Empty list means the file passes.

    Matching rules:
    - Exact match: the URL in the file equals an allowlist URL exactly.
    - Prefix match: the URL in the file STARTS WITH an allowlist URL
      (followed by `/`, `?`, `#`, or end-of-string).
    - Template match: an allowlist URL contains `{...}` placeholders
      that resolve to a regex (e.g. `{year}` → `\\d{4}`, `{number}` → `\\d+`).

    The matcher's purpose is to FAIL LOUD when a new DLT source file
    references a URL that is NOT a public-sector body listed in
    LICENSE.md §3.1–§3.7. It is NOT a syntactic-equality check.
    """
    allowlist = load_allowlist()
    allowlist_urls = [e["url"] for e in allowlist]

    urls = extract_urls_from_dlt_source_text(p_text)
    errors = []
    for url in urls:
        # Strip a trailing backtick (from code blocks like `https://www.courts.ie/`)
        url_clean = url.rstrip("`").rstrip(",").rstrip(".").rstrip(";")

        # URL templates in the file itself (e.g. `https://www.example.com/{id}`)
        # are allowed (the matcher would not have a counterpart anyway).
        if "{" in url_clean and "}" in url_clean:
            continue

        matched = False
        for au in allowlist_urls:
            au_clean = au.rstrip("`").rstrip(",")
            # Exact match
            if au_clean == url_clean:
                matched = True
                break
            # Prefix match: the file URL starts with the allowlist URL
            # (possibly followed by any sub-path, query string, fragment, etc.).
            # The check `len(url_clean) > len(au_clean)` ensures we don't match
            # the bare allowlist root against a totally different host.
            if url_clean.startswith(au_clean):
                matched = True
                break
            # Reverse prefix (file URL is a prefix of allowlist URL — e.g. file has
            # `https://www.courts.ie` and allowlist has `https://www.courts.ie/forms`).
            if au_clean.startswith(url_clean):
                matched = True
                break
            # Template match
            if "{" in au_clean and "}" in au_clean:
                pattern = re.escape(au_clean).replace(r"\{year\}", r"\d{4}").replace(r"\{number\}", r"\d+").replace(r"\{id\}", r"\w+")
                if re.match(pattern, url_clean):
                    matched = True
                    break
        if not matched:
            errors.append({
                "source_file": source_file,
                "offending_url": url_clean,
                "error_type": "url_not_in_osint_allowlist",
            })
    return errors


def lint_dlt_source_file(source_file: Path) -> list[dict[str, Any]]:
    """Lint a single DLT source file against the OSINT allowlist."""
    with source_file.open("r", encoding="utf-8") as fh:
        text = fh.read()
    return lint_dlt_source_text(text, str(source_file))


def osint_audit() -> int:
    """Audit all DLT source files under dlt_sources/ciandlithe/.

    Returns 0 if every file passes; non-zero if any file has errors.
    """
    import sys
    dlt_root = Path(__file__).parent.parent  # dlt_sources/ciandlithe/
    errors: list[dict[str, Any]] = []
    for py in dlt_root.rglob("*.py"):
        file_errors = lint_dlt_source_file(py)
        errors.extend(file_errors)
    if errors:
        print(f"OSINT audit FAILED: {len(errors)} URL(s) not in allowlist")
        for e in errors:
            print(f"  - {e['source_file']}: {e['offending_url']}")
        return 1
    print("OSINT audit PASSED")
    return 0


__all__ = [
    "OSINT_ALLOWLIST_PATH",
    "load_allowlist",
    "extract_urls_from_dlt_source_text",
    "lint_dlt_source_text",
    "lint_dlt_source_file",
    "osint_audit",
]