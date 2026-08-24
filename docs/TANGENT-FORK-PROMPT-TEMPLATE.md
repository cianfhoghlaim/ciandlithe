# CIANDLITHE — Tangent Fork Prompt Template

> **For:** Anyone who wants to fork `cianfhoghlaim/cianfhoghlaim` or `cianfhoghlaim/cianchosaint` or `cianfhoghlaim/ciandlithe` (or any similar baseline) into a domain-specific tangent using their own generative AI.

> **Source for the meta-prompt shape:** Per the cianfhoghlaim/cianfhoghlaim README: *"Use my notes as a blueprint for your own deep-research tangent."*

> **Companion docs:** README.md · AGENTS.md · LICENSE.md · docs/USAGE-GUIDELINES.md · docs/HOW-BRITISH-ISLES-LITIGATION-ENTITIES-USE-CIANDLITHE.md · docs/DEMO-PATHS.md · docs/DEPLOYMENT.md · docs/case-study/composite-pilot.md · docs/source-catalogue/blip-v1-sources.md

## §1 — Why this document exists

The `cianfhoghlaim/ciandlithe` platform is a **new iteration of the cianfhoghlaim/cianfhoghlaim + cianfhoghlaim/cianchosaint projects**. The original Cianfhoghlaim is the British-Isles education corpus platform (8 jurisdictions × 5 stages × bilingual Goidelic + Brythonnic + 3.4 GB leabharlann source materials). Cianchosaint was created by **tangenting** Cianfhoghlaim into a domain-specific focus on **defence / policing / intelligence oversight** — same opensource stack (DLT + BAML + CocoIndex + Dagster + LanceDB + MotherDuck + Komodo + Pangolin + LiteLLM + TanStack Start + Convex + AG-UI + CopilotKit), different domain verticals (BIPP v1 / BIDP v1 / BIIP v1), different BAML schemas, different DLT sources, different licence posture. Ciandlithe was created by **further tangenting** Cianfhoghlaim + Cianchosaint into a domain-specific focus on **civil litigation / medical malpractice** — same opensource stack, single umbrella BLIP v1, 7 cohorts × 6-8 jurisdictions, 7 per-persona web apps, BUSL-1.1 v2 CIANDLITHE licence with Person-of-Interest clause + no-automated-form-submission constraint.

This document provides the **meta-prompt template** for authoring YOUR OWN domain-specific tangent. Whether you want to fork Cianfhoghlaim, Cianchosaint, Ciandlithe, or any similar baseline (e.g. for medical / legal / financial / environmental / public health / regulatory domains), the meta-prompt gives you the 8-step structure + the structured templates + the worked examples you need.

## §2 — The original Cianfhoghlaim setup (the baseline)

Before you fork, understand the original setup.

### §2.1 — What Cianfhoghlaim is

`Cianfhoghlaim` = Irish Gaelic "cian" (long/far/longing) + "fhoghlaim" (learning). British-Isles education corpus platform.

### §2.2 — The 7 major components

| Component | Path | What it does |
|---|---|---|
| `leabharlann` (external repo) | github.com/cianfhoghlaim/leabharlann | The source materials that informed every sub-agent + BAML schema + CocoIndex flow |
| `bonneagar` (in-repo) | `bonneagar/` | The 99 Docker Compose stacks + the deployment runbooks |
| `baml_src` (in-repo) | `baml_src/` | The BAML extraction functions + schemas |
| `dlt_sources` (in-repo) | `dlt_sources/` | The DLT source files + per-constituency manifest |
| `cocoindex_flows` (in-repo) | `cocoindex_flows/` | The CocoIndex v1 Apps |
| `agents` (in-repo) | `agents/` | The agent fleet |
| `openspec` (in-repo) | `openspec/` | The canonical specs + archived openspec changes |

### §2.3 — The wholesale-copy pattern (from Cianfhoghlaim → Cianchosaint → Ciandlithe)

**WHOLESALE-COPY VERBATIM** (with namespace renames):

- dlt_sources/_cross/ + dlt_sources/common/ (the shared helpers)
- cocoindex_flows/_shared/ (the 7 shared helpers)
- agents/adk/ (the Google ADK framework)
- agents/meaisinfhoghlaim/firecrawl_mcp/ (the browser tool client)
- baml_src/clients.baml + baml_src/_shared/ (the 4-tier provider chain)
- web/packages/{ui-kit,auth,db}/ (the 3 shared web packages)
- bonneagar/stacks/ (the 13 compose stacks)
- .agents/skills/ (the ~68 SKILL.md files)
- the openspec/ workflow (AGENTS.md + change artifacts pattern)

