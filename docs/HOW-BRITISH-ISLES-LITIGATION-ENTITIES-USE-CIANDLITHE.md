# CIANDLITHE — How British-Isles Litigation Entities Use Ciandlithe

> **Audience:** Courts Service of Ireland, NICTS, Scottish Courts, HMCTS, Crown Dependencies courts, WRC, PIAB, HSE / NHS complaints bodies, NI Ombudsman, NHS Resolution, GMC, Law Society of Ireland, Law Society of NI, Faculty of Advocates, Bar of NI, Bar of England & Wales, Legal Aid Board, Legal Aid Agency, SLAB, NILSC, Coroner Service of Ireland, Coroners' Society of England & Wales, registered claimant-representation charities.
>
> **Companion docs:** USAGE-GUIDELINES.md · DEMO-PATHS.md · LIVE-DEPLOYMENT-PLAN.md · DEPLOYMENT.md · case-study/composite-pilot.md · source-catalogue/blip-v1-sources.md · configuration-surface.md
>
> **Licence:** BUSL-1.1 v2 — CIANDLITHE edition (British-Isles-only Additional Use Grant + 3-step foreign-use gate + Person-of-Interest clause + no-automated-form-submission constraint + warrant-to-enforce clause)

## §1 — Welcome + why this document exists

This document is for the British-Isles public-sector litigation bodies explicitly named in the BUSL-1.1 v2 CIANDLITHE licence Additional Use Grant.

**The purpose of ciandlithe** is to **minimise the burden of entry** for British-Isles litigation preparation by self-representing claimants, WRC claimants, HSE/NHS complainants, PIAB applicants, inquest parties, coroner's-court applicants, and legally-aided claimants. The platform covers civil-litigation preparation across 8 British-Isles nations + 3 Crown Dependencies — court-form generation, medical-malpractice investigation, personal-injury / PIAB application, WRC / Employment-Tribunal complaints, HSE / NHS complaints, statute lookup, and court-judgment lookup — all through the OSINT ceiling (public-facing content only) and within the BUSL-1.1 v2 CIANDLITHE licence posture.

The case studies in this document — the composite pilot of 7 entities (QUB/RVH brain-injury, Eric employer/breach, Garda data-access, DkIT education, NUIG education, UCL admission, sodium valproate misprescription) — are **illustrative examples of what the platform enables** for litigation preparation. They are **not** the repository author's only research interest. They demonstrate the kinds of cross-source investigations the medical-malpractice pipeline + the civil-litigation pipeline enable. Other British-Isles public-sector litigation bodies may use the platform for any civil-litigation preparation within the OSINT ceiling + the licence posture.

**The meta-purpose of this document** is to explain how a body with NO prior AI/OPS skills can stand up their own use of the platform.

## §2 — The minimal skill set the platform removes

You don't need to be a senior platform engineer to use ciandlithe. The 4-tier provider chain + the 13 compose stacks + the OSINT allowlist + the composite pilot FunctionTool + the 7 per-persona web apps remove the need for these specialist skills:

| Skill | How the platform abstracts it |
|---|---|
| OpenAI-compatible API key management | The 4-tier `ModelProviderRouter` abstracts it — see `baml_src/_shared/provider_router.py` |
| Docker orchestration debugging | The 6-file GOLD_STANDARD pattern (compose.yaml + sidecar.yaml + secrets.env + pangolin.yaml + blueprint.yaml + .env.example) |
| VLM / OCR model selection | BAML abstracts it — see `baml_src/ciandlithe/ireland/law/*.baml` + `baml_src/ciandlithe/case_studies/*.baml` |
| Vector embedding | LanceDB + BAAI/bge-m3 abstracts it — see `cocoindex_flows/_shared/_lifespan.py` |
| Knowledge graph construction | Cognee + Graphiti abstracts it — see `agents/meaisinfhoghlaim/firecrawl_mcp/memory/` |
| Browser automation | Stagehand + Crawl4AI + headless Chrome abstracts it |
| Pipeline orchestration | Dagster abstracts it — see `orchestration/defs/` |
| Secret injection | Locket sidecar abstracts it |
| Reverse proxy + identity | Pangolin abstracts it |
| Resource-sync + procedure engine | Komodo abstracts it |
| CocoIndex embedding pipeline | CocoIndex v1 abstracts it |
| Litigation-form lookup | The BAML extraction schemas abstract it — see `baml_src/ciandlithe/ireland/law/courts.baml:CourtForm` |
| Court-rules lookup | | `court_rules.baml:CourtRule` |
| Court-judgment lookup | | `judgements.baml:Judgement` |
| PIAB application generation | | `piab.baml:PIABPage` |
| Legal-aid application generation | | `legal_aid.baml:LegalAidForm` |

