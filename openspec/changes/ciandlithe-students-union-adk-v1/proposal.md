# Change: ciandlithe-students-union-adk-v1

## Why

Three problems converged on 2026-09-13:

1. **The cianfhoghlaim Education Council (per `cianchosaint-pipeline-graph`/`ciandlithe-pipeline`) covers the Leaving Certificate + A-Level + GCSE subjects**, but there is no native surface for the **student-experience layer** — Clubs & Societies registration, Grants & Funding triage, Class Rep feedback aggregation, Complaints & Welfare routing, Election & Referendum workflows. These are the canonical Students' Union (USG / Ollscoil na Gaillimhe) workflows and they generate the most-incoming-traffic documents at any university.

2. **The Google ADK framework is the canonical agent runtime for the cianfhoghlaim monorepo** (per `agents/adk/`). But there are no working ADK case studies for civil-litigation-adjacent workflows. The ciandlithe repo is the natural staging ground for non-curriculum ADK agents that need to live outside the curriculum-only scope of cianfhoghlaim.

3. **The University of Galway / Ollscoil na Gaillimhe / NUI Galway / Kings College Galway** is the canonical anchor institution for the user's domain (per `leabharlann/ollscoil_na_gaillimhe/`). Building the SU agents for the University of Galway SU grounds the project in a real, public-sector institution with a published constitution + funding policy + election rules + safeguarding policy.

The result is 5 case studies, each one a Google ADK pattern that scales to any Irish / British Isles university SU:

  1. **Clubs & Societies Registration** — pattern: structured-form validator + scoring rubric
  2. **Grants & Funding Triage** — pattern: pot matcher + cap calculator + partial-award penalty
  3. **Class Rep Feedback Aggregator** — pattern: keyword/theme taxonomy + weighted count + minimum-N refusal rule
  4. **Complaints & Welfare Triage** — pattern: keyword category detector + urgent-keyword escalation + officer-routing table
  5. **Election & Referendum Workflow** — pattern: eligibility validator + nominator counting + repeat-term guard

## What changes

### Code — agents/adk/students_union/

- **NEW dir** `agents/adk/students_union/` with 11 files:
  - `__init__.py` — exports the root_agent + 5 specialists
  - `root_agent.py` — `students_union_root_agent` orchestrator + `students_union_app` + `classify_su_query` intent classifier
  - `config.py` — `StudentsUnionAgentConfig` dataclass + `config` singleton (model defaults + SU bylaws thresholds)
  - `clubs_socs_agent.py` — Clubs & Societies specialist
  - `grants_funding_agent.py` — Grants & Funding specialist
  - `class_rep_aggregator_agent.py` — Class Rep Feedback specialist
  - `complaints_welfare_agent.py` — Complaints & Welfare specialist
  - `elections_agent.py` — Election & Referendum specialist
  - `tools/__init__.py` — exports the 5 pure-Python tools + their dataclasses
  - `tools/clubs_socs_validator.py` — validate_club_application(ClubApplication) -> ValidationResult
  - `tools/grants_matcher.py` — match_grant_to_pot(GrantApplication) -> GrantAward (4 funding pots + caps + first-time bonus + receipts penalty)
  - `tools/complaint_router.py` — route_complaint(Complaint) -> ComplaintRoute (8 categories + urgent-keyword escalation + 9-officer routing table)
  - `tools/election_validator.py` — validate_candidate_eligibility(Candidate) -> EligibilityResult (6 hard requirements + 2 soft warnings)
  - `tools/class_rep_themer.py` — aggregate_class_rep_themes(List[ClassRepReport]) -> ThemeAggregation (7-theme taxonomy + weighted count + insufficient-data refusal)
  - `_smoke_test.py` — deterministic test runner (no LLM, no network) covering all 5 tools + 5 agents + root + classifier

### Notebook — notebooks/students_union_adk_case_studies.py

- **NEW marimo notebook** `notebooks/students_union_adk_case_studies.py` showcasing all 5 case studies end-to-end. PEP 723 inline dependencies. `@app.cell` layout with 5 tabs (one per case study) + a final "Root orchestrator routing" tab.

### CI gate

- The `_smoke_test.py` script is the CI gate. Exits 0 iff all 5 tools + 5 agents + root_agent + classifier construct correctly + every deterministic assertion passes. Run via `python3 agents/adk/students_union/_smoke_test.py`.

## Impact

- Affected specs: **1 NEW spec** `openspec/specs/ciandlithe-adk-students-union/spec.md` (written as a delta below)
- Affected code: **11 NEW Python files** under `agents/adk/students_union/`
- Affected notebook: **1 NEW marimo notebook** under `notebooks/`

## Out of scope (follow-up changes)

- The BAML extraction schemas for SU documents (manifesto text, complaint text, club application text) — follow-up `ciandlithe-students-union-baml-schemas-v1`
- The Convex schema for the SU workflow tables (ClubApplication + GrantApplication + ComplaintRoute + EligibilityResult + ThemeAggregation) — follow-up `ciandlithe-convex-students-union-v1`
- The Dagster orchestration for nightly SU workflow runs (e.g. nightly grants reconciliation) — follow-up `ciandlithe-dagster-students-union-v1`
- The marimo notebook's TanStack Start / CopilotKit chat surface for live SU queries — follow-up `ciandlithe-su-web-v1`

## Dependencies

`Blocked by: ciandlithe-repo-foundation-v1` (archived 2026-08-24).
`Affected repos: ciandlithe.`

## Cross-repo sync

This change touches ONLY the `ciandlithe` repo. However, the `marimo` notebook depends on the `marimo` + `marimo[baml]` + `google-adk` Python packages — these are already declared in `pyproject.toml` for the cianfhoghlaim + ciandlithe monorepos.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/ciandlithe

# 1. CI gate (the smoke test)
python3 agents/adk/students_union/_smoke_test.py
# Expected: "All 5 SU case-study tools + 5 agents + root_agent + classifier pass."

# 2. Openspec strict validation
openspec validate ciandlithe-students-union-adk-v1 --strict
# Expected: pass

# 3. Marimo notebook syntax check
python3 -c "import ast; ast.parse(open('notebooks/students_union_adk_case_studies.py').read())"
# Expected: exit 0
```