**DO NOT WHOLESALE-COPY** (these are domain-specific, must be replaced):

- The 9 Irish law DLT sources (replace with YOUR domain DLT sources)
- The 4 Ireland/medicine DLT sources (replace with YOUR domain medicine DLT sources)
- The 4 legislation.py stubs (replace with YOUR domain per-sub-nation legislation DLT sources)
- The 6 Ireland/law BAML files (replace with YOUR domain BAML schemas)
- The 14 cocoindex flows (replace with YOUR domain flows)
- The 7 per-persona web apps (replace with YOUR personas)
- The canonical specs (rename to your-domain-*)
- The Reform UK pilot (replace with YOUR case study)

### §2.4 — The 14 knowledge sync layers

Per the Cianfhoghlaim knowledge-sync-loop spec:

1. **paths
2. **ccc** (CocoIndex Code)
3. **cognee** (knowledge graph)
4. **skills** (agent skill validation)
5. **mcp** (Model Context Protocol server inventory)
6. **drift-docs** (AGENTS.md number claim validation)
7. **baml** (BAML extraction schema validation)
8. **openspec** (change + canonical spec validation)
9. **dlt** (DLT source URL allowlist + British-Isles body check)
10. **cocoindex-flows** (CocoIndex flow validation)
11. **agents** (agent fleet registry validation)
12. **lint** (openspec + licence + drift + skills validation)
13. **deploy** (IaC stack validation)
14. **test** (smoke test suite validation)

### §2.5 — The 5 dispatchable opencode subagents

Per the Cianfhoghlaim opencode.json (adopted into all 3 repos):

1. **data-platform**
2. **infrastructure**
3. **agent-platform**
4. **frontend-apps**
5. **research**

## §3 — The meta-prompt template

Copy-paste the following prompt into a fresh gen AI session to fork Cianfhoghlaim / Cianchosaint / Ciandlithe into your domain-specific tangent.

```markdown
# Meta-prompt: How to fork [CIANFHOGHLAIM | CIANCHOSAINT | CIANDLITHE] into a domain-specific tangent

## Goal
Build a new sibling repo `github.com/<your-org>/<your-repo>` that inherits the opensource stack (DLT + BAML + CocoIndex + Dagster + LanceDB + MotherDuck + Komodo + Pangolin + LiteLLM + TanStack Start + Convex + AG-UI + CopilotKit) but targets a different domain vertical.

## Step 1 — Pick your domain + your canonical pilot

Choose a domain vertical that's underserved by proprietary AI vendors. Examples:
- Public-health (NHS vs LexisNexis for clinical-trial data)
- Local-government (data.gov.uk + council budgets vs Westlaw for planning law)
- Veterinary medicine (DEFRA + Royal College of Veterinary Surgeons vs proprietary databases)
- Tenancy law (Tenant.ie + Property Tribunal decisions vs proprietary legal databases)

For each domain, identify ONE canonical pilot case study (single entity, allowlist-bounded, narrow scope). For cianchosaint the pilot was Richard Tice + Reform UK. For ciandlithe the pilot is the composite of 7 case studies (QUB/RVH brain-injury, Eric employer/breach, Garda data-access, DkIT/NUIG education, UCL admission, sodium valproate/HSE misprescription).

## Step 2 — Identify your canonical sources

For each pilot party, identify the canonical sources:
- Official government websites (statute books, court service portals, regulator press releases)
- Leabharlann-equivalent (your own `leabharlann_<domain>/` repo containing ~50-100 Gemini Deep Research outputs)
- Private case-study evidence (gitignored; lives in a separate `stedding/private_case_evidence/` volume)

## Step 3 — Adopt the 14-layer knowledge sync loop + the 5 opencode subagents + the openspec workflow

The wholesale-copy pattern is identical:
- `openspec/AGENTS.md` + `openspec/specs/<your-pipeline>/{spec.md,AGENTS.md}` + `openspec/changes/<your-foundation>/{proposal.md,tasks.md,cross-repo-sync.md,specs/...}`
- `.agents/skills/` (wholesale-copy the 68 SKILL.md files)
- `opencode.json` + `.mcp.json` (wholesale-copy)
- `.cocoindex_code/{settings.yml,guides.yml}` (wholesale-copy + customise guides)

## Step 4 — Choose your licence posture

The licence is the load-bearing architectural constraint. Three options:

1. **BUSL-1.1 broader cultural grant** (like Cianfhoghlaim) — open to all civil-society use
2. **BUSL-1.1 v2 British-Isles-only OSINT with warrant-to-enforce** (like Cianchosaint) — restricted to named public-sector bodies
3. **BUSL-1.1 v2 with extra clauses** (like Ciandlithe) — adds PoI clause + no-auto-submit constraint

## Step 5 — Build the 4-tier provider chain

The 4-tier provider chain is the load-bearing Python module at `baml_src/_shared/provider_router.py`. Wholesale-copy verbatim + change the `LITELLM_BASE_URL` default to your domain.

## Step 6 — Write your umbrella pipeline spec

Mirrors `openspec/specs/ciandlithe-pipeline/spec.md`:
- Purpose (1 paragraph)
- Background (3 paragraphs)
- Requirements (8-12 requirements with 2-4 scenarios each)
- Cross-references

## Step 7 — Write your first openspec change

Mirrors `openspec/changes/ciandlithe-repo-foundation-v1/`:
- `proposal.md` (the 4-Why + the 8-What-changes + the 7-Impact + the 7-Out-of-scope + the 4-Dependencies + the 2-Cross-repo-sync)
- `tasks.md` (the 11-step checklist)
- `cross-repo-sync.md` (the commit order: source → source → destination)
- `specs/<your-pipeline>/spec.md` (the ADDED Requirements delta)

## Step 8 — Wholesale-migrate + run `openspec validate --all --strict` + commit

Run the wholesale-migration script (the standard cianchosaint bootstrap pattern). Run `openspec validate --all --strict` to confirm 100% pass. Commit on `main` with the canonical commit message: `feat(openspec): <your-repo> repo foundation + <your-pipeline> + BUSL-1.1 <your-edition> licence + <your-pilot> stub`.

## What you get out

A new repo with:
- Full feature parity with the parent (provider chain + orchestrator + deployment + licence + openspec workflow + knowledge sync loop + opencode subagents + Infisical vault + Lakehouse stack)
- A domain-specific umbrella pipeline (BLIP v1, BIPP v1 + BIDP v1 + BIIP v1, or your own)
- Per-persona web apps tailored to your domain's users
- A canonical pilot case study validating the workflow end-to-end
- The OSINT allowlist + the PoI clause + the no-auto-submit constraint (where applicable)
```

## §4 — The 3 sibling repos at-a-glance

| Repo | Domain | Licence | Verts | Personas | Pilot |
|---|---|---|---|---|---|
| `cianfhoghlaim/cianfhoghlaim` | Education | BUSL-1.1 (cultural) | 8 LC subjects | students / teachers / parents | NCCA LC |
| `cianfhoghlaim/cianchosaint` | Defence / policing / intel | BUSL-1.1 v2 (British-Isles OSINT) | BIPP v1 + BIDP v1 + BIIP v1 | 7 (Garda / PSNI / MET / MOD / Intel-oversight / NI-justice / Welsh-police) | Reform UK + Richard Tice |
| `cianfhoghlaim/ciandlithe` | Civil litigation / med-malpractice | BUSL-1.1 v2 CIANDLITHE (PoI + no-auto-submit) | BLIP v1 (single umbrella) | 7 (self-rep / WRC / HSE-NHS / PIAB / coroner / inquest / legal-aid) | Composite of 7 case studies |

All 3 repos share:
- The openspec workflow + the 14-layer knowledge sync loop + the 5 opencode subagents
- The Infisical `dev-baile` vault
- The Lakehouse stack (MotherDuck + LanceDB + DuckDB)
- The 4-tier provider chain (Unsloth Studio → LiteLLM → MiniMax → Gemini)

All 3 repos diverge on:
- Domain
- Licence posture
- Vertical pipeline structure
- Persona surfaces
- Canonical pilot

## §5 — Cross-references

- [Cianfhoghlaim README](https://github.com/cianfhoghlaim/cianfhoghlaim/blob/main/README.md) — the original baseline
- [Cianchosaint README](https://github.com/cianfhoghlaim/cianchosaint/blob/main/README.md) — the defence/policing/intel sibling
- [Ciandlithe README](../README.md) — the civil-litigation sibling
- [Cianchosaint docs/TANGENT-FORK-PROMPT-TEMPLATE.md](https://github.com/cianfhoghlaim/cianchosaint/blob/main/docs/TANGENT-FORK-PROMPT-TEMPLATE.md) — the original Cianchosaint template (mirrored by this doc)