You only need to:
1. Run `mise run core` (the full bootstrap)
2. Open the per-persona web app (e.g. `web/apps/ciandlithe-self-rep/`)
3. Type your complaint / case-study / question
4. Download the dossier (PDF + JSON) for manual review

If you're already comfortable with Docker + Git + YAML + Python, the entire setup takes ~1 hour for the self-hosted citizen footprint or ~2 days for the full law-clinic analyst footprint.

## §3 — The 3 deployment footprints

### §3.1 — Self-hosted citizen footprint (~8 GB RAM, ~1 hour, $0/month)
- **Who:** A British-Isles self-representing claimant, WRC claimant, HSE/NHS complainant, PIAB applicant, coroner's-court applicant, or legal-aid applicant on their own machine (Raspberry Pi 5, NAS, laptop)
- **Components:** Docker Compose bundle at `web/apps/ciandlithe-self-rep/` + 5 containers (Unsloth Studio + LiteLLM + Locket + Crawl4AI + Stagehand)
- **Cloud dependencies:** NONE (all local)
- **Live deployment:** `git clone` → `docker compose up -d` → `open http://localhost:7777`

### §3.2 — Law-clinic analyst footprint (cloud, ~$3k/month, ~2 days)
- **Who:** A Law Society of Ireland analyst + a Law Society of NI analyst + a Law Society of England & Wales analyst + a legal-aid clinic solicitor
- **Components:** 13 compose stacks + 7 per-persona web apps + MotherDuck + Cloudflare Workers
- **Cloud dependencies:** arm1-oci (or Hetzner) + Pangolin + Cloudflare + Infisical + MotherDuck SaaS
- **Live deployment:** provision cloud + DNS + deploy 13 stacks + deploy 7 web apps

### §3.3 — Developer / contributor footprint (local dev, ~30 minutes, $0/month)
- **Components:** `mise run core` + CCC indexing + opencode + openspec
- **Live deployment:** `git clone` → `mise install` → `mise run core` → `openspec list` → `bun run ccc:init`

## §4 — The 13 stacks

The 13 stacks deploy in order (per `DEPLOYMENT.md §2`):

| # | Stack | Port | Purpose |
|--:|:--|--:|:--|
| 1 | infisical | 8443 | Secrets management |
| 2 | motherduck | (SaaS) | Cloud DuckDB via Postgres endpoint |
| 3 | lakehouse | 3900-3904, 5433, 8181-8182 | Garage S3 + Postgres + Lakekeeper |
| 4 | litellm | 4000 | LLM gateway |
| 5 | unsloth-serve | 8889 | Tier-1 local LLM |
| 6 | langfuse | 3000 | LLM observability |
| 7 | crawl4ai | 11235 | Self-hosted browser scraper |
| 8 | stagehand | 11300 | Stagehand + headless Chrome |
| 9 | changedetection | 5000 | Page-change monitor |
| 10 | komodo | 9120 | GitOps deployment orchestrator |
| 11 | pangolin | 8443 (alt) | Reverse proxy + identity |
| 12 | locket | (sidecar) | Secret-injection sidecar |
| 13 | traefik | 80/443 | Edge proxy + TLS termination |

## §5 — The 7 per-persona web apps

| # | Persona | App | Purpose |
|--:|---|---|---|
| 1 | Self-rep claimant | `web/apps/ciandlithe-self-rep/` | Circuit / District / High Court self-rep toolkit |
| 2 | WRC / ET claimant | `web/apps/ciandlithe-wrc/` | Workplace Relations / Employment Tribunal bundle |
| 3 | HSE / NHS complainant | `web/apps/ciandlithe-health-complain/` | HSE / NHS complaint drafting + clinical-incident navigation |
| 4 | PIAB applicant | `web/apps/ciandlithe-piab/` | Personal Injuries Assessment Board application |
| 5 | Coroner's court applicant | `web/apps/ciandlithe-coroner/` | Coroner's inquest bundle |
| 6 | Inquest counsel | `web/apps/ciandlithe-inquest/` | For solicitors/barristers preparing an inquest |
| 7 | Legal-aid applicant | `web/apps/ciandlithe-legal-aid/` | Legal Aid Board / Agency / SLAB / NILSC eligibility |

