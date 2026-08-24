# Change: ciandlithe-repo-foundation-v1

## Why

Four problems converged on 2026-08-24:

1. **The British-Isles civil-litigation ecosystem has no open-source OSINT platform equivalent to cianfhoghlaim/cianfhoghlaim or cianfhoghlaim/cianchosaint.** Every British-Isles sub-nation (Republic of Ireland, the 4 UK nations, the 3 Crown Dependencies) currently operates its own bespoke litigation toolkit (e.g. PIAB, NHS Resolution, NICTS) — or relies on proprietary AI vendors at £30k+/year (LexisNexis, Westlaw). There is no shared, auditable, sovereign-capability stack for self-representing claimants, WRC claimants, HSE/NHS complainants, PIAB applicants, inquest parties, coroner's-court applicants, or legal-aid applicants.

2. **The existing partial pipelines in cianfhoghlaim + cianchosaint already cover law + medicine wholesale-migratable assets.** 9 Ireland/law DLT sources in cianchosaint + 4 Ireland/medicine DLT sources in cianfhoghlaim + 3 NHS DLT sources in cianfhoghlaim + 4 legislation.py stubs in cianfhoghlaim + 6 Ireland/law BAML files in cianchosaint + the entire cianchosaint infrastructure (provider chain + licence + deployment) can be wholesale-migrated to ciandlithe with namespace renames. This is the standard cianchosaint wholesale-copy pattern (per `docs/TANGENT-FORK-PROMPT-TEMPLATE.md §2.3`).

3. **The leabharlann `gemini_deep_research/law/` + `gemini_deep_research/medical/` directories (~60+ PDFs, ~5 MB total)** are the canonical source-of-truth for every entity + event + jurisdiction the user has case-study material on. These are read-only context for the BAML extractions. The raw evidence folders at `stedding/private_case_evidence/` (dkit/ eric_case/ garda/ nuig/ qub/ ucl/ taafes/ monroes/ little_collins/ qub_royal_victoria_hospital_malpractice/) are NOT in the open repo (they are gitignored per `.gitignore`); they stay in the private stedding volume and are referenced by case-ID only.

4. **The composite pilot exercises all 7 cohorts × 4 jurisdictions via 7 leabharlann PDFs.** This validates the workflow end-to-end before any expansion. Mirrors how the Reform UK pilot was trench-tested first in cianchosaint (per `cianchosaint/docs/case-study/reform-uk-pilot.md`).

## What changes

