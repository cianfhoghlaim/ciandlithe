# Tasks: ciandlithe-toolchain-repair-v1

## 0. Pre-flight

- [x] Verify the toolchain defect (no `scripts/`, no `[tools]`, no `pipeline` modules)
- [x] Verify the ciandlithe OSINT allowlist uses `url:` (not `source_url:`)
- [x] Verify `pyproject.toml` requires `python >=3.12`
- [x] Verify `uv 0.12.1` is installed and unused

## 1. Write the openspec change artifacts

- [x] `openspec/changes/ciandlithe-toolchain-repair-v1/proposal.md`
- [x] `openspec/changes/ciandlithe-toolchain-repair-v1/tasks.md` (this file)
- [x] `openspec/changes/ciandlithe-toolchain-repair-v1/cross-repo-sync.md`
- [x] `openspec/changes/ciandlithe-toolchain-repair-v1/specs/ciandlithe-toolchain/spec.md`
- [x] `openspec/specs/ciandlithe-toolchain/spec.md` (the canonical end-state)
- [x] `openspec/specs/ciandlithe-toolchain/AGENTS.md` (≤30 lines)

## 2. Create the 3 lint scripts

- [x] `scripts/lint_license.py` — port from `cianchosaint/scripts/lint_license.py`,
      adapt `load_allowlist` to read `url:` (not `source_url:`), expand
      `BRITISH_ISLES_DOMAINS` to include `courts.ie`, `irishstatutebook.ie`,
      `citizensinformation.ie`, `nidirect.gov.uk`, `scotcourts.gov.uk`,
      `judiciary.uk`, `gov.wales`, `phw.nhs.wales`, `nhsinform.scot`,
      `hpsc.ie`, `gmc-uk.org`, `rte.ie`, `met.ie`.
- [x] `scripts/lint_drift_docs.py` — regex-extract every numeric claim
      in `AGENTS.md` + `README.md` (cohort count, PDF count, jurisdiction
      count, skill count) and verify against disk.
- [x] `scripts/lint_skills.py` — every `.agents/skills/*/SKILL.md`
      frontmatter has `name` (≤64 chars) + `description` (≤1024 chars).

## 3. Create the 3 jurisdiction pipeline runners

- [x] `dlt_sources/ciandlithe/ireland/pipeline.py` — enumerates the ROI
      cohorts from `PILOT_PARTIES` + asserts ≥7 (m1 gate) + prints a
      summary table. `--dry-run` skips DLT loads.
- [x] `dlt_sources/ciandlithe/uk/pipeline.py` — same shape for NI +
      Scotland + Wales + England. Asserts ≥14 (m2 gate).
- [x] `dlt_sources/ciandlithe/crown_dependencies/pipeline.py` — Jersey
      + Guernsey + IoM. Asserts ≥3 (m3 gate).

## 4. Modify mise.toml

- [x] Add `[tools]` with `python = "3.12"`, `node = "20"`, `bun = "1.4"`.
- [x] Replace `python3 scripts/<x>.py` with
      `uv run --python 3.12 python scripts/<x>.py` in every lint task.
- [x] Replace `python3 -m <x>` with `uv run --python 3.12 python -m <x>`
      in the milestone gates + composite-pilot gate.

## 5. Modify pyproject.toml

- [x] Add `pymupdf>=1.24` to `dependencies` (used in WO-1; pin now)
- [x] Add `pyyaml>=6.0` to `dependencies` (used by the 3 lint scripts)

## 6. Run the verification gates (paste real output in the commit message)

- [x] `openspec validate ciandlithe-toolchain-repair-v1 --strict`
- [x] `openspec validate ciandlithe-toolchain --strict`
- [x] `mise run openspec:validate-all`
- [x] `mise run lint` (the 3 lints)
- [x] `mise run ciandlithe:blip:v1:m1`
- [x] `mise run ciandlithe:blip:v1:m2`
- [x] `mise run ciandlithe:blip:v1:m3`
- [x] `uv run --python 3.12 python -m pytest tests/ -v` (existing 7 smoke tests must still pass)

## 7. Commit

- [x] `git add -A`
- [x] `git commit -m "fix(toolchain): repair lint scripts + pin python 3.12 + add 3 jurisdiction pipeline runners"`

## 8. Follow-up openspec changes (NOT in this change's scope)

- [ ] `ciandlithe-leabharlann-corpus-ingest-v1` (WO-1)
- [ ] `ciandlithe-lakehouse-medallion-v1` (WO-2)
- [ ] `ciandlithe-blip-v1-cohort-expansion-v1` (WO-3)
- [ ] `ciandlithe-temporal-graph-v1` (WO-4)
- [ ] `ciandlithe-limitation-calculator-v1` (WO-5)
- [ ] `ciandlithe-timeline-visualiser-v1` (WO-6)
- [ ] `ciandlithe-casefile-convention-v1` (WO-7)
- [ ] `ciandlithe-case-study-expansion-v1` (WO-8)
- [ ] `ciandlithe-orchestration-v1` (WO-9)
- [ ] `ciandlithe-per-persona-web-surfaces-v1` (WO-10)
- [ ] `ciandlithe-agent-fleet-v1` (WO-11)
- [ ] `ciandlithe-initiation-runbook-v1` (WO-12)