## §6 — The composite pilot (the canonical worked example)

The 7 composite-pilot parties (per `docs/case-study/composite-pilot.md` + `agents/ciandlithe/tools/composite_pilot.py`):

1. **QUB / Royal Victoria Hospital brain-injury** (medical_malpractice, NI) — `law/qub_royal_victoria_malpractice.pdf`
2. **Eric employer / breach of contract** (employer_breach, Cross-border NI ↔ ROI) — `law/suing_ceo_for_breach_abuse_damages.pdf`
3. **Garda discrimination / data-access** (garda_discrimination, ROI) — `law/garda_corruption_and_data_access.pdf`
4. **DkIT disability / education complaint** (education_discrimination, ROI) — `law/discrimination_case_strategy_university_of_galway.pdf`
5. **NUIG / UoG rejection + abuse of power** (education_discrimination, ROI) — `law/discrimination_case_strategy_university_of_galway.pdf`
6. **UCL offer / DBS** (admission_breach, England) — `law/ucl_sar_equality_act_claim.pdf`
7. **Sodium valproate / HSE misprescription** (medical_malpractice, ROI) — `medical/irish_sodium_valproate_inquiry_and_healthcare.pdf`

The composite pilot validates the workflow end-to-end before any expansion to multi-party dossiers.

## §7 — What you MUST NOT do (per the licence)

1. **Do NOT submit forms to courts.ie / irishstatutebook.ie / nidirect.gov.uk / scotcourts.gov.uk / judiciary.uk / courtserve.net or any other British-Isles court / tribunal / regulator endpoint.** The platform is read-only + manual-review-only for these endpoints. Per `LICENSE.md §3.8`.
2. **Do NOT ingest URLs not on the OSINT allowlist.** Per `LICENSE.md §5.1`. Add new URLs to `dlt_sources/ciandlithe/common/osint_allowlist.yaml` via PR + openspec change FIRST.
3. **Do NOT surface the names of non-public individuals in any shared view** (without analyst review). Per `LICENSE.md §5.2`. Use the `[redacted per PoI clause]` placeholder pattern.
4. **Do NOT bypass the 4-tier provider chain.** Per `baml_src/_shared/provider_router.py`. The 4 tiers are the only source of truth for LLM calls.

## §8 — Where to get help

- **Documentation:** Start with [`README.md`](../../README.md) + [`AGENTS.md`](../../AGENTS.md) + [`USAGE-GUIDELINES.md`](../USAGE-GUIDELINES.md).
- **Demo paths:** See [`DEMO-PATHS.md`](../DEMO-PATHS.md).
- **Deployment:** See [`DEPLOYMENT.md`](../DEPLOYMENT.md).
- **Configuration:** See [`configuration-surface.md`](../configuration-surface.md).
- **Source catalogue:** See [`source-catalogue/blip-v1-sources.md`](../source-catalogue/blip-v1-sources.md).
- **Composite pilot narrative:** See [`case-study/composite-pilot.md`](../case-study/composite-pilot.md).
- **Tangent fork template:** See [`TANGENT-FORK-PROMPT-TEMPLATE.md`](../TANGENT-FORK-PROMPT-TEMPLATE.md).

## §9 — Cross-references

- [`README.md`](../../README.md) — project overview
- [`LICENSE.md`](../../LICENSE.md) — the load-bearing legal document (BUSL-1.1 v2 CIANDLITHE edition)
- [`AGENTS.md`](../../AGENTS.md) — canonical agent routing
- [`USAGE-GUIDELINES.md`](../USAGE-GUIDELINES.md) — operational guidelines
- [`DEMO-PATHS.md`](../DEMO-PATHS.md) — 3 demo paths
- [`DEPLOYMENT.md`](../DEPLOYMENT.md) — deployment procedure
- [`LIVE-DEPLOYMENT-PLAN.md`](../LIVE-DEPLOYMENT-PLAN.md) — Cloudflare + arm1-oci + MotherDuck SaaS plan
- [`case-study/composite-pilot.md`](../case-study/composite-pilot.md) — canonical pilot narrative
- [`source-catalogue/blip-v1-sources.md`](../source-catalogue/blip-v1-sources.md) — DLT source URL catalogue
- [`configuration-surface.md`](../configuration-surface.md) — per-deployment config surface
- [`research/law-med-malpractice-research.md`](../research/law-med-malpractice-research.md) — 60+ leabharlann PDFs synthesis