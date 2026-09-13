# Cross-repo sync: ciandlithe-students-union-adk-v1

This change touches ONLY the `ciandlithe` repo. There are no
upstream/downstream effects on:

- `cianfhoghlaim` — the main monorepo (the SU agents do not depend
  on any cianfhoghlaim-only module)
- `cianchosaint` — the defence / policing / intelligence-oversight
  platform (no shared modules with ciandlithe at the Python level)

## Files touched

| Path | Repo | Change |
|:--|:--|:--|
| `agents/adk/students_union/__init__.py` | ciandlithe | NEW |
| `agents/adk/students_union/config.py` | ciandlithe | NEW |
| `agents/adk/students_union/root_agent.py` | ciandlithe | NEW |
| `agents/adk/students_union/clubs_socs_agent.py` | ciandlithe | NEW |
| `agents/adk/students_union/grants_funding_agent.py` | ciandlithe | NEW |
| `agents/adk/students_union/class_rep_aggregator_agent.py` | ciandlithe | NEW |
| `agents/adk/students_union/complaints_welfare_agent.py` | ciandlithe | NEW |
| `agents/adk/students_union/elections_agent.py` | ciandlithe | NEW |
| `agents/adk/students_union/tools/__init__.py` | ciandlithe | NEW |
| `agents/adk/students_union/tools/clubs_socs_validator.py` | ciandlithe | NEW |
| `agents/adk/students_union/tools/grants_matcher.py` | ciandlithe | NEW |
| `agents/adk/students_union/tools/complaint_router.py` | ciandlithe | NEW |
| `agents/adk/students_union/tools/election_validator.py` | ciandlithe | NEW |
| `agents/adk/students_union/tools/class_rep_themer.py` | ciandlithe | NEW |
| `agents/adk/students_union/_smoke_test.py` | ciandlithe | NEW |
| `notebooks/students_union_adk_case_studies.py` | ciandlithe | NEW |
| `openspec/specs/ciandlithe-adk-students-union/spec.md` | ciandlithe | NEW (the delta in `changes/ciandlithe-students-union-adk-v1/specs/...` is the source of truth until archive) |
| `openspec/changes/ciandlithe-students-union-adk-v1/{proposal,tasks,cross-repo-sync}.md` | ciandlithe | NEW |

## Soft dependencies (informational only)

- **Marimo** is required to run the `notebooks/students_union_adk_case_studies.py`
  notebook. Already declared in `pyproject.toml` as a cianfhoghlaim + ciandlithe
  dev dependency.
- **Google ADK** (`google-adk>=2.9.0`) is required to construct the 5 specialist
  agents + the root_agent. Already declared in `pyproject.toml` as a
  ciandlithe runtime dependency (the wholesale-copy from cianfhoghlaim pulled
  it in transitively).
- The marimo notebook uses the cianfhoghlaim BAML extraction functions
  (`baml_src/cianchosaint/politics/politician_extraction.baml`) for
  optional enrichment of the Class Rep theme extraction. This is a soft
  dependency — the notebook degrades to regex-only theme extraction if
  BAML is not available.
