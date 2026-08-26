## ADDED Requirements

### Requirement: The 3 lint scripts

The system SHALL provide 3 lint scripts at `scripts/` that enforce the
ciandlithe verification harness.

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

#### Scenario: `ireland/pipeline.py` enumerates ≥7 cohorts (m1 gate)

- **WHEN** the operator runs `mise run ciandlithe:blip:v1:m1`
- **THEN** the runner SHALL enumerate ROI cohorts from the registry
- **AND** SHALL assert ≥7 cohorts
- **AND** SHALL print a summary table
- **AND** SHALL exit 0 on success; exit 1 on assertion failure

#### Scenario: `uk/pipeline.py` enumerates ≥14 cohorts (m2 gate)

- **WHEN** the operator runs `mise run ciandlithe:blip:v1:m2`
- **THEN** the runner SHALL enumerate UK (NI + Scotland + Wales + England) cohorts
- **AND** SHALL assert ≥14 cohorts

#### Scenario: `crown_dependencies/pipeline.py` enumerates ≥3 cohorts (m3 gate)

- **WHEN** the operator runs `mise run ciandlithe:blip:v1:m3`
- **THEN** the runner SHALL enumerate Crown Dependencies (Jersey + Guernsey + IoM) cohorts
- **AND** SHALL assert ≥3 cohorts

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

### Requirement: The new ciandlithe-toolchain spec

The system SHALL provide a canonical spec at
`openspec/specs/ciandlithe-toolchain/{spec.md, AGENTS.md}` documenting
the 3 lint scripts + the 3 jurisdiction pipeline runners + the pinned toolchain.

#### Scenario: The canonical spec exists + AGENTS.md is ≤30 lines

- **WHEN** the operator runs `ls openspec/specs/ciandlithe-toolchain/`
- **THEN** the directory SHALL contain both `spec.md` and `AGENTS.md`
- **AND** `AGENTS.md` SHALL be ≤30 lines (the repo-hygiene-agent-routing convention)