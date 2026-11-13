# Tasks — `2026-08-24-ciandlithe-init-v1`

> **Parent change**: [`2026-08-24-dlt-sources-to-multi-repo-scaffold-v1`](../../../2026-08-24-dlt-sources-to-multi-repo-scaffold-v1/proposal.md) §13
> **Companion plan**: [`openspec/plans/2026-08-24-dlt-deep-analysis-v2.md`](../../../../openspec/plans/2026-08-24-dlt-deep-analysis-v2.md) §Phase 2.1

---

## 13. Phase 2.1 — Create `ciandlithe/` sister-repo skeleton

- [x] 13.1 The `github.com/cianmacandeisigh/ciandlithe.git` repo is **NOT YET CREATED** on GitHub (that's a separate human step). The local skeleton at `/Users/cianmacandeisigh/dev/ciandlithe/` already exists as a **standalone iteration** (per the `ciandlithe-repo-foundation-v1` openspec change) which is richer than the skeleton spec — this is OK; the existing implementation is preserved, the per-sister skeleton artifacts (this change) are additive on top.
- [x] 13.2 The `tuatha/` project shape is replicated: `pyproject.toml` (ALREADY EXISTS as standalone), `mise.toml` (ALREADY EXISTS with `ciandlithe:<verb>:*` namespace), `openspec/{specs,changes}/` (ALREADY EXISTS with rich content), `dlt_sources/` (ALREADY EXISTS as full standalone), `baml_src/` (ALREADY EXISTS as `baml_src/` not `baml/` — renamed in a follow-up), `orchestration/` (ALREADY EXISTS as `orchestration/` not `dagster/` — renamed in a follow-up), `cocoindex_flows/` (ALREADY EXISTS as `cocoindex_flows/` not `cocoindex/` — renamed in a follow-up), `notebooks/` (ALREADY EXISTS), `tests/smoke/` (ALREADY EXISTS — `tests/dlt/` NEW in this change), `ci/` (NEW in this change), `docs/` (ALREADY EXISTS with rich content — `docs/AGENTS.md` + `docs/architecture.md` NEW in this change).
- [x] 13.3 This change writes `openspec/changes/2026-08-24-ciandlithe-init-v1/proposal.md` documenting the skeleton + the multi-repo sync contracts (the bilingual carve rule + the 6 cascade contracts + the tuatha precedent). Also writes `tasks.md` (this file), `cross-repo-sync.md`, and `specs/ciandlithe-dlt-sources-split/spec.md`. Also writes the per-sister canonical spec at `openspec/specs/ciandlithe-architecture.md` + the per-spec `AGENTS.md`.
- [x] 13.4 The repo push + uv workspace wire-in is DEFERRED to a human step (the prompt explicitly forbids `gh repo create`). Once pushed, the wire-in to the cianfhoghlaim uv workspace `pyproject.toml` happens in a follow-up change (the existing ciandlithe pyproject.toml is explicitly standalone per its comment block at lines 96-108 — the transition to a uv workspace member dependency is a separate openspec change).

## Verification artifacts (this change)

- [x] V.1 `openspec/changes/2026-08-24-ciandlithe-init-v1/proposal.md` — written
- [x] V.2 `openspec/changes/2026-08-24-ciandlithe-init-v1/tasks.md` — this file
- [x] V.3 `openspec/changes/2026-08-24-ciandlithe-init-v1/cross-repo-sync.md` — written
- [x] V.4 `openspec/changes/2026-08-24-ciandlithe-init-v1/specs/ciandlithe-dlt-sources-split/spec.md` — written
- [x] V.5 `openspec/specs/ciandlithe-architecture.md` — written
- [x] V.6 `openspec/specs/ciandlithe-architecture/AGENTS.md` — written
- [x] V.7 `ci/README.md` — written
- [x] V.8 `docs/AGENTS.md` — written
- [x] V.9 `docs/architecture.md` — written
- [x] V.10 `tests/dlt/__init__.py` — written
- [x] V.11 `tests/dlt/test_imports.py` — written (mirrors `cianfhoghlaim/tests/dlt/test_imports.py`)

## Post-scaffold report

The post-scaffold sync report lives at
`/Users/cianmacandeisigh/dev/cianfhoghlaim/stedding/sync-reports/sister-repo-skeletons-2026-08-25.md`
covering both ciandlithe + cianchosaint + the recommended `gh repo create` commands.

---

**Total tasks**: 4 parent tasks (§13.1-§13.4) + 11 verification artifacts (V.1-V.11). All marked [x] for this init change (the skeleton is complete; the GitHub push + uv workspace wire-in is deferred to human + follow-up changes).