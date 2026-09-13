# Cross-repo sync: ciandlithe-kcg-integration-v1

This change ships the ciandlithe-side of the cross-repo integration.
The kcg-side was already shipped as part of
`kcg-university-of-galway-doc-processing-v1`.

## Files touched (ciandlithe)

| Path | Change |
|:--|:--|
| `agents/adk/students_union/_smoke_test_cross_repo.py` | NEW |
| `notebooks/students_union_kcg_integration.py` | NEW |
| `mise.toml` | +1 task |
| `openspec/changes/ciandlithe-kcg-integration-v1/{proposal,tasks,cross-repo-sync}.md` | NEW |
| `openspec/changes/ciandlithe-kcg-integration-v1/specs/ciandlithe-adk-students-union/spec.md` | NEW |

## Files consumed cross-repo (read-only — no changes)

| Path | Repo | Used by |
|:--|:--|:--|
| `dlt_sources/uog/academic_calendar.py` | kings_college_galway | Notebook tabs 2 + 6 |
| `dlt_sources/uog/course_catalog.py` | kings_college_galway | Notebook tab 5 |
| `dlt_sources/uog/university_council_minutes.py` | kings_college_galway | Notebook tabs 4 + 6 + 7 |
| `dlt_sources/uog/press_releases.py` | kings_college_galway | Notebook tab 3 |
| `dlt_sources/uog/research_outputs.py` | kings_college_galway | Notebook tab 5 |
| `agents/adk/students_union/tools/*.py` | ciandlithe | Notebook tabs 3-7 |

## Soft dependencies

- **KCG repo must exist at `~/dev/kings_college_galway/`** — required by
  the smoke test (sys.path manipulation)
- **google-adk 2.9.0** — already declared in pyproject.toml
- **dlt>=1.0.0** — already declared in the KCG pyproject.toml

## Licence alignment

- ciandlithe: BUSL-1.1 v2 CIANDLITHE edition (court-facing procedural
  rules scope)
- kcg: BUSL-1.1 (KCG edition) (University of Galway public-document
  processing scope)

The notebook imports data from BOTH scopes but never aggregates them
into a single repository — the SU agents consume the KCG data as
context for their decision logic, not as primary source-of-truth
data.
