# Tasks: ciandlithe-blig-v1-spec-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.4.1 installed
- [x] Verify ciandlithe-repo-foundation-v1 has archived

## 1. Write the BLIG v1 spec

- [x] Write `openspec/specs/ciandlithe-blig-v1/spec.md`
- [x] Write `openspec/specs/ciandlithe-blig-v1/AGENTS.md`

## 2. Write the change artifacts

- [x] Write `openspec/changes/ciandlithe-blig-v1-spec-v1/proposal.md` (DONE)
- [x] Write `openspec/changes/ciandlithe-blig-v1-spec-v1/tasks.md` (this file)
- [x] Write `openspec/changes/ciandlithe-blig-v1-spec-v1/cross-repo-sync.md` (DONE)
- [x] Write `openspec/changes/ciandlithe-blig-v1-spec-v1/specs/ciandlithe-blig-v1/spec.md` (DONE)
- [ ] Run `openspec validate ciandlithe-blig-v1-spec-v1 --strict`
- [ ] Run `openspec validate ciandlithe-blig-v1 --strict`
- [ ] Run `openspec validate --all --strict`

## Verification

```bash
cd /Users/cianmacandeisigh/dev/ciandlithe
openspec validate ciandlithe-blig-v1-spec-v1 --strict
# Expected: pass

openspec validate ciandlithe-blig-v1 --strict
# Expected: pass
```