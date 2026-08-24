# CIANDLITHE — Usage Guidelines

> **Audience:** Every Licencee named in `LICENSE.md §3.1–§3.7` + every dev who runs `mise run core`.
>
> **Companion docs:** [`README.md`](../README.md) + [`LICENSE.md`](../LICENSE.md) + [`AGENTS.md`](../AGENTS.md) + [`HOW-BRITISH-ISLES-LITIGATION-ENTITIES-USE-CIANDLITHE.md`](HOW-BRITISH-ISLES-LITIGATION-ENTITIES-USE-CIANDLITHE.md) + [`DEMO-PATHS.md`](DEMO-PATHS.md) + [`case-study/composite-pilot.md`](case-study/composite-pilot.md) + [`source-catalogue/blip-v1-sources.md`](source-catalogue/blip-v1-sources.md) + [`configuration-surface.md`](configuration-surface.md).

## §1 — The 5 load-bearing constraints

CIANDLITHE has 5 constraints that every dev + every Licencee MUST respect at all times.

### 1.1 — OSINT ceiling (per `LICENSE.md §3.8 + §5.1`)

The platform MAY ONLY ingest source content from URLs and endpoints listed in `dlt_sources/ciandlithe/common/osint_allowlist.yaml` (the "OSINT Allowlist"). The OSINT Allowlist contains only URLs that point to public-facing pages of British-Isles public-sector litigation bodies (per `LICENSE.md §3.1–§3.7`).

**Enforcement:**

- `mise run lint:license` (the canonical CI gate) verifies every DLT source URL is in the OSINT Allowlist.
- Every BAML extraction function MUST include `osint_ceiling_enforced: bool = True` in its return schema.
- Every FunctionTool at `agents/ciandlithe/tools/*.py` MUST include `osint_ceiling_enforced: True` in its response.

### 1.2 — Person-of-Interest clause (per `LICENSE.md §5.2`)

The platform MAY NOT be used to ingest, store, retrieve, or surface data of any **identifiable natural person who is not a public official**, except where the 3 lawful-basis conditions are met (voluntary public disclosure + public legal proceeding + GDPR lawful basis).

**Enforcement:**

- Every BAML extraction function MUST check the `is_public_official` flag on every `CaseParty` record (per `baml_src/ciandlithe/case_studies/reform_civil_suit_dossier.baml`).
- Any extraction naming a non-public individual MUST set `analyst_review_required: True` and MUST NOT auto-render the name in any shared view.
- The composite pilot's FunctionTool response uses `[redacted per PoI clause]` placeholders for non-public individuals.

### 1.3 — No-automated-form-submission constraint (per `LICENSE.md §3.8`)

The platform NEVER directly submits forms to courts.ie / irishstatutebook.ie / nidirect.gov.uk / scotcourts.gov.uk / judiciary.uk / courtserve.net or any other British-Isles court / tribunal / regulator endpoint. The platform generates a *dossier* (PDF + structured JSON) for manual review by the claimant or their solicitor.

**Enforcement:**

- Every FunctionTool at `agents/ciandlithe/tools/*.py` MUST include `analyst_review_required: True` in its response.
- Every per-persona web app at `web/apps/ciandlithe-<persona>/` MUST offer a "Download dossier (PDF + JSON)" button and MUST NOT offer any "Submit to court" / "File on my behalf" / "Send to court registry" affordance.
- The FunctionTool wrapper around `composite_pilot_tool` (`agents/ciandlithe/tools/composite_pilot.py`) enforces this at the Python layer.

### 1.4 — 4-tier model provider chain (per `baml_src/_shared/provider_router.py`)

Every LLM-touching surface in ciandlithe routes through `ModelProviderRouter` with a 30-second timeout per provider and a 3-strike circuit-breaker:

- Tier 1 (PRIMARY): Unsloth Studio (`http://unsloth-serve:8889/api/v1`)
- Tier 2: LiteLLM Proxy (`https://litellm.ciandlithe.ie`)
- Tier 3: MiniMax Token Plan (`https://api.minimax.io/v1`)
- Tier 4 (LAST RESORT): Gemini API (`https://generativelanguage.googleapis.com/v1beta`)

**Enforcement:**

- `mise run ciandlithe:provider:health-check` pings each of the 4 providers + returns a health table.
- The router's `_last_span["provider_used"]` is logged to Langfuse for observability.

### 1.5 — BUSL-1.1 v2 CIANDLITHE edition (the load-bearing legal constraint)

The licence at `LICENSE.md` is the load-bearing architectural constraint. Every Licencee has a warrant-to-enforce (§7) triggered by either publicly observable evidence OR a credible written complaint.

**Enforcement:**

- `LICENSE.md` is the canonical document; do not modify it without an openspec change.
- The Additional Use Grant (§3) lists every Licencee. New Licencees MUST be added via PR + openspec change.
- The 3-step foreign-use gate (§6) is enforced at the onboarding layer (any non-British-Isles user must satisfy the 3 steps before being granted access).

## §2 — The 3 deployment footprints

### 2.1 — Citizen footprint (self-rep claimant + WRC claimant + HSE/NHS complainant + PIAB applicant + coroner + inquest + legal-aid applicant)

- **Components:** Docker Compose bundle at `web/apps/ciandlithe-self-rep/` + 5 containers (Unsloth Studio + LiteLLM + Locket + Crawl4AI + Stagehand)
- **Cloud dependencies:** NONE (all local)
- **Live deployment:** `git clone` → `docker compose up -d` → `open http://localhost:7777`
- **Time to first dossier:** ~5 minutes

### 2.2 — Law-clinic analyst footprint

- **Components:** 13 compose stacks (per `bonneagar/stacks/`) + 7 per-persona web apps + MotherDuck + Cloudflare Workers
- **Cloud dependencies:** arm1-oci (or Hetzner) + Pangolin + Cloudflare + Infisical + MotherDuck SaaS
- **Live deployment:** provision cloud + DNS + deploy 13 stacks + deploy 7 web apps
- **Time to first dossier:** ~2 days

### 2.3 — Developer / contributor footprint

- **Components:** `mise run core` + CCC indexing + opencode + openspec
- **Live deployment:** `git clone` → `mise install` → `mise run core` → `openspec list` → `bun run ccc:init`
- **Time to first dossier:** ~2 hours

## §3 — The 3 demo paths

For detailed step-by-step demos, see [`DEMO-PATHS.md`](DEMO-PATHS.md). Quick orientation:

| Persona | App | Demo duration | Primary value |
|---|---|---|---|
| **Self-rep claimant** | `web/apps/ciandlithe-self-rep/` | 5 min | Conversational agent for non-emergency court-form preparation |
| **WRC / ET claimant** | `web/apps/ciandlithe-wrc/` | 5 min | WRC complaint drafting + hearing-day checklists |
| **HSE / NHS complainant** | `web/apps/ciandlithe-health-complain/` | 5 min | HSE / NHS complaint drafting + clinical-incident navigation |
| **PIAB applicant** | `web/apps/ciandlithe-piab/` | 5 min | PIAB form + book of documents + medical report collation |
| **Coroner's court applicant** | `web/apps/ciandlithe-coroner/` | 5 min | Notification of death + post-mortem request + inquest witness prep |
| **Inquest counsel** | `web/apps/ciandlithe-inquest/` | 30 min | Article 2 ECHR framing + disclosure requests + interested-party status |
| **Legal-aid applicant** | `web/apps/ciandlithe-legal-aid/` | 5 min | Legal Aid Board / Agency / SLAB / NILSC eligibility + form drafting |

## §4 — What you MUST NOT do

1. **Do NOT submit forms to courts.ie / irishstatutebook.ie / nidirect.gov.uk / scotcourts.gov.uk / judiciary.uk / courtserve.net or any other British-Isles court / tribunal / regulator endpoint.** The platform is read-only + manual-review-only for these endpoints. Per `LICENSE.md §3.8`.
2. **Do NOT ingest URLs not on the OSINT Allowlist.** Per `LICENSE.md §5.1`. Add new URLs to `dlt_sources/ciandlithe/common/osint_allowlist.yaml` via PR + openspec change FIRST.
3. **Do NOT surface the names of non-public individuals in any shared view** (without analyst review). Per `LICENSE.md §5.2`. Use the `[redacted per PoI clause]` placeholder pattern from the composite pilot FunctionTool.
4. **Do NOT bypass the 4-tier provider chain.** Per `baml_src/_shared/provider_router.py`. The 4 tiers are the only source of truth for LLM calls. Adding a 5th provider requires a separate openspec change.
5. **Do NOT modify `LICENSE.md` without an openspec change.** Per the licence being the load-bearing architectural constraint.
6. **Do NOT commit secrets.** All secrets resolve via `infisical://dev-baile/ciandlithe/...` template refs (per `.infisical.env`). The CI gate enforces this.
7. **Do NOT commit private case-study evidence.** The `stedding/private_case_evidence/` folder is gitignored. Only the leabharlann PDFs (read-only context) appear in the open repo.

## §5 — Cross-references

- [`README.md`](../README.md) — the project overview
- [`LICENSE.md`](../LICENSE.md) — the load-bearing legal document
- [`AGENTS.md`](../AGENTS.md) — the canonical agent routing
- [`openspec/AGENTS.md`](../openspec/AGENTS.md) — the openspec workflow
- [`DEMO-PATHS.md`](DEMO-PATHS.md) — the 3 demo paths
- [`HOW-BRITISH-ISLES-LITIGATION-ENTITIES-USE-CIANDLITHE.md`](HOW-BRITISH-ISLES-LITIGATION-ENTITIES-USE-CIANDLITHE.md) — the audience-targeted use guide
- [`case-study/composite-pilot.md`](case-study/composite-pilot.md) — the canonical pilot narrative
- [`source-catalogue/blip-v1-sources.md`](source-catalogue/blip-v1-sources.md) — the ~70 DLT source URL catalogue
- [`configuration-surface.md`](configuration-surface.md) — the per-deployment configuration surface
- [`research/law-med-malpractice-research.md`](research/law-med-malpractice-research.md) — the 60+ leabharlann PDFs synthesis
- [`governance/ROLES.md`](governance/ROLES.md) — roles + responsibilities
- [`governance/CONTRIBUTING.md`](governance/CONTRIBUTING.md) — contribution guidelines
- [`governance/CODE_OF_CONDUCT.md`](governance/CODE_OF_CONDUCT.md) — code of conduct