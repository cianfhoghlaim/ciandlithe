# Cross-Repo Sync: ciandlithe-repo-foundation-v1

This change touches **3 repos**: `cianfhoghlaim/cianfhoghlaim` (the source — supplies the helpers + Ireland/medicine + legislation.py stubs + NHS DLT sources + opencode.json + .mcp.json + .agents/skills/ + .cocoindex_code/), `cianchosaint/cianchosaint` (the source — supplies the 9 Ireland/law DLT sources + 6 Ireland/law BAML files + the 4-tier provider chain + the deployment runbook + the 13 compose stacks + the 3 shared web packages + the openspec workflow pattern), and `ciandlithe/ciandlithe` (the destination — receives them).

They MUST be committed in this order:

## Order of Operations

```
[1] cianfhoghlaim  → openspec/changes/official-law-pipeline-migration-to-ciandlithe-v1/
                      (proposal + tasks + 1 spec delta for official-law-pipeline)
                      Declares the Ireland/medicine + NHS DLT sources + legislation.py stubs + helpers
                      as pending-migration to ciandlithe.
                      Pushed to main.
                           ↓
[2] cianchosaint   → openspec/changes/cianchosaint-ireland-law-migration-to-ciandlithe-v1/
                      (proposal + tasks + cross-repo-sync + 1 spec delta for cianchosaint-pipeline)
                      Declares the 9 Ireland/law DLT sources + 6 Ireland/law BAML files + the 4-tier provider chain
                      + the deployment pattern as pending-migration to ciandlithe.
                      Pushed to main.
                           ↓
[3] ciandlithe     → openspec/changes/ciandlithe-repo-foundation-v1/
                      (proposal + tasks + cross-repo-sync + 1 spec delta for ciandlithe-pipeline)
                      Receives the migrated assets via cp/rewrite from cianfhoghlaim + cianchosaint.
                      Pushed to main.
                           ↓
[4] operator       → cd ciandlithe && openspec validate ciandlithe-repo-foundation-v1 --strict
                      → cd cianchosaint && openspec validate cianchosaint-ireland-law-migration-to-ciandlithe-v1 --strict
                      → cd cianfhoghlaim && openspec validate official-law-pipeline-migration-to-ciandlithe-v1 --strict
                      → All validations pass
                           ↓
[5] operator       → openspec archive ciandlithe-repo-foundation-v1 --yes (in ciandlithe)
                      → openspec archive cianchosaint-ireland-law-migration-to-ciandlithe-v1 --yes (in cianchosaint)
                      → openspec archive official-law-pipeline-migration-to-ciandlithe-v1 --yes (in cianfhoghlaim)
                      → All changes archive
                           ↓
[6] follow-ups     → The 9 follow-up openspec changes (ciandlithe-provider-router-v1, etc.)
                      may begin, each with their own cross-repo-sync.md where applicable
```

## Repo 1: cianfhoghlaim/cianfhoghlaim (source — first)

**Files to commit** (under `openspec/changes/official-law-pipeline-migration-to-ciandlithe-v1/`):

- `proposal.md` (with `## Dependencies` + `## Cross-repo sync` sections)
- `tasks.md`
- `specs/official-law-pipeline/spec.md` (delta — marks the law + medicine assets as deprecated-pending-migration)
- `cross-repo-sync.md`

**Files marked as deprecated-pending-migration** (NOT moved, just annotated):

