# ciandlithe-adk-students-union Specification

## Purpose
Codify the 5-case-study Google ADK agent surface for the
**University of Galway Students' Union** (USG / Ollscoil na Gaillimhe /
Comhaltas na Mac Léinn) workflows. The agents are deployed under
`agents/adk/students_union/` in the ciandlithe repo and are the
canonical staging ground for non-curriculum Google ADK agents in
the cianfhoghlaim monorepo's broader ADK framework.

The 5 case studies are: Clubs & Societies registration review,
Grants & Funding triage, Class Rep feedback aggregation, Complaints
& Welfare routing, and Election & Referendum workflow. Each case
study pairs a Google ADK `LlmAgent` with a pure-Python `FunctionTool`
that implements the SU's published bylaws + funding policy + election
rules + safeguarding policy deterministically.

## Requirements

### Requirement: 5 specialist agents + 1 root orchestrator

The system SHALL provide 5 specialist Google ADK `LlmAgent` instances
under `agents/adk/students_union/`, each named `<workflow>_agent` for
the 5 case studies:

1. `clubs_socs_agent` — Clubs & Societies Registration review
2. `grants_funding_agent` — Grants & Funding triage
3. `class_rep_aggregator_agent` — Class Rep Feedback aggregation
4. `complaints_welfare_agent` — Complaints & Welfare triage
5. `elections_agent` — Election & Referendum workflow

Plus 1 root orchestrator `students_union_root_agent` (in
`agents/adk/students_union/root_agent.py`) that exposes the 5
specialists as `sub_agents` and includes a `classify_su_query(query)`
intent classifier to demonstrate routing independent of the LLM.

#### Scenario: All 5 specialists import + construct cleanly

- **WHEN** the operator runs `python3 agents/adk/students_union/_smoke_test.py`
- **THEN** all 5 specialists + the root_agent + the 5 pure-Python tools + the
  `classify_su_query` classifier MUST construct without errors
- **AND** the smoke test MUST exit 0 with the message "All 5 SU case-study
  tools + 5 agents + root_agent + classifier pass."

### Requirement: Each specialist wraps a pure-Python FunctionTool

Each specialist agent MUST wrap a pure-Python FunctionTool that
implements the SU workflow deterministically (no LLM, no network).
The 5 tools are:

- `validate_club_application` (8 hard requirements + 3 soft warnings + 0-100 score)
- `match_grant_to_pot` (4 funding pots + per-pot cap + first-time bonus + receipts penalty)
- `route_complaint` (8 categories + 9-officer routing + urgent-keyword escalation)
- `validate_candidate_eligibility` (6 hard + 2 soft rules + nominator counting)
- `aggregate_class_rep_themes` (7-theme taxonomy + weighted count + insufficient-data refusal)

#### Scenario: Pure-Python tools are testable without google.adk

- **WHEN** the operator runs the smoke test in an environment without
  `google-adk` installed
- **THEN** the 5 pure-Python tools MUST still produce correct results
  (the smoke test stubs google.adk via `_StubLlmAgent` so the tools
  are exercised without needing the ADK runtime)

### Requirement: The marimo case-study notebook

The system SHALL provide a marimo notebook at
`notebooks/students_union_adk_case_studies.py` that showcases all 5
case studies end-to-end. The notebook MUST have at least these tabs:

1. **Tools only (no LLM)** — deterministic, runnable without API keys
2. **Case Study 1: Clubs & Societies Registration** — sample application + decision
3. **Case Study 2: Grants & Funding Triage** — sample grant application + award
4. **Case Study 3: Class Rep Feedback Aggregation** — sample reports + themes
5. **Case Study 4: Complaints & Welfare Triage** — sample complaint + routing
6. **Case Study 5: Election & Referendum Workflow** — sample candidacy + eligibility
7. **Root Orchestrator Routing** — `classify_su_query` demo across many queries

#### Scenario: The notebook has PEP 723 inline dependencies

- **WHEN** the operator runs `python3 -c "import ast; ast.parse(open('notebooks/students_union_adk_case_studies.py').read())"`
- **THEN** the parse MUST succeed
- **AND** the notebook's first cell MUST be a `# /// script` block declaring
  the PEP 723 inline dependencies (marimo + google-adk + the local
  students_union package)

### Requirement: Deterministic CI gate

The system SHALL ship a smoke test at
`agents/adk/students_union/_smoke_test.py` that:

- Exercises every pure-Python tool with at least one positive + one
  negative test case
- Exercises the `classify_su_query` classifier with at least 6 test
  queries (one per case study + one ambiguous)
- Constructs the 5 ADK agents + the root_agent (stubbing google.adk
  so the test runs in any environment)
- Exits 0 on full pass, 1 on any failure

#### Scenario: The smoke test passes in CI

- **WHEN** CI runs `python3 agents/adk/students_union/_smoke_test.py`
- **THEN** the exit code MUST be 0
- **AND** stdout MUST contain "All 5 SU case-study tools + 5 agents +
  root_agent + classifier pass."

### Requirement: SU bylaws are encoded as constants, not prompts

The system SHALL encode the SU's published bylaws + funding policy +
election rules + safeguarding policy as Python constants in
`agents/adk/students_union/config.py`, NOT as LLM-prompted rules.
This ensures the agents make deterministic decisions and provides a
single source of truth that the SU staff can audit.

The minimum required constants:

- `max_travel_grant_eur: int` (default: 600)
- `max_equipment_grant_eur: int` (default: 1_500)
- `max_event_grant_eur: int` (default: 2_000)
- `max_welfare_grant_eur: int` (default: 400)
- `welfare_urgent_keywords: tuple[str, ...]` (default: 15 keywords)
- `min_nominator_signatures: int` (default: 10)
- `hustings_min_days_before_vote: int` (default: 7)
- `min_class_reps_for_aggregation: int` (default: 3)

#### Scenario: A reviewer can audit the SU bylaws in one file

- **WHEN** the SU Staff reviewer opens `agents/adk/students_union/config.py`
- **THEN** every threshold + keyword list used by the 5 agents MUST be visible
  in that single file
- **AND** no SU-bylaw threshold MUST be hardcoded in any of the 5 agent files
  (they MUST read from `config.*`)

### Requirement: Cross-repo smoke test

The system SHALL provide
`agents/adk/students_union/_smoke_test_cross_repo.py` that exercises
the 5 SU agents consuming data from the 5 KCG DLT sources in
`~/dev/kings_college_galway/dlt_sources/uog/`.

The smoke test MUST exercise 4 sections + 1 bonus test:

1. KCG data ingestion — every one of the 5 DLT sources yields its
   canonical sample rows
2. Case Study 1: Clubs & Socs × KCG press releases — apply for a new
   society name + cross-reference against the press archive
3. Case Study 2: Grants × KCG governance minutes — match a grant +
   count funding-policy governance decisions
4. Case Study 3: Class Rep × KCG course catalog — aggregate Class
   Rep reports whose module codes are real UoG courses from the
   course_catalog pipeline
5. **BONUS:** `classify_su_query` on 3 UoG-specific queries
   ("Apply for funding for the Seachtain na Gaeilge 2026 poetry slam",
   "Summarise Class Rep feedback from CS203", "I want to register a
   new sustainability society")

#### Scenario: Cross-repo smoke test passes on first run

- **WHEN** the operator runs `python3 agents/adk/students_union/_smoke_test_cross_repo.py`
- **THEN** the script MUST exit 0 with the message
  `Cross-repo integration PASS — SU agents consume real KCG data.`
- **AND** every section MUST log ✓ for the relevant counts (KCG row
  counts, SU decision values, classifier matches)

### Requirement: Marimo integration notebook

The system SHALL provide `notebooks/students_union_kcg_integration.py`
— a marimo notebook showcasing the cross-repo integration end-to-end.

The notebook MUST have at least 8 tabs:

1. Overview + cross-repo wiring diagram (ASCII art)
2. KCG data overview (every DLT source in 1 tab — row counts + sample rows)
3. Case Study 1: Clubs & Socs × KCG press releases
4. Case Study 2: Grants × KCG governance minutes
5. Case Study 3: Class Rep × KCG course catalog
6. Case Study 4: Complaints × KCG governance + academic calendar
7. Case Study 5: Elections × KCG governance
8. End-to-end orchestrator (the full pipeline summary)

#### Scenario: Notebook parses + imports both repos

- **WHEN** the operator runs `python3 -c "import ast; ast.parse(open('notebooks/students_union_kcg_integration.py').read())"`
- **THEN** the parse MUST succeed
- **AND** the notebook's first cell MUST be a `# /// script` block
  declaring the PEP 723 inline dependencies (`marimo + pandas +
  google-adk`)
- **AND** the notebook's `_bootstrap_paths` cell MUST add both
  `~/dev/ciandlithe` AND `~/dev/kings_college_galway` to `sys.path`

### Requirement: Mise task

The system SHALL provide a `ciandlithe:adk:su-smoke-test-cross-repo`
mise task in `mise.toml` that runs the cross-repo smoke test against
the cianchosaint/.venv (which has google-adk installed).

#### Scenario: Mise task exits 0

- **WHEN** the operator runs `mise run ciandlithe:adk:su-smoke-test-cross-repo`
- **THEN** the task MUST exit 0 with the same output as the
  cross-repo smoke test
