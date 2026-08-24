# Cross-Repo Sync: ciandlithe-langfuse-prompt-mirror-v1

This change touches **2 repos**: `cianchosaint/cianchosaint` (the source — defines the canonical pattern at `baml_src/_shared/langfuse_prompt_resolver.py`) and `ciandlithe/ciandlithe` (the destination — receives the mirror).

They MUST be committed in this order:

```
[1] cianchosaint   → openspec/changes/cianchosaint-langfuse-prompt-management-v1/
                      (proposal + tasks + cross-repo-sync + 1 spec delta for cianchosaint-langfuse-prompt-management)
                      Adds: baml_src/_shared/{langfuse_prompt_resolver,langfuse_client}.py + scripts/sync_langfuse_prompts.py
                      Pushed to main.
                           ↓
[2] ciandlithe     → openspec/changes/ciandlithe-langfuse-prompt-mirror-v1/
                      (proposal + tasks + cross-repo-sync + 1 spec delta for ciandlithe-langfuse-prompt-mirror)
                      Adds: baml_src/_shared/langfuse_prompt_resolver.py (mirror)
                      Pushed to main.
                           ↓
[3] operator       → cd cianchosaint && openspec validate cianchosaint-langfuse-prompt-management-v1 --strict
                      → cd ciandlithe && openspec validate ciandlithe-langfuse-prompt-mirror-v1 --strict
                      → Both validations pass
                           ↓
[4] operator       → openspec archive cianchosaint-langfuse-prompt-management-v1 --yes (in cianchosaint)
                      → openspec archive ciandlithe-langfuse-prompt-mirror-v1 --yes (in ciandlithe)
                      → Both changes archive
                           ↓
[5] follow-ups     → The 9 follow-up cianchosaint changes (BIPP v2 spec, BIPP v2 BAML, BIPP v2 DLT, RAGAS, Langfuse dashboard, Cognee+Graphiti, CopilotKit GenUI, Collab, Bilingual)
                      may begin. The ciandlithe follow-ups (BIPP v2 crossref, BLIG v1, RAGAS) may also begin.
```

## Repo 1: cianchosaint (upstream — first)

**Files to commit** (under `openspec/changes/cianchosaint-langfuse-prompt-management-v1/`):

- `proposal.md` (DONE)
- `tasks.md` (DONE)
- `cross-repo-sync.md` (DONE)
- `specs/cianchosaint-langfuse-prompt-management/spec.md` (delta)
- `openspec/specs/cianchosaint-langfuse-prompt-management/{spec.md, AGENTS.md}` (NEW canonical spec)

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/cianchosaint`

**Commit message**: `feat(openspec): Langfuse prompt management foundation + skill deepening wholesale-copy + ciandlithe mirror resolver`

**Why this is first**: Cianchosaint is the canonical upstream for the LangfusePromptResolver pattern. Ciandlithe mirrors.

## Repo 2: ciandlithe (mirror — second)

**Files to commit** (under `openspec/changes/ciandlithe-langfuse-prompt-mirror-v1/`):

- `proposal.md` (DONE)
- `tasks.md` (DONE)
- `cross-repo-sync.md` (this file)
- `specs/ciandlithe-langfuse-prompt-mirror/spec.md` (delta)
- `openspec/specs/ciandlithe-langfuse-prompt-mirror/{spec.md, AGENTS.md}` (NEW canonical spec)

**Files added**:

- `baml_src/_shared/langfuse_prompt_resolver.py` (the mirror)

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/ciandlithe`

**Commit message**: `feat(openspec): ciandlithe Langfuse prompt resolver mirror (parallel to cianchosaint)`

**Why this is second**: Ciandlithe mirrors but does not own. The canonical upstream is cianchosaint.

## Branch + push order summary

| Step | Repo | Branch | Push target | Commit message |
|---|---|---|---|---|
| 1 | cianchosaint | main | github.com/cianfhoghlaim/cianchosaint | `feat(openspec): Langfuse prompt management foundation + skill deepening wholesale-copy + ciandlithe mirror resolver` |
| 2 | ciandlithe | main | github.com/cianfhoghlaim/ciandlithe | `feat(openspec): ciandlithe Langfuse prompt resolver mirror (parallel to cianchosaint)` |

## Verification

After step 2, the operator runs (in ciandlithe):

```bash
openspec list --specs            # Expected: 2 specs (ciandlithe-pipeline + ciandlithe-langfuse-prompt-mirror)
openspec list                    # Expected: 2 changes (ciandlithe-repo-foundation-v1 + ciandlithe-langfuse-prompt-mirror-v1)
openspec validate ciandlithe-langfuse-prompt-mirror-v1 --strict   # Expected: pass
openspec validate ciandlithe-langfuse-prompt-mirror --strict        # Expected: pass
```

The cianchosaint change validates independently in its own repo.