- `dlt_sources/medicine/ireland/british_isles/{doh,hpsc,hse,medical_council}.py` — annotation header added
- `dlt_sources/medicine/england/british_isles/{gmc,nhs_england,nice}.py` — annotation header added
- `dlt_sources/medicine/scotland/british_isles/nhs_scotland.py` — annotation header added
- `dlt_sources/medicine/wales/british_isles/nhs_wales.py` — annotation header added
- `dlt_sources/medicine/northern_ireland/british_isles/nidirect.py` — annotation header added
- `dlt_sources/law/{england,scotland,wales,northern_ireland}/british_isles/legislation.py` — annotation header added
- The `dlt_sources/_cross/`, `dlt_sources/common/`, `cocoindex_flows/_shared/`, `agents/adk/`, `agents/meaisinfhoghlaim/firecrawl_mcp/`, `.agents/skills/`, `.cocoindex_code/`, `opencode.json`, `.mcp.json` — annotation header added (the wholesale-migration is read-only for cianfhoghlaim — it just marks the assets as the canonical source)

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/cianfhoghlaim`

**Commit message**: `feat(openspec): mark law + medicine assets as pending-migration to ciandlithe`

**Why this is first**: Cianfhoghlaim needs to declare "these assets are being migrated" BEFORE cianchosaint + ciandlithe receive them. This avoids the "undocumented behavior" failure mode where ciandlithe consumes assets that cianfhoghlaim hasn't yet marked as out-of-scope.

## Repo 2: cianchosaint/cianchosaint (source — second)

**Files to commit** (under `openspec/changes/cianchosaint-ireland-law-migration-to-ciandlithe-v1/`):

- `proposal.md`
- `tasks.md`
- `specs/cianchosaint-pipeline/spec.md` (delta — marks the Ireland/law assets as pending-migration)
- `cross-repo-sync.md`

**Files marked as deprecated-pending-migration**:

- `dlt_sources/cianchosaint/ireland/law/{irish_statute_book,courts_ie,doj,courtsinformation,injuries_ie,lawreform,workplace_relations,citizensinformation,gov_ie_law}.py` — annotation header added
- `baml_src/cianchosaint/ireland/law/{courts,court_rules,judgements,piab,legal_aid,shared_legal_enums}.baml` — annotation header added
- `baml_src/clients.baml`, `baml_src/_shared/provider_router.py`, `baml_src/_shared/templates/*.baml` — annotation header added
- `bonneagar/stacks/{infisical,motherduck,lakehouse,litellm,unsloth-serve,langfuse,crawl4ai,stagehand,changedetection,komodo,pangolin,locket,traefik}/` — annotation header added (the wholesale-migration is read-only for cianchosaint)
- `web/packages/{ui-kit,auth,db}/` — annotation header added
- `openspec/AGENTS.md` (the openspec workflow) — annotation header added

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/cianchosaint`

**Commit message**: `feat(openspec): mark Ireland/law + provider-chain + deployment assets as pending-migration to ciandlithe`

**Why this is second**: Cianchosaint commits AFTER cianfhoghlaim (so the lineage is cianfhoghlaim → cianchosaint → ciandlithe). It declares "these assets are being migrated" BEFORE ciandlithe receives them.

## Repo 3: ciandlithe/ciandlithe (destination — last)

**Files to commit** (in the new repo):

- `AGENTS.md`, `README.md`, `LICENSE.md`
- `.gitignore`, `.infisical.env`
- `pyproject.toml`, `mise.toml`, `package.json`
- `openspec/AGENTS.md`
- `openspec/specs/ciandlithe-pipeline/spec.md`
- `openspec/specs/ciandlithe-pipeline/AGENTS.md`
- `openspec/changes/ciandlithe-repo-foundation-v1/{proposal.md,tasks.md,cross-repo-sync.md,specs/ciandlithe-pipeline/spec.md}` (this change's artifacts)
- ~30 wholesale-migrated DLT sources + BAML files + cocoindex flows + compose stacks + web packages + opencode.json + .mcp.json + .agents/skills/ + .cocoindex_code/
- The 7 composite-pilot FunctionTool stubs + BAML extraction + case-study doc
- The OSINT allowlist + the cross/ helpers

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/ciandlithe` (NEW repo)

**Commit message**: `feat(openspec): ciandlithe repo foundation + BLIP v1 + BUSL-1.1 v2 CIANDLITHE licence + composite pilot stub`

**Why this is last**: Ciandlithe receives the migrated assets AFTER both upstream repos have declared them as pending-migration. The wholesale-migration is "read-only" for cianfhoghlaim + cianchosaint (they keep their own copies; ciandlithe gets its own copies with namespace renames).

## Branch + push order summary

| Step | Repo | Branch | Push target | Commit message |
|---|---|---|---|---|
| 1 | cianfhoghlaim | main | github.com/cianfhoghlaim/cianfhoghlaim | feat(openspec): mark law + medicine assets as pending-migration to ciandlithe |
| 2 | cianchosaint | main | github.com/cianfhoghlaim/cianchosaint | feat(openspec): mark Ireland/law + provider-chain + deployment assets as pending-migration to ciandlithe |
| 3 | ciandlithe | main | github.com/cianfhoghlaim/ciandlithe | feat(openspec): ciandlithe repo foundation + BLIP v1 + BUSL-1.1 v2 CIANDLITHE licence + composite pilot stub |

## Verification

After step 3, the operator runs (in ciandlithe):

```bash
openspec list --specs            # Expected: 1 spec (ciandlithe-pipeline)
openspec list                    # Expected: 1 change (ciandlithe-repo-foundation-v1)
openspec validate ciandlithe-repo-foundation-v1 --strict   # Expected: pass
openspec validate ciandlithe-pipeline --strict             # Expected: pass
```

The cianfhoghlaim + cianchosaint changes validate independently in their own repos.

## Post-archive

Once all 3 changes are archived (per step 5 above), the 9 follow-up changes (§17 of the openspec/changes/ciandlithe-repo-foundation-v1/proposal.md) may begin, each with their own cross-repo-sync.md where applicable.