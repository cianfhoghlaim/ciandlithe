# Tasks: ciandlithe-langfuse-prompt-mirror-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.4.1 installed
- [x] Verify cianchosaint `baml_src/_shared/langfuse_prompt_resolver.py` exists (the upstream pattern)

## 1. Write the mirror Langfuse prompt resolver

- [x] Write `baml_src/_shared/langfuse_prompt_resolver.py` (~150 LOC) — the mirror resolver
  - 15 canonical ciandlithe prompt names
  - Same circuit-breaker + graceful-fallback pattern as cianchosaint
  - `LangfusePromptResolver`, `LangfuseCircuitBreaker`, `LangfusePromptHit`, `get_default_resolver`

## 2. OpenSpec artifacts

- [x] Write `openspec/changes/ciandlithe-langfuse-prompt-mirror-v1/proposal.md` (DONE)
- [x] Write `openspec/changes/ciandlithe-langfuse-prompt-mirror-v1/tasks.md` (this file)
- [ ] Write `openspec/changes/ciandlithe-langfuse-prompt-mirror-v1/cross-repo-sync.md`
- [ ] Write `openspec/specs/ciandlithe-langfuse-prompt-mirror/spec.md` (the NEW canonical spec)
- [ ] Write `openspec/specs/ciandlithe-langfuse-prompt-mirror/AGENTS.md` (≤30 lines)
- [ ] Write `openspec/changes/ciandlithe-langfuse-prompt-mirror-v1/specs/ciandlithe-langfuse-prompt-mirror/spec.md` (the spec delta)
- [ ] Run `openspec validate ciandlithe-langfuse-prompt-mirror-v1 --strict`
- [ ] Run `openspec validate ciandlithe-langfuse-prompt-mirror --strict`
- [ ] Run `openspec validate --all --strict`

## 3. Smoke tests

- [ ] Add `tests/smoke/test_langfuse_resolver_ciandlithe.py`:
  - Test the ciandlithe mirror resolver has 15 canonical prompt names (not the cianchosaint 21)
  - Test `health_check()` returns `status: "not_configured"` when no creds
  - Test `register_inline_fallback()` + `resolve()` returns the inline fallback text

## 4. CI gates + commit

- [ ] Run `mise run openspec:validate-all`
- [ ] Run `mise run lint:license`
- [ ] Commit on `ciandlithe:main` with message: `feat(openspec): ciandlithe Langfuse prompt resolver mirror (parallel to cianchosaint)`

## 5. Follow-up openspec changes (NOT in this change's scope)

- [ ] `ciandlithe-blip-v1` — the BLIP v1 single umbrella
- [ ] `ciandlithe-blig-v1-spec-v1` — the BLIG v1 umbrella spec
- [ ] `ciandlithe-bipp-v2-crossref-v1` — the BIPP v2 cross-reference
- [ ] `ciandlithe-ragas-eval-v1` — the RAGAS eval pipeline

## Verification

```bash
cd /Users/cianmacandeisigh/dev/ciandlithe
openspec list --specs
# Expected: 2 specs (ciandlithe-pipeline + ciandlithe-langfuse-prompt-mirror)

openspec list
# Expected: 2 changes (ciandlithe-repo-foundation-v1 + ciandlithe-langfuse-prompt-mirror-v1)

openspec validate ciandlithe-langfuse-prompt-mirror-v1 --strict
# Expected: pass

openspec validate ciandlithe-langfuse-prompt-mirror --strict
# Expected: pass
```