- **NEW repo `github.com/cianfhoghlaim/ciandlithe`** — sibling to both cianfhoghlaim and cianchosaint. Cold-start skeleton (AGENTS.md + README.md + pyproject.toml + mise.toml + package.json + openspec/).
- **`LICENSE.md` — BUSL-1.1 v2 CIANDLITHE edition** with the Additional Use Grant covering every British-Isles court, tribunal, regulator, ombudsman, law society, bar council, legal-aid body, coroner, health-service complaints body, and registered claimant-representation clinic; the 3-step foreign-use gate (Explain → Do us a favour → Maybe); the **Person-of-Interest clause** (stricter than cianchosaint — bans identifiable private-individual data); the **no-automated-form-submission constraint** (the platform NEVER submits forms to courts.ie / irishstatutebook.ie / nidirect.gov.uk / scotcourts.gov.uk / judiciary.uk); and the warrant-to-enforce clause granted to every Licencee, triggered by either publicly observable evidence OR a credible written complaint.
- **`openspec/specs/ciandlithe-pipeline/spec.md` — the umbrella capability spec** describing the full end-state (foundation + the BLIP v1 single umbrella + the 7 cohort matrix + the 7 personas + the composite pilot).
- **The wholesale-migration plan** (see `cross-repo-sync.md`) for ~30 assets from cianfhoghlaim + cianchosaint → ciandlithe: the 9 Ireland/law DLT sources + 6 Ireland/law BAML files (from cianchosaint) + the 4 Ireland/medicine + 4 legislation.py stubs + the 7 NHS DLT sources (from cianfhoghlaim) + the `dlt_sources/_cross/` + `dlt_sources/common/` helpers (from cianfhoghlaim) + the `cocoindex_flows/_shared/` helpers (from cianfhoghlaim) + the `baml_src/_shared/` + `baml_src/clients.baml` 4-tier provider chain (from cianchosaint) + the 13 compose stacks at `bonneagar/stacks/` (from cianchosaint) + the 3 shared web packages (from cianchosaint) + the `.agents/skills/` (from cianfhoghlaim) + the opencode.json + `.mcp.json` (from cianfhoghlaim).
- **The 4-tier provider chain contract** (documented in this proposal and codified in a follow-up openspec change `ciandlithe-provider-router-v1`): Unsloth Studio → LiteLLM → MiniMax Token Plan → Gemini API, with a 30-second timeout per provider and a 3-strike circuit-breaker.
- **The OSINT source URL allowlist** at `dlt_sources/ciandlithe/common/osint_allowlist.yaml` (NEW), enforced by `mise run lint:license` (NEW) at CI time.
- **The composite pilot FunctionTool** at `agents/ciandlithe/tools/composite_pilot.py` (NEW), the composite pilot BAML extraction at `baml_src/ciandlithe/case_studies/reform_civil_suit_dossier.baml` (NEW), and the composite pilot case-study doc at `docs/case-study/composite-pilot.md` (NEW).
- **The 7 per-persona FunctionTool stubs** at `agents/ciandlithe/tools/<cohort>_pilot.py` (NEW).
- **Per-spec `AGENTS.md` convention** (mirrors cianfhoghlaim's `repo-hygiene-agent-routing` spec).
- **Cross-repo openspec sync convention** with the `cross-repo-sync.md` file (the standard Cianfhoghlaim pattern, retained in ciandlithe).

## Impact

- Affected specs: **1 new spec** (`ciandlithe-pipeline`) + 2 modified Cianfhoghlaim + Cianchosaint specs (`official-law-pipeline-migration-to-ciandlithe-v1` and `cianchosaint-ireland-law-migration-to-ciandlithe-v1`, declared as the documented upstream of the wholesale-migrated assets).
- Affected code/config: ciandlithe repo skeleton (NEW); LICENSE.md (NEW); ~30 wholesale-migrated DLT sources + BAML files + cocoindex flows + 13 compose stacks + 5 opencode subagents + 14-layer knowledge sync loop; 50 NEW DLT source files (the per-sub-nation law + courts + Crown Dependencies); 16 NEW BAML files (the umbrella + per-cohort schemas); 14 NEW cocoindex flows; 7 NEW web apps; the composite pilot FunctionTool + BAML + case-study doc.
- New openspec changes that BLOCK on this change:
  - `ciandlithe-provider-router-v1` — implements the 4-tier chain
  - `ciandlithe-baml-schemas-v1` — the 22 BAML extraction functions
  - `ciandlithe-blip-v1` — the BLIP v1 single umbrella + the 50 cohort DLT sources
  - `ciandlithe-cocoindex-flows-v1` — the 14 CocoIndex flows
  - `ciandlithe-orchestration-v1` — the Dagster defs + asset checks + milestone gates
  - `ciandlithe-per-persona-web-surfaces-v1` — the 7 persona apps
  - `ciandlithe-composite-pilot-workflow-v1` — the 7 composite-pilot FunctionTools + the 7 BAML extractions + the 7 cross-referenced dossiers
  - `ciandlithe-pangolin-ingress-v1` — Pangolin ingress for Unsloth Studio + the 7 web apps
  - `ciandlithe-licence-enforcement-v1` — operationalises the warrant-to-enforce clause
- No secret values are written to disk: all keys resolve via `infisical://dev-baile/ciandlithe/...` template refs hydrated by mise + Locket.
- The cianfhoghlaim repo is unaffected by this change beyond the wholesale-migration markers (added in a follow-up cianfhoghlaim openspec change `official-law-pipeline-migration-to-ciandlithe-v1`).
- The cianchosaint repo is unaffected by this change beyond the wholesale-migration markers (added in a follow-up cianchosaint openspec change `cianchosaint-ireland-law-migration-to-ciandlithe-v1`).
- The leabharlann repo is unaffected (the law + medicine PDFs are read-only context).

## Out of scope

- The actual implementation of the 50 NEW DLT sources (follow-up change `ciandlithe-blip-v1`).
- The 16 NEW BAML extraction functions (follow-up change `ciandlithe-baml-schemas-v1`).
- The 14 NEW cocoindex flows (follow-up change `ciandlithe-cocoindex-flows-v1`).
- The 7 NEW per-persona web apps (follow-up change `ciandlithe-per-persona-web-surfaces-v1`).
- The Pangolin ingress for Unsloth Studio (separate IaC change in `bonneagar`).
- Retrofitting the 4-tier chain into Cianfhoghlaim (separate follow-up `litellm-to-unsloth-provider-chain-v1` per the cianchosaint Q6 = a decision).
- Direct submission to operational systems (e.g. courts.ie POST, irishstatutebook.ie form upload). Explicitly FORBIDDEN per `LICENSE.md §3.8` + the no-auto-submit constraint.

## Dependencies

`Blocked by: none.`
`Blocked by (soft): cianfhoghlaim/cianfhoghlaim@official-law-pipeline-migration-to-ciandlithe-v1` (the existing partial law + medicine pipeline that ciandlithe extends).
`Blocked by (soft): cianchosaint/cianchosaint@cianchosaint-ireland-law-migration-to-ciandlithe-v1` (the existing partial Ireland/law pipeline that ciandlithe extends).
`Affected repos: ciandlithe, cianfhoghlaim, cianchosaint, leabharlann (read-only).`

## Cross-repo sync

See [`cross-repo-sync.md`](./cross-repo-sync.md) for the commit plan + branch + push target for each repo + the order of operations (cianfhoghlaim first, then cianchosaint, then ciandlithe).