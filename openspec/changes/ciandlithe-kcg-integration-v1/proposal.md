# Change: ciandlithe-kcg-integration-v1

## Why

The `ciandlithe-students-union-adk-v1` change ships the 5 SU ADK
agents + the 5 pure-Python tools. The `kcg-university-of-galway-doc-processing-v1`
change (in the `kings_college_galway` repo) ships the 5 KCG DLT
sources for University of Galway public-document ingestion.

These two changes were designed to interoperate (per the
cross-repo-sync.md in the SU change), but the actual cross-repo
import + smoke test + integration notebook were not shipped as part
of either change. This change ships:

  1. The cross-repo smoke test (`_smoke_test_cross_repo.py`)
  2. The marimo notebook demonstrating end-to-end integration
     (`notebooks/students_union_kcg_integration.py`)
  3. The mise task for the cross-repo smoke test

## What changes

### Code — agents/adk/students_union/

- **NEW file** `agents/adk/students_union/_smoke_test_cross_repo.py`
  (~340 LOC) — exercises the 5 SU agents consuming the 5 KCG DLT
  sources end-to-end. 4 sections + bonus classifier test, all
  deterministic, exits 0 on full pass.

### Notebook — notebooks/

- **NEW file** `notebooks/students_union_kcg_integration.py` (~764
  LOC) — 8 marimo tabs showcasing the cross-repo integration:
  1. Overview + cross-repo wiring diagram
  2. KCG data overview (every DLT source in 1 tab)
  3. Case Study 1: Clubs & Socs × KCG press releases
  4. Case Study 2: Grants × KCG governance minutes
  5. Case Study 3: Class Rep × KCG course catalog
  6. Case Study 4: Complaints × KCG governance + academic calendar
  7. Case Study 5: Elections × KCG governance
  8. End-to-end orchestrator

### Mise tasks

- **NEW task** `ciandlithe:adk:su-smoke-test-cross-repo` in
  `mise.toml` — runs `_smoke_test_cross_repo.py` against the
  cianchosaint/.venv (which has google-adk installed).

### Dependency wiring

The notebook imports BOTH repos via `sys.path` manipulation:

    notebook_dir     = ~/dev/ciandlithe/notebooks
    ciandlithe_root  = ~/dev/ciandlithe
    kcg_root         = ~/dev/kings_college_galway

Both paths are prepended to `sys.path` at notebook startup, then
`dlt_sources.uog` (KCG) + `agents.adk.students_union` (ciandlithe)
are imported in dependency order.

## Impact

- Affected specs: **1 NEW spec delta** `openspec/changes/ciandlithe-kcg-integration-v1/specs/ciandlithe-adk-students-union/spec.md`
- Affected code: **2 NEW files** (the smoke test + the notebook)
- Affected mise tasks: **1 NEW task** (`ciandlithe:adk:su-smoke-test-cross-repo`)

## Out of scope (follow-up changes)

- LLM-backed invocation of the SU agents against real KCG data
  (the smoke test stubs `google.adk` so it runs without an LLM;
  the follow-up `ciandlithe-adk-live-llm-invocation-v1` wires the
  agents against the 4-tier provider chain)
- MotherDuck destination wiring for the KCG tables (the
  `kcg-motherduck-destination-v1` follow-up)
- Beng + LanceDB semantic search UI (the marimo notebook shows
  the cross-repo data flow but does not provide a search UI;
  the `kcg-web-uog-v1` follow-up builds the TanStack Start surface)

## Dependencies

`Blocked by:`
  - `ciandlithe-students-union-adk-v1` (the 5 SU agents + 5 tools)
  - `kcg-university-of-galway-doc-processing-v1` (in the
    `kings_college_galway` repo — the 5 KCG DLT sources)

`Affected repos: ciandlithe.`

## Cross-repo sync

This change ships the ciandlithe-side of the cross-repo integration.
The kcg-side was already shipped as part of
`kcg-university-of-galway-doc-processing-v1`.

| Path | Repo | Change |
|:--|:--|:--|
| `notebooks/students_union_kcg_integration.py` | ciandlithe | NEW |
| `agents/adk/students_union/_smoke_test_cross_repo.py` | ciandlithe | NEW |
| `mise.toml` | ciandlithe | +1 task |

## Verification

```bash
cd ~/dev/ciandlithe

# 1. The cross-repo smoke test
/Users/cianmacandeisigh/dev/cianchosaint/.venv/bin/python3 \
    agents/adk/students_union/_smoke_test_cross_repo.py
# Expected: "Cross-repo integration PASS — SU agents consume real KCG data."

# 2. Openspec strict validation
openspec validate ciandlithe-kcg-integration-v1 --strict
# Expected: pass

# 3. Marimo notebook parse check
python3 -c "import ast; ast.parse(open('notebooks/students_union_kcg_integration.py').read())"
# Expected: exit 0

# 4. Mise task runs the smoke test
mise run ciandlithe:adk:su-smoke-test-cross-repo
# Expected: same as step 1
```
