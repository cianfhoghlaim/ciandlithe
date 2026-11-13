# Cross-Repo Sync — `2026-08-24-ciandlithe-init-v1`

> **Per the openspec/AGENTS.md convention**: required for any change that touches >1 repo. This change touches ciandlithe (the primary) + references cianfhoghlaim + cianchosaint (read-only).

## Repos in scope

| Repo | Role | Operations |
|---|---|---|
| `ciandlithe` (`/Users/cianmacandeisigh/dev/ciandlithe/`) | Primary | WRITE — add skeleton artifacts (this change) |
| `cianfhoghlaim` (`/Users/cianmacandeisigh/dev/cianfhoghlaim/`) | Read-only reference | READ-ONLY — parent change `2026-08-24-dlt-sources-to-multi-repo-scaffold-v1` lives here; `JurisdictionPipelineBase` lives here at `dlt_sources/british_isles/_cross/` |
| `cianchosaint` (`/Users/cianmacandeisigh/dev/cianchosaint/`) | Sister reference | READ-ONLY — the parallel sister init change `2026-08-24-cianchosaint-init-v1` lives there; the same skeleton shape is mirrored |

## Commit plan

### ciandlithe (this repo)

| Order | Files | Commit message |
|---|---|---|
| 1 | `openspec/changes/2026-08-24-ciandlithe-init-v1/{proposal,tasks,cross-repo-sync}.md` + `specs/ciandlithe-dlt-sources-split/spec.md` | `openspec: 2026-08-24-ciandlithe-init-v1 — sister-repo skeleton init` |
| 2 | `openspec/specs/ciandlithe-architecture.md` + `openspec/specs/ciandlithe-architecture/AGENTS.md` | `openspec: add ciandlithe-architecture canonical spec` |
| 3 | `ci/README.md` | `docs: add ci/README.md — per-sister CI conventions` |
| 4 | `docs/AGENTS.md` + `docs/architecture.md` | `docs: add docs/AGENTS.md + docs/architecture.md` |
| 5 | `tests/dlt/__init__.py` + `tests/dlt/test_imports.py` | `tests: add tests/dlt/ — sister smoke test pattern` |

**NOTE:** This change LEAVES ALL FILES UNSTAGED per the prompt instruction. The human reviews + stages + commits per their preferred workflow.

### cianfhoghlaim (read-only)

- NO writes in this change.
- The parent change `2026-08-24-dlt-sources-to-multi-repo-scaffold-v1/tasks.md` §13.1-§13.4 is updated from [ ] to [x] by a separate sibling step in this same task group (§§13.1-13.4 + §§14.1-14.4).

### cianchosaint (read-only)

- NO writes in this change.
- The parallel sister init change `2026-08-24-cianchosaint-init-v1` is written by the sister step in this same task group.

## Branch + remote

| Repo | Branch | Remote | Push target |
|---|---|---|---|
| ciandlithe | `main` (existing local branch; no push yet) | NOT YET CONFIGURED (the `github.com/cianmacandeisigh/ciandlithe.git` remote does NOT exist yet) | HUMAN STEP — `gh repo create cianmacandeisigh/ciandlithe --public --description "..." --clone=false` (see sync-report for the exact command) |

## Order of operations

1. **First**: Write all ciandlithe artifacts (this change).
2. **In parallel**: Write all cianchosaint artifacts (the sister step).
3. **In parallel**: Write the post-scaffold sync report at `/Users/cianmacandeisigh/dev/cianfhoghlaim/stedding/sync-reports/sister-repo-skeletons-2026-08-25.md`.
4. **Last**: Update the parent change's tasks.md §13.1-13.4 + §14.1-14.4 from [ ] to [x].
5. **After this change is archived**: Human runs the recommended `gh repo create` commands (from the sync report) to push both repos to GitHub.

## Rollback

Full reversal: `git checkout -- .` + `rm -rf openspec/changes/2026-08-24-ciandlithe-init-v1/ openspec/specs/ciandlithe-architecture.md openspec/specs/ciandlithe-architecture/ ci/ docs/AGENTS.md docs/architecture.md tests/dlt/`.