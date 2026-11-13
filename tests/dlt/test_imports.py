"""Phase 2.1 sister-repo smoke test — discover every top-level sub-tree of
`dlt_sources/` and record whether `importlib.import_module("dlt_sources.<subtree>")`
succeeds or raises ImportError.

Per `openspec/changes/2026-08-24-dlt-sources-to-multi-repo-scaffold-v1`
parent change §13 (the ciandlithe sister-repo init), this test reuses the
Phase 0.1 cianfhoghlaim smoke-test pattern at
`cianfhoghlaim/tests/dlt/test_imports.py` and adapts it for the
standalone ciandlithe sister-repo shape.

The JSON summary is the durable artifact that the sister init change
consumes to verify the skeleton is wired.

This test is READ-ONLY on `dlt_sources/` — it does not modify any
source file. It is expected to FAIL for some sub-trees today (the
standalone bulk-copy may have import errors that the Phase 3 carve-out
will resolve); the failures are the signal.
"""

from __future__ import annotations

import importlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
DLT_SOURCES_DIR = REPO_ROOT / "dlt_sources"
SYNC_REPORTS_DIR = REPO_ROOT / "stedding" / "sync-reports"

# Sub-trees to skip from the import walk (Python bytecode cache only —
# everything else is a real, intentful sub-tree of the DLT layer).
_SKIP_NAMES = frozenset({"__pycache__", ".DS_Store"})


def _discover_subtrees() -> list[str]:
    """Return every top-level sub-tree of `dlt_sources/` in deterministic
    alphabetical order. Underscore-prefixed sub-trees (e.g. `_cross/`,
    `_lakehouse/`) are included — they are first-class package roots.
    """
    if not DLT_SOURCES_DIR.is_dir():
        raise FileNotFoundError(f"dlt_sources directory missing: {DLT_SOURCES_DIR}")
    names = [
        p.name
        for p in sorted(DLT_SOURCES_DIR.iterdir(), key=lambda p: p.name)
        if p.is_dir() and p.name not in _SKIP_NAMES and not p.name.startswith(".")
    ]
    return names


def _first_error_line(exc: BaseException) -> str:
    """Return a single, JSON-safe, deterministic first-line error message.

    For ImportError we extract `exc.name` (the missing module) when
    present, falling back to `str(exc)`. For other exceptions we take
    `type(exc).__name__` + the first line of `str(exc)`.
    """
    if isinstance(exc, ImportError):
        missing = getattr(exc, "name", None)
        msg = str(exc).splitlines()[0] if str(exc) else ""
        if missing:
            return f"ImportError: {missing}: {msg}".rstrip(": ").strip()
        return f"ImportError: {msg}".strip() if msg else "ImportError"
    first = str(exc).splitlines()[0] if str(exc) else ""
    return f"{type(exc).__name__}: {first}".strip()


def _run_smoke() -> dict:
    """Walk every discovered sub-tree, time each import, and return the
    summary dict ready for JSON serialisation.
    """
    subtrees = _discover_subtrees()
    if not subtrees:
        raise RuntimeError(
            f"No sub-trees discovered under {DLT_SOURCES_DIR} — "
            "the sister-repo smoke test has nothing to report."
        )

    results: list[dict] = []
    ok_count = 0
    fail_count = 0
    total_duration_ms = 0

    overall_start = time.monotonic()
    for name in subtrees:
        module_name = f"dlt_sources.{name}"
        start = time.monotonic()
        try:
            importlib.import_module(module_name)
            duration_ms = int((time.monotonic() - start) * 1000)
            results.append(
                {
                    "subtree": name,
                    "status": "ok",
                    "error": None,
                    "duration_ms": duration_ms,
                }
            )
            ok_count += 1
            total_duration_ms += duration_ms
        except BaseException as exc:  # noqa: BLE001 — we want every failure surfaced
            duration_ms = int((time.monotonic() - start) * 1000)
            results.append(
                {
                    "subtree": name,
                    "status": "fail",
                    "error": _first_error_line(exc),
                    "duration_ms": duration_ms,
                }
            )
            fail_count += 1
            total_duration_ms += duration_ms
    overall_duration_ms = int((time.monotonic() - overall_start) * 1000)

    summary = {
        "schema_version": 1,
        "change_id": "2026-08-24-ciandlithe-init-v1",
        "phase": "2.1",
        "sister_repo": "ciandlithe",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version.split()[0],
        "dlt_sources_dir": str(DLT_SOURCES_DIR.relative_to(REPO_ROOT)),
        "total_subtrees": len(subtrees),
        "ok_count": ok_count,
        "fail_count": fail_count,
        "total_duration_ms": total_duration_ms,
        "overall_duration_ms": overall_duration_ms,
        "results": results,
    }
    return summary


def test_dlt_subtree_imports(tmp_path: Path) -> None:
    """Smoke-test every `dlt_sources.<subtree>` import and persist a JSON
    summary. The test ALWAYS writes the report (even if every import
    fails) — that is the deliverable, not the pass/fail outcome.

    Asserted: total wall-clock < 60s (mirroring the cianfhoghlaim budget).
    Asserted: report exists on disk and parses as JSON.
    Asserted: every discovered sub-tree has a corresponding result row.

    The pass/fail of the test ITSELF is dictated by whether the import
    walk completed inside the 60s budget. Individual subtree failures
    are recorded in the JSON, not used to fail the pytest run — we
    explicitly do NOT want a red CI to mask the report.
    """
    SYNC_REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    summary = _run_smoke()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report_path = SYNC_REPORTS_DIR / f"dlt-smoke-run-ciandlithe-{timestamp}.json"
    report_path.write_text(json.dumps(summary, indent=2, sort_keys=False) + "\n")

    # Pytest-side assertions (budget + report integrity only — NOT
    # the import outcomes themselves, which are recorded in the JSON).
    assert summary["overall_duration_ms"] < 60_000, (
        f"dlt sister-repo smoke walk exceeded the 60s budget "
        f"({summary['overall_duration_ms']}ms)"
    )
    assert report_path.is_file(), f"smoke report missing: {report_path}"
    reloaded = json.loads(report_path.read_text())
    assert reloaded["total_subtrees"] == summary["total_subtrees"]
    assert len(reloaded["results"]) == summary["total_subtrees"]
    assert {r["subtree"] for r in reloaded["results"]} == {
        r["subtree"] for r in summary["results"]
    }

    # Print a one-line summary so the CI log captures it. The pytest
    # `-q` flag silences per-test status; this line is the canonical
    # "did the sister-repo smoke walk happen?" signal.
    print(
        f"\n[ciandlithe:dlt:smoke-all] {summary['total_subtrees']} sub-trees "
        f"({summary['ok_count']} ok / {summary['fail_count']} fail) "
        f"in {summary['overall_duration_ms']}ms — "
        f"report: {report_path.relative_to(REPO_ROOT)}"
    )


if __name__ == "__main__":
    # Skeleton entrypoint: the parent change's §V.11 verification
    # delegates to `uv run pytest tests/dlt/test_imports.py -q`.
    raise SystemExit(
        "Run via `uv run pytest tests/dlt/test_imports.py -q` "
        "(or `mise run ciandlithe:smoke-all` once the per-sister "
        "mise.toml task is wired)."
    )