# ciandlithe-adk-students-union Specification

## ADDED Requirements

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
