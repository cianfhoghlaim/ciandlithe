# ciandlithe-toolchain Capability

## Purpose

`ciandlithe-toolchain` provides the pinned Python 3.12 + Node 20 + bun 1.4
toolchain, the 3 lint scripts (`lint:license`, `lint:drift-docs`, `lint:skills`),
and the 3 jurisdiction pipeline runners (`ciandlithe:blip:v1:m1/m2/m3`)
that every later work order depends on. Repairs the three defects
(`scripts/` missing, no `[tools]`, missing pipeline modules) identified
in the post-bootstrap audit.

## Background

The `ciandlithe-repo-foundation-v1` change shipped a correct skeleton
with a hollow middle: the mise tasks invoked `python3 scripts/*.py`
and `python3 -m dlt_sources.ciandlithe.{ireland,uk,crown_dependencies}.pipeline`
— none of which existed. Every verification gate failed. This spec
authorises the load-bearing toolchain repair that unblocks WO-1 through
WO-12.

## Requirements

### Requirement: The 3 lint scripts

The system SHALL provide 3 lint scripts at `scripts/` that enforce
the ciandlithe verification harness.

#### Scenario: `scripts/lint_license.py` exits 0 on a clean repo

- **WHEN** the operator runs `mise run lint:license`
- **THEN** the script SHALL AST-walk `dlt_sources/ciandlithe/**` + `agents/ciandlithe/**`
- **AND** SHALL extract every HTTPS string literal declared in a module decorated with `@dlt.source` / `@dlt.resource` / a Google ADK agent constructor
- **AND** SHALL assert each URL is prefix-matched by an entry in `dlt_sources/ciandlithe/common/osint_allowlist.yaml`
- **AND** SHALL assert each allowlist entry resolves to a British-Isles TLD
- **AND** SHALL exit 0 when all assertions pass; exit 1 with a structured per-URL error otherwise

#### Scenario: `scripts/lint_drift_docs.py` exits 0 when doc numbers match disk

- **WHEN** the operator runs `mise run lint:drift-docs`
- **THEN** the script SHALL parse every numeric claim in `AGENTS.md` + `README.md` (e.g. "7 cohorts", "13 cohorts", "113 PDFs")
- **AND** SHALL verify each claim against ground truth computed from disk (registry length, leabharlann PDF count)
- **AND** SHALL exit 0 when all match; exit 1 with a structured per-mismatch error otherwise

#### Scenario: `scripts/lint_skills.py` exits 0 when every skill frontmatter is valid

- **WHEN** the operator runs `mise run lint:skills`
- **THEN** the script SHALL validate every `.agents/skills/*/SKILL.md` frontmatter
- **AND** SHALL assert `name` is ≤64 chars + `description` is ≤1024 chars
- **AND** SHALL exit 0 when all pass; exit 1 with a structured per-file error otherwise

### Requirement: The 3 jurisdiction pipeline runners

The system SHALL provide 3 jurisdiction pipeline runners at
`dlt_sources/ciandlithe/{ireland,uk,crown_dependencies}/pipeline.py`.

#### Scenario: `ireland/pipeline.py` enumerates the ROI cohorts (m1 gate)

- **WHEN** the operator runs `mise run ciandlithe:blip:v1:m1`
- **THEN** the runner SHALL enumerate ROI cohorts from the registry
- **AND** SHALL assert the current-state m1 cohort count
- **AND** SHALL print a summary table
- **AND** SHALL exit 0 on success; exit 1 on assertion failure

#### Scenario: `uk/pipeline.py` enumerates the UK parties (m2 gate)

- **WHEN** the operator runs `mise run ciandlithe:blip:v1:m2`
- **THEN** the runner SHALL enumerate UK (NI + Scotland + Wales + England) parties
- **AND** SHALL assert the current-state m2 cohort count
- **AND** SHALL exit 0 on success

#### Scenario: `crown_dependencies/pipeline.py` enumerates the Crown Dependencies parties (m3 gate)

- **WHEN** the operator runs `mise run ciandlithe:blip:v1:m3`
- **THEN** the runner SHALL enumerate Jersey + Guernsey + IoM parties
- **AND** SHALL assert the current-state m3 cohort count
- **AND** SHALL exit 0 on success

### Requirement: The pinned toolchain

The system SHALL pin `python = "3.12"`, `node = "20"`, `bun = "1.4"` in
the `[tools]` section of `mise.toml`.

#### Scenario: `mise run ciandlithe:blip:v1:m1` uses Python 3.12

- **WHEN** the operator runs `mise run ciandlithe:blip:v1:m1`
- **THEN** the underlying Python invocation SHALL use Python 3.12+ (via `uv run --python 3.12`)
- **AND** SHALL NOT use the system `python3` (3.9.6)

#### Scenario: Every lint task uses Python 3.12

- **WHEN** the operator runs `mise run lint:license` or `mise run lint:drift-docs` or `mise run lint:skills`
- **THEN** the underlying script invocation SHALL use Python 3.12+

## Cross-references

- [`../../dlt_sources/ciandlithe/common/osint_allowlist.yaml`](../../dlt_sources/ciandlithe/common/osint_allowlist.yaml)
- [`../../LICENSE.md`](../../LICENSE.md) — §5.1 (OSINT ceiling) + §5.2 (PoI clause)
- [`../../AGENTS.md`](../../AGENTS.md) — the routing table
- [`../../pyproject.toml`](../../pyproject.toml) — the dep declarations