# Tasks: ciandlithe-ragas-eval-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.4.1 installed
- [x] Verify ciandlithe-blig-v1-spec-v1 has archived

## 1. Write the ciandlithe mirror RAGAS evaluator

- [x] Write `baml_src/_shared/ragas_evaluator.py` (~150 LOC) — the ciandlithe mirror evaluator

## 2. OpenSpec artifacts

- [x] Write `openspec/changes/ciandlithe-ragas-eval-v1/proposal.md` (DONE)
- [x] Write `openspec/changes/ciandlithe-ragas-eval-v1/tasks.md` (this file)
- [x] Write `openspec/changes/ciandlithe-ragas-eval-v1/cross-repo-sync.md` (DONE)
- [x] Write `openspec/changes/ciandlithe-ragas-eval-v1/specs/ciandlithe-blig-v1/spec.md` (the spec delta — DONE)
- [ ] Run `openspec validate ciandlithe-ragas-eval-v1 --strict`
- [ ] Run `openspec validate ciandlithe-blig-v1 --strict`

## Verification

```bash
cd /Users/cianmacandeisigh/dev/ciandlithe
openspec validate ciandlithe-ragas-eval-v1 --strict
# Expected: pass
```