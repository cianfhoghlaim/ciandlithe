# ciandlithe-langfuse-prompt-mirror — Agent Routing

| Spec | Path |
|:--|:--|
| spec.md | [./spec.md](./spec.md) |

## Quick orientation

`ciandlithe-langfuse-prompt-mirror` is the mirror Langfuse v3 prompt management capability for ciandlithe. It mirrors the cianchosaint `cianchosaint-langfuse-prompt-management` spec with 15 ciandlithe-specific canonical prompt names.

## Routing table

| I want to... | Look at... |
|:--|:--|
| Resolve a ciandlithe BAML prompt via Langfuse | `baml_src/_shared/langfuse_prompt_resolver.py:LangfusePromptResolver.resolve()` |
| List the 15 ciandlithe canonical prompt names | `LangfusePromptResolver.canonical_prompt_names()` |
| Health check the Langfuse connection | `python3 -c "from baml_src._shared.langfuse_prompt_resolver import get_default_resolver; print(get_default_resolver().health_check())"` |
| View the upstream pattern (cianchosaint) | `../cianchosaint/baml_src/_shared/langfuse_prompt_resolver.py` |

## Implementation order

See [`../../openspec/changes/ciandlithe-langfuse-prompt-mirror-v1/tasks.md`](../../openspec/changes/ciandlithe-langfuse-prompt-mirror-v1/tasks.md) §5 for the follow-up changes.