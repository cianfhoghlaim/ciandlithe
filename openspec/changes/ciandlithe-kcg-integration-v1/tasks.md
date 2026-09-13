# Tasks: ciandlithe-kcg-integration-v1

## 1. OpenSpec artifacts

- [x] Write `openspec/changes/ciandlithe-kcg-integration-v1/proposal.md`
- [x] Write `openspec/changes/ciandlithe-kcg-integration-v1/tasks.md` (this file)
- [x] Write `openspec/changes/ciandlithe-kcg-integration-v1/cross-repo-sync.md`
- [x] Write `openspec/changes/ciandlithe-kcg-integration-v1/specs/ciandlithe-adk-students-union/spec.md` (delta)

## 2. Cross-repo smoke test

- [x] Write `agents/adk/students_union/_smoke_test_cross_repo.py`
- [x] Smoke test bootstraps both packages (ciandlithe + kcg)
- [x] Smoke test exercises 4 sections (KCG data + Clubs/Socs + Grants + Class Rep)
- [x] Smoke test exits 0 on full pass

## 3. Marimo notebook

- [x] Write `notebooks/students_union_kcg_integration.py`
- [x] Notebook has 8 tabs (overview + KCG data + 5 case studies + orchestrator)
- [x] Notebook imports both repos via sys.path manipulation
- [x] Notebook stubs google.adk + dlt so it runs in any environment

## 4. Mise task

- [x] Add `ciandlithe:adk:su-smoke-test-cross-repo` task to `mise.toml`

## 5. Validation

- [x] Run `python3 agents/adk/students_union/_smoke_test_cross_repo.py` — pass
- [x] Run `python3 -c "import ast; ast.parse(...)"` on the notebook — pass
- [ ] Run `openspec validate ciandlithe-kcg-integration-v1 --strict` — TODO
- [x] Run `mise run ciandlithe:adk:su-smoke-test-cross-repo` — pass

## Verification

```bash
cd ~/dev/ciandlithe
python3 agents/adk/students_union/_smoke_test_cross_repo.py
openspec validate ciandlithe-kcg-integration-v1 --strict
```
