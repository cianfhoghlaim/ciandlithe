# Cross-Repo Sync: ciandlithe-toolchain-repair-v1

This change touches ONLY the `ciandlithe/ciandlithe` repo. `cianfhoghlaim`
and `cianchosaint` are read-only references (the `lint_license.py` is
ported from `cianchosaint/scripts/lint_license.py`).

## Repo 1: ciandlithe (sole)

**Branch**: `main`
**Push target**: `github.com/cianfhoghlaim/ciandlithe`

**Files added:**
- `scripts/lint_license.py`
- `scripts/lint_drift_docs.py`
- `scripts/lint_skills.py`
- `dlt_sources/ciandlithe/ireland/pipeline.py`
- `dlt_sources/ciandlithe/uk/pipeline.py`
- `dlt_sources/ciandlithe/crown_dependencies/pipeline.py`
- `openspec/changes/ciandlithe-toolchain-repair-v1/{proposal.md, tasks.md, cross-repo-sync.md}`
- `openspec/changes/ciandlithe-toolchain-repair-v1/specs/ciandlithe-toolchain/spec.md`
- `openspec/specs/ciandlithe-toolchain/{spec.md, AGENTS.md}`

**Files modified:**
- `mise.toml` — adds `[tools]` section + replaces `python3` with
  `uv run --python 3.12 python` in every lint task + every milestone
  gate + the composite-pilot gate.
- `pyproject.toml` — adds `pymupdf>=1.24` + `pyyaml>=6.0` to
  `dependencies`.

**Commit message:**
`fix(toolchain): repair lint scripts + pin python 3.12 + add 3 jurisdiction pipeline runners`