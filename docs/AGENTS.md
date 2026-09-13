# `docs/` — Agent Quick Reference

> **Per the repo-hygiene-agent-routing spec**, every top-level directory in ciandlithe (or any sister repo) MAY have its own AGENTS.md that documents the per-directory conventions. This file documents `docs/`.

## Routing

Load this AGENTS.md when:
- You are adding a new document under `docs/` (architecture.md, deployment.md, case-study/*.md, personas/*.md, governance/*.md, etc.)
- You are updating an existing document under `docs/` and need to know the per-doc conventions
- You are writing a new openspec change that references a docs/ file

## Conventions

1. **No emojis** in any document (per the user preference).
2. **1-page README convention** — each top-level doc (architecture.md, deployment.md, etc.) MUST be ≤1 page (≈ 200 lines or ≈ 600 words). Anything longer goes in a sub-directory (e.g. `case-study/`, `personas/`, `governance/`).
3. **Cross-references** — every doc MUST reference its parent spec via `[../openspec/specs/<spec-name>/spec.md](../openspec/specs/<spec-name>/spec.md)` + the canonical AGENTS.md via `[../AGENTS.md](../AGENTS.md)`.
4. **Number claims** — every number claim in `docs/` MUST be validated by `mise run lint:drift-docs` against the ground truth in `dlt_sources/`, `baml_src/`, `orchestration/`, etc.
5. **No code samples that don't run** — every code block in `docs/` MUST be a verified, working example. Use `mise run sync:dlt` + `mise run test:smoke` to validate.

## Sub-directories

| Sub-dir | Purpose |
|:--|:--|
| `architecture.md` | The 1-page architecture overview (per-sister canonical spec summary) |
| `case-study/` | The 7 leabharlann case-study PDFs + the composite-pilot verification |
| `configuration-surface.md` | The 14-domain configuration surface (the per-sister config grid) |
| `DEPLOYMENT.md` | The deployment guide |
| `governance/` | The per-sister governance docs (PR templates, code-review guidelines, etc.) |
| `personas/` | The per-persona web-app docs (one .md per persona) |
| `USAGE-GUIDELINES.md` | The OSINT ceiling + no-auto-submit constraint in operational terms |

## See also

- [`../AGENTS.md`](../AGENTS.md) — the canonical agent routing
- [`../openspec/specs/ciandlithe-architecture/spec.md`](../openspec/specs/ciandlithe-architecture/spec.md) — the per-sister canonical spec
- [`../openspec/AGENTS.md`](../openspec/AGENTS.md) — the per-repo openspec conventions