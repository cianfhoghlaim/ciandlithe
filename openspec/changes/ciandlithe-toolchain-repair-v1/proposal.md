# Change: ciandlithe-toolchain-repair-v1

## Why

The ciandlithe repo was bootstrapped in a single "repo foundation" commit
(`ciandlithe-repo-foundation-v1`, 2026-08-24) that shipped a correct
skeleton with a hollow middle. Audit found three confirmed defects
that block every subsequent work order:

1. **`scripts/` directory does not exist.** The `mise.toml` tasks
   `lint:license`, `lint:drift-docs`, `lint:skills` all invoke
   `python3 scripts/<x>.py`, so `mise run lint` and `mise run core`
   fail immediately. The 4 BLIP milestone gates (m1/m2/m3/ga) and the
   composite-pilot gate all transit through `mise run openspec:validate-all`
   → they fail too.

2. **No `[tools]` section in `mise.toml`; system `python3` is 3.9.6**
   while `pyproject.toml` requires `>=3.12`. Every `python3 -m …` task
   runs on 3.9 — this is the same `datetime.UTC` ImportError pattern that
   already hit the foundation commit. `uv 0.12.1` is installed and
   unused.

3. **All 4 BLIP milestone gates reference modules that do not exist.**
   `ciandlithe:blip:v1:m1` runs
   `python3 -m dlt_sources.ciandlithe.ireland.pipeline` — the
   `pipeline` module does not exist. Same for `uk.pipeline` and
   `crown_dependencies.pipeline`. Every milestone gate fails. There
   is no working verification gate for the BLIP v1 pipeline.

Until these three are fixed, every later work order reports false
failures and any agent (human or otherwise) burns time debugging the
harness instead of building the system. This change is the
load-bearing foundation for WO-1 … WO-12.

## What changes

- **NEW scripts/**
  - `scripts/lint_license.py` — AST-walks `dlt_sources/ciandlithe/**`
    + `agents/ciandlithe/**`, extracts every HTTPS string literal
    declared in a module decorated with `@dlt.source` / `@dlt.resource`
    / a Google ADK agent constructor; asserts each is prefix-matched by
    an entry in `dlt_sources/ciandlithe/common/osint_allowlist.yaml`;
    asserts the allowlist entry resolves to a British-Isles TLD.
    Ported from cianchosaint's `scripts/lint_license.py`; ciandlithe
    allowlist uses `url:` (not `source_url:`) so the loader is adapted.
  - `scripts/lint_drift_docs.py` — parses every numeric claim in
    `AGENTS.md` and `README.md` (e.g. "7 cohorts", "13 cohorts",
    "113 PDFs") and verifies against ground truth computed from disk
    (registry length, leabharlann PDF counts). Returns exit 1 with a
    structured list of mismatches.
  - `scripts/lint_skills.py` — validates every
    `.agents/skills/*/SKILL.md` frontmatter has `name` (≤64 chars) and
    `description` (≤1024 chars). Exit 1 on any violation.

- **NEW jurisdiction pipeline runners** (REAL cohort-enumerating
  runners, not stubs) at
  - `dlt_sources/ciandlithe/ireland/pipeline.py`
  - `dlt_sources/ciandlithe/uk/pipeline.py`
  - `dlt_sources/ciandlithe/crown_dependencies/pipeline.py`
  Each enumerates its jurisdiction's cohorts from the
  `PILOT_PARTIES` / cohort registry, asserts the minimum cohort count
  for its milestone (m1=7, m2=14, m3=3), and prints a summary table.

- **MODIFY `mise.toml`**
  - Add `[tools]` section pinning `python = "3.12"`, `node = "20"`,
    `bun = "1.4"`.
  - Replace every `python3 <x>` with `uv run --python 3.12 python <x>`
    (the lint tasks + the milestone gate inner calls).

- **MODIFY `pyproject.toml`** — add `pymupdf>=1.24` (used in WO-1;
  pin now so `uv run --python 3.12` resolves cleanly) + `pyyaml>=6.0`
  (used by the new lint scripts).

- **NEW openspec artifacts** under
  `openspec/changes/ciandlithe-toolchain-repair-v1/`:
  - `proposal.md` (this file)
  - `tasks.md`
  - `cross-repo-sync.md`
  - `specs/ciandlithe-toolchain/spec.md` (the spec delta)

- **NEW canonical spec** `openspec/specs/ciandlithe-toolchain/`
  containing `spec.md` (the end state) + `AGENTS.md` (≤30 lines).

## Impact

- Affected specs: **1 NEW spec** (`ciandlithe-toolchain`).
- Affected code/config: 5 NEW files (3 lint scripts + 3 jurisdiction
  pipeline runners) + 2 MODIFIED files (`mise.toml`, `pyproject.toml`)
  + 4 NEW openspec artifacts + 1 NEW canonical spec.
- Subsequent changes depend on this: every WO-1 through WO-12 invokes
  the verification harness repaired here.

## Out of scope (follow-up changes)

- WO-1 (corpus ingest) onward — the BAML extraction functions, the
  cocoindex flows, the timeline visualiser, the case-study expansion,
  the lakehouse medallion, the orchestration, the per-persona web apps,
  the agent fleet, the initiation runbook. All separate changes.

## Dependencies

`Blocked by: none.`
`Blocked by (soft): ciandlithe-repo-foundation-v1` (archived 2026-08-24;
the source of the defective `mise.toml`).
`Affected repos: ciandlithe.`

## Cross-repo sync

This change touches ONLY the `ciandlithe` repo. `cianfhoghlaim` and
`cianchosaint` are read-only references (the `lint_license.py` is
ported from `cianchosaint/scripts/lint_license.py`).

## Verification

```bash
cd /Users/cianmacandeisigh/dev/ciandlithe
openspec validate ciandlithe-toolchain-repair-v1 --strict
mise run openspec:validate-all
mise run lint
mise run ciandlithe:blip:v1:m1
mise run ciandlithe:blip:v1:m2
mise run ciandlithe:blip:v1:m3
uv run --python 3.12 python -m dlt_sources.ciandlithe.ireland.pipeline --dry-run
uv run --python 3.12 python -m dlt_sources.ciandlithe.uk.pipeline --dry-run
uv run --python 3.12 python -m dlt_sources.ciandlithe.crown_dependencies.pipeline --dry-run
uv run --python 3.12 python -m pytest tests/ -v
```

All must exit 0. Paste real command output in the commit message.