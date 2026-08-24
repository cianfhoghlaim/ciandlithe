# Tasks: ciandlithe-repo-foundation-v1

## 0. Pre-flight

- [x] Verify the openspec CLI is installed: `openspec --version` (1.4.1 confirmed)
- [x] Verify the parent directory `/Users/cianmacandeisigh/dev/` exists and is writable
- [x] Verify the local git user is configured (cianmacliathain@gmail.com + cianfhoghlaim)

## 1. Repo skeleton (ciandlithe)

- [x] Create the new repo directory: `/Users/cianmacandeisigh/dev/ciandlithe`
- [x] Initialise git: `git init -b main` in the new repo
- [x] Configure git user: `git config user.email` + `git config user.name`
- [x] Move the existing private case-study evidence folders (dkit/, eric_case/, garda/, little_collins/, monroes/, nuig/, qub/, qub_royal_victoria_hospital_malpractice/, taafes/, ucl/) to `stedding/private_case_evidence/` (gitignored)
- [x] Write `.gitignore` (excludes pycache, node_modules, .env*, motherduck, lance, stedding/private_case_evidence)
- [x] Create the directory tree (mirrors cianchosaint's post-v7 layout, with ciandlithe-specific sub-dirs):
  ```
  ciandlithe/
  ├── AGENTS.md
  ├── README.md
  ├── LICENSE.md
  ├── pyproject.toml
  ├── mise.toml
  ├── package.json
  ├── .gitignore
  ├── .infisical.env
  ├── openspec/
  │   ├── AGENTS.md
  │   ├── specs/
  │   │   └── ciandlithe-pipeline/{spec.md,AGENTS.md}
  │   └── changes/
  │       ├── archive/
  │       └── ciandlithe-repo-foundation-v1/{proposal.md,tasks.md,cross-repo-sync.md,specs/ciandlithe-pipeline/spec.md}
  ├── dlt_sources/
  │   ├── _cross/
  │   ├── common/
  │   └── ciandlithe/{ireland,northern_ireland,scotland,wales,england,crown_dependencies,common,cross}/...
  ├── baml_src/
  │   ├── _shared/{provider_router.py,templates/}
  │   ├── clients.baml
  │   └── ciandlithe/{ireland/law,medicine,courts,case_studies,processing}/...
  ├── cocoindex_flows/{_shared,ciandlithe,infrastructure}/
  ├── orchestration/
  ├── agents/{ciandlithe/tools,meaisinfhoghlaim,adk}/
  ├── notebooks/
  ├── motherduck/
  ├── mise-tasks/
  ├── bonneagar/{stacks,iac,komodo,pangolin}/
  ├── docs/{governance,case-study,personas,research,source-catalogue}/
  └── web/{apps,packages,hono-api}/
  ```

## 2. Core documentation files

- [x] Write `LICENSE.md` — the BUSL-1.1 v2 CIANDLITHE edition with the Additional Use Grant, the 3-step foreign-use gate, the PoI clause, the no-auto-submit constraint, and the warrant-to-enforce clause
- [x] Write `AGENTS.md` — the canonical agent routing
- [x] Write `README.md` — concise project intro
- [x] Write `openspec/AGENTS.md` — the openspec workflow

## 3. OpenSpec artifacts

- [x] Write `openspec/specs/ciandlithe-pipeline/spec.md` — the umbrella capability spec
- [x] Write `openspec/specs/ciandlithe-pipeline/AGENTS.md` — sibling AGENTS.md per the repo-hygiene convention
- [x] Write `openspec/changes/ciandlithe-repo-foundation-v1/proposal.md` (DONE)
- [x] Write `openspec/changes/ciandlithe-repo-foundation-v1/tasks.md` (this file)
- [ ] Write `openspec/changes/ciandlithe-repo-foundation-v1/cross-repo-sync.md`
- [ ] Write `openspec/changes/ciandlithe-repo-foundation-v1/specs/ciandlithe-pipeline/spec.md` (the spec delta)
- [ ] Run `openspec validate ciandlithe-repo-foundation-v1 --strict` and verify exit code 0
- [ ] Run `openspec validate ciandlithe-pipeline --strict` and verify exit code 0

## 4. Minimal config files

- [ ] Write `pyproject.toml` (mirror cianfhoghlaim + cianchosaint's `pyproject.toml` skeleton — single Python package `ciandlithe`)
- [ ] Write `mise.toml` (canonical 9-namespace task catalogue, with `ciandlithe:` namespace stubs)
- [ ] Write `package.json` (bun workspace, mirror cianchosaint's)
- [ ] Write `.infisical.env` (template with `infisical://dev-baile/ciandlithe/...` references)

## 5. Cross-repo preparation (cianfhoghlaim side)

- [ ] Author the cianfhoghlaim openspec change `official-law-pipeline-migration-to-ciandlithe-v1/`:
  - `proposal.md` declaring the assets to be migrated (Ireland/medicine + England/Scotland/Wales/NI legislation.py stubs + the helpers)
  - `tasks.md` listing the deprecation markers to add to each asset
  - `cross-repo-sync.md` declaring cianfhoghlaim-first ordering

## 5b. Cross-repo preparation (cianchosaint side)

- [ ] Author the cianchosaint openspec change `cianchosaint-ireland-law-migration-to-ciandlithe-v1/`:
  - `proposal.md` declaring the 9 Ireland/law DLT sources + 6 Ireland/law BAML files + the 4-tier provider chain + the deployment pattern to be migrated
  - `tasks.md` listing the deprecation markers to add to each asset
  - `cross-repo-sync.md` declaring cianchosaint-second ordering

## 6. Wholesale migration (ciandlithe side)

- [ ] Migrate the 9 Ireland/law DLT sources from cianchosaint:
  1. `cianchosaint/dlt_sources/cianchosaint/ireland/law/irish_statute_book.py` → `ciandlithe/dlt_sources/ciandlithe/ireland/law/irish_statute_book.py`
  2. ... (8 more)
- [ ] Migrate the 6 Ireland/law BAML files from cianchosaint
- [ ] Migrate the 4 Ireland/medicine DLT sources from cianfhoghlaim
- [ ] Migrate the 3 NHS DLT sources from cianfhoghlaim
- [ ] Migrate the 4 legislation.py stubs from cianfhoghlaim
- [ ] Migrate the `baml_src/clients.baml` 4-tier chain from cianchosaint
- [ ] Migrate the `baml_src/_shared/` templates from cianchosaint
- [ ] Migrate the 13 compose stacks from cianchosaint/bonneagar/stacks/
- [ ] Migrate the 3 shared web packages from cianchosaint/web/packages/
- [ ] Migrate the opencode.json + .mcp.json from cianfhoghlaim
- [ ] Rewrite imports in each migrated file (the cross-namespace rewrite)
- [ ] Add a LICENCE attribution header to each migrated file

## 7. OSINT allowlist + cross/ helpers

- [ ] Write `dlt_sources/ciandlithe/common/osint_allowlist.yaml` (the law + medicine-only allowlist)
- [ ] Write `dlt_sources/ciandlithe/cross/case_study_loader.py` (loads leabharlann PDFs by case-ID; read-only context)
- [ ] Write `dlt_sources/ciandlithe/cross/case_party_registry.py` (registry of the 7 composite-pilot parties)
- [ ] Write `dlt_sources/ciandlithe/cross/complaint_classifier.py` (maps uploaded complaint → cohort + jurisdiction)

## 8. Composite pilot stub

- [ ] Write `agents/ciandlithe/tools/composite_pilot.py` (the FunctionTool; mirrors `cianchosaint/tools/reform_uk_pilot.py`)
- [ ] Write `baml_src/ciandlithe/case_studies/reform_civil_suit_dossier.baml` (the BAML schema + extraction function)
- [ ] Write `docs/case-study/composite-pilot.md` (the canonical narrative)
- [ ] Write 6 more per-cohort FunctionTool stubs (medical_malpractice, employer_breach, garda_discrimination, education_discrimination, admission_breach, civil_action_outline)

## 9. CI gates + commit

- [ ] Run `openspec validate ciandlithe-repo-foundation-v1 --strict` and verify exit code 0
- [ ] Run `openspec validate ciandlithe-pipeline --strict` and verify exit code 0
- [ ] Run `openspec validate --all --strict` (no further changes expected)
- [ ] Commit on `ciandlithe:main` with message: `feat(openspec): ciandlithe repo foundation + BLIP v1 + BUSL-1.1 v2 CIANDLITHE licence + composite pilot stub`

## 10. Follow-up openspec changes (NOT in this change's scope)

- [ ] `ciandlithe-provider-router-v1` — implements the 4-tier chain
- [ ] `ciandlithe-baml-schemas-v1` — the 22 BAML extraction functions (8 wholesale + 14 NEW)
- [ ] `ciandlithe-blip-v1` — the BLIP v1 single umbrella + the 50 cohort DLT sources
- [ ] `ciandlithe-cocoindex-flows-v1` — the 14 CocoIndex flows + RAGAS faithfulness gate
- [ ] `ciandlithe-orchestration-v1` — the Dagster defs + asset checks + milestone gates m1 / m2 / m3
- [ ] `ciandlithe-per-persona-web-surfaces-v1` — the 7 per-persona TanStack Start + Convex + AG-UI + CopilotKit apps
- [ ] `ciandlithe-composite-pilot-workflow-v1` — the 7 FunctionTools + 7 BAML extractions + 7 cross-referenced dossiers
- [ ] `ciandlithe-pangolin-ingress-v1` — Pangolin ingress for Unsloth Studio + the 7 web apps
- [ ] `ciandlithe-licence-enforcement-v1` — operationalises the warrant-to-enforce clause
- [ ] `litellm-to-unsloth-provider-chain-v1` (cianfhoghlaim side) — retrofit the 4-tier chain

## Verification

```bash
cd /Users/cianmacandeisigh/dev/ciandlithe
openspec list --specs
# Expected: 1 spec (ciandlithe-pipeline)

openspec list
# Expected: 1 change (ciandlithe-repo-foundation-v1)

openspec validate ciandlithe-repo-foundation-v1 --strict
# Expected: Validation passes

openspec validate ciandlithe-pipeline --strict
# Expected: Validation passes
```