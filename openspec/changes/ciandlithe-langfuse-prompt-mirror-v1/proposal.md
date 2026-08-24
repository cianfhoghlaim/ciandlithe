# Change: ciandlithe-langfuse-prompt-mirror-v1

## Why

Two problems converged on 2026-08-24:

1. **The ciandlithe platform has no Langfuse prompt management** — parallel to cianchosaint. The ciandlithe composite pilot + the per-cohort BAML extraction functions (ExtractCompositePilotDossier, ExtractCourtForm, ExtractJudgement, etc.) all hardcode their prompts inline in the .baml file. There is no versioning, no A/B testing, no per-extraction score reporting. This blocks the ciandlithe-side Garda self-hosted prompt development workflow.

2. **The ciandlithe BAML extraction functions are a subset of the cianchosaint ones** — the 15 ciandlithe canonical prompt names are different from the 21 cianchosaint ones. We need a **mirror resolver** (not a wholesale-copy) that knows about the 15 ciandlithe-specific prompt names but shares the same circuit-breaker + graceful-fallback infrastructure as cianchosaint.

## What changes

- **NEW mirror module** at `baml_src/_shared/langfuse_prompt_resolver.py` (~150 LOC) — the ciandlithe-side `LangfusePromptResolver` with:
  - 15 canonical ciandlithe prompt names (per the ciandlithe BAML extraction functions)
  - Same circuit-breaker + graceful-fallback pattern as cianchosaint
  - Wholesale-copied from `cianchosaint/baml_src/_shared/langfuse_prompt_resolver.py` (renamed cianchosaint → ciandlithe; cianchosaint-specific prompt names → ciandlithe-specific ones)

- **NEW spec** `openspec/specs/ciandlithe-langfuse-prompt-mirror/spec.md` (~150 lines) — the mirror resolver spec
- **NEW openspec artifacts**:
  - `proposal.md` (this file)
  - `tasks.md`
  - `cross-repo-sync.md`
  - `specs/ciandlithe-langfuse-prompt-mirror/spec.md` (the spec delta)

## Impact

- Affected specs: **1 NEW spec** (`ciandlithe-langfuse-prompt-mirror`)
- Affected code/config: ciandlithe repo (1 NEW file + 4 NEW openspec artifacts)
- No secret values are written to disk: all keys resolve via `infisical://dev-baile/ciandlithe/langfuse/{public,secret}-key` template refs hydrated by mise + Locket.
- The cianchosaint + cianfhoghlaim repos are unaffected.

## Out of scope (follow-up changes)

- The ciandlithe BIPP v2 cross-reference (follow-up `ciandlithe-bipp-v2-crossref-v1`).
- The ciandlithe BLIG v1 umbrella spec (follow-up `ciandlithe-blig-v1-spec-v1`).
- The ciandlithe RAGAS eval pipeline (follow-up `ciandlithe-ragas-eval-v1`).
- Retrofitting the existing inline ciandlithe BAML prompts to use the resolver.

## Dependencies

`Blocked by: none.`
`Blocked by (soft): cianchosaint/cianchosaint@cianchosaint-langfuse-prompt-management-v1` (the upstream that defines the canonical pattern).
`Affected repos: ciandlithe.`

## Cross-repo sync

This change is the **mirror** of `cianchosaint-langfuse-prompt-management-v1`. Per the cross-repo-sync convention:
- cianfhoghlaim — no changes
- ciandlithe — commits first (this change)
- cianchosaint — commits second (the canonical upstream)

## Verification

```bash
cd /Users/cianmacandeisigh/dev/ciandlithe
openspec validate ciandlithe-langfuse-prompt-mirror-v1 --strict
# Expected: Validation passes

python3 -c "
from baml_src._shared.langfuse_prompt_resolver import get_default_resolver
r = get_default_resolver()
print(r.health_check())
"
# Expected: status: 'not_configured' (no Langfuse creds in CI)

python3 -c "
from baml_src._shared.langfuse_prompt_resolver import LangfusePromptResolver
names = LangfusePromptResolver.canonical_prompt_names()
print(f'Canonical ciandlithe prompt names: {len(names)}')
"
# Expected: Canonical ciandlithe prompt names: 15
```