# Tasks: ciandlithe-students-union-adk-v1

## 1. OpenSpec artifacts

- [x] Write `openspec/changes/ciandlithe-students-union-adk-v1/proposal.md`
- [x] Write `openspec/changes/ciandlithe-students-union-adk-v1/tasks.md` (this file)
- [x] Write `openspec/changes/ciandlithe-students-union-adk-v1/cross-repo-sync.md`
- [x] Write `openspec/changes/ciandlithe-students-union-adk-v1/specs/ciandlithe-adk-students-union/spec.md`

## 2. agents/adk/students_union/ — config + tools (the pure-Python layer)

- [x] Write `agents/adk/students_union/__init__.py` (exports root_agent + 5 specialists)
- [x] Write `agents/adk/students_union/config.py` (StudentsUnionAgentConfig dataclass + config singleton)
- [x] Write `agents/adk/students_union/tools/__init__.py` (exports 5 tools + 14 dataclasses)
- [x] Write `agents/adk/students_union/tools/clubs_socs_validator.py` (ClubApplication + validate_club_application + ValidationResult)
- [x] Write `agents/adk/students_union/tools/grants_matcher.py` (4 funding pots + GrantApplication + match_grant_to_pot + GrantAward)
- [x] Write `agents/adk/students_union/tools/complaint_router.py` (Complaint + route_complaint + ComplaintRoute; 8 categories + 9-officer routing + urgent-keyword escalation)
- [x] Write `agents/adk/students_union/tools/election_validator.py` (Candidate + validate_candidate_eligibility + EligibilityResult; 6 hard + 2 soft rules)
- [x] Write `agents/adk/students_union/tools/class_rep_themer.py` (ClassRepReport + aggregate_class_rep_themes + ThemeAggregation; 7-theme taxonomy + weighted count)

## 3. agents/adk/students_union/ — the 5 specialist ADK agents

- [x] Write `agents/adk/students_union/clubs_socs_agent.py` (LlmAgent + FunctionTool wrapper)
- [x] Write `agents/adk/students_union/grants_funding_agent.py`
- [x] Write `agents/adk/students_union/class_rep_aggregator_agent.py`
- [x] Write `agents/adk/students_union/complaints_welfare_agent.py`
- [x] Write `agents/adk/students_union/elections_agent.py`

## 4. agents/adk/students_union/ — the root orchestrator

- [x] Write `agents/adk/students_union/root_agent.py` (students_union_root_agent + students_union_app + classify_su_query intent classifier)
- [x] Root agent has 5 sub_agents
- [x] Root agent has English + Irish bilingual instructions
- [x] classify_su_query covers all 5 case studies + ambiguous

## 5. agents/adk/students_union/ — CI smoke test

- [x] Write `agents/adk/students_union/_smoke_test.py`
- [x] Smoke test covers all 5 tools (positive + negative paths)
- [x] Smoke test covers the 6-query classify_su_query classifier
- [x] Smoke test constructs the 5 ADK agents + root_agent (stubs google.adk for test-time isolation)
- [x] Smoke test exits 0 when every assertion passes

## 6. Notebook — the case-study showcase

- [x] Write `notebooks/students_union_adk_case_studies.py` (marimo notebook with PEP 723 inline dependencies)
- [x] Notebook has a "Tools only (no LLM)" tab — deterministic, runnable without API keys
- [x] Notebook has 5 case-study tabs (one per workflow)
- [x] Notebook has a "Root orchestrator" tab demonstrating classify_su_query routing

## 7. Validation

- [x] Run `python3 agents/adk/students_union/_smoke_test.py` — pass
- [ ] Run `openspec validate ciandlithe-students-union-adk-v1 --strict` — TODO
- [ ] Run `openspec validate --all --strict` — TODO
- [ ] Run `python3 -c "import ast; ast.parse(open('notebooks/students_union_adk_case_studies.py').read())"` — TODO

## Verification

```bash
cd /Users/cianmacandeisigh/dev/ciandlithe
python3 agents/adk/students_union/_smoke_test.py
openspec validate ciandlithe-students-union-adk-v1 --strict
```
