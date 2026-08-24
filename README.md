# CIANDLITHE

> **Wordplay (canonical):** *Ciandlíthe* = Irish Gaelic "cian" (long/far/longing) + "dlíthe" (laws / statutes) → "distant laws" / "far statutes". Mirrors *Cianfhoghlaim* = "cian" + "fhoghlaim" (learning) and *Cianchosaint* = "cian" + "chosaint" (defence).

**The British-Isles civil-litigation open-source OSINT platform for self-representing claimants, WRC claimants, HSE/NHS complainants, PIAB applicants, inquest parties, coroner's-court applicants, and legal-aid applicants.**

Ciandlithe is a defensive OSINT (Open-Source Intelligence) data platform for civil-litigation preparation across the British Isles. It ingests public official-government sources — the Irish Statute Book, Courts.ie, NICTS, Scottish Courts and Tribunals Service, HMCTS for England & Wales, the Crown Dependencies courts, HSE + NHS complaints processes, WRC decisions, PIAB decisions, GMC FTPAN decisions, NHS Resolution, BAILII judgments, ICLR CaseMine, and the law-society / bar-council disciplinary registers — and routes them through a 4-tier model provider chain (Unsloth Studio → LiteLLM → MiniMax → Gemini) for BAML extraction, CocoIndex v1 embedding, LanceDB + DuckLake storage, and per-persona TanStack Start + Convex + AG-UI + CopilotKit dashboards.

## Why does this exist?

Two reasons.

**First — equalisation.** British-Isles self-representing claimants, WRC claimants, HSE/NHS complainants, PIAB applicants, inquest parties, and legally-aided claimants should not have to negotiate a £30k+/year LexisNexis or Westlaw licence just to read public court judgments and statutes that their own government publishes for free. This platform ships a permissive-internal BUSL-1.1 v2 grant covering every court, tribunal, regulator, ombudsman, law society, bar council, legal-aid body, coroner, health-service complaints body, and registered claimant-representation clinic of the Republic of Ireland, the United Kingdom of Great Britain and Northern Ireland (including the devolved administrations of Scotland, Wales, and Northern Ireland), and the Crown Dependencies (Jersey, Guernsey, Isle of Man).

**Second — open-source SOTA is good enough.** The platform is a case study that proves the open-source SOTA stack (Unsloth Studio for local fine-tuning, HuggingFace for OCR/VLM/embedding, LiteLLM + MiniMax + Gemini as fallback, BAML for typed extraction, CocoIndex v1 for embeddings, LanceDB + DuckLake + MotherDuck for storage, Dagster for orchestration, TanStack Start + Convex + AG-UI + CopilotKit for dashboards) is sufficient for British-Isles civil-litigation preparation. Without this stack, self-rep claimants and small legal-aid clinics fall behind well-funded commercial law firms that can afford proprietary AI; with this stack, they have parity.

## The composite pilot (the canonical case study)

The ciandlithe composite pilot exercises **all 7 cohorts × 4 jurisdictions** via 7 leabharlann PDFs (one per pilot party), drawn from the existing case-study material in `leabharlann/gemini_deep_research/law/` + `leabharlann/gemini_deep_research/medical/`:

| # | Pilot party | Cohort | Sub-nation |
|--:|---|---|---|
| 1 | QUB / Royal Victoria Hospital brain-injury | medical_malpractice | NI |
| 2 | Eric (employer / breach of contract) | employer_breach | Cross-border NI ↔ ROI |
| 3 | Garda discrimination / data-access | garda_discrimination | ROI |
| 4 | DkIT disability / education complaint | education_discrimination | ROI |
| 5 | NUIG / UoG rejection + abuse of power | education_discrimination | ROI |
| 6 | UCL offer / DBS | admission_breach | England |
| 7 | Sodium valproate / HSE misprescription | medical_malpractice | ROI |

Each pilot party is **single-entity, allowlist-bounded**, mirroring how Reform UK was single-entity in cianchosaint. The pilots expand from there. See `docs/case-study/composite-pilot.md` for the canonical narrative.

## The flagship umbrella pipeline

| Pipeline | Sub-cohorts | Cohorts |
|---|---|---:|
| **BLIP v1** — British Isles Litigation Pipeline | 7 cohorts (civil-litigation / medical-malpractice / personal-injury / WRC / HSE-NHS / statutes / court judgments) × 6-8 jurisdictions | ~50 |

**BLIP v1 cohort matrix** (each cell = 1 DLT source + 1 BAML function + 1 FunctionTool + 1 per-persona AG-UI tab):

| Cohort | ROI | NI | Scotland | Wales | England | Crown Deps |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| **Civil-litigation forms** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Medical-malpractice / clinical-negligence** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Personal injury / PIAB / NHS-litigation** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Workplace-relations / WRC / ET** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **HSE / NHS complaints** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Statutes + SIs + court rules** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Court judgments + tribunal decisions** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

## The 4-tier model provider chain

Every LLM-touching surface in ciandlithe routes through `ModelProviderRouter` (`baml_src/_shared/provider_router.py`) with a 30-second timeout per provider and a 3-strike circuit-breaker:

| Tier | Provider | URL | Why |
|---|---|---|---|
| 1 (PRIMARY) | Unsloth Studio (local API) | `http://unsloth-serve:8889/api/v1` (Pangolin ingress later) | Self-hosted, audited, no egress |
| 2 | LiteLLM Proxy | `https://litellm.ciandlithe.ie` | Existing fallback |
| 3 | MiniMax Token Plan | `https://api.minimax.io/v1` | Direct, metered |
| 4 (LAST RESORT) | Gemini API | `https://generativelanguage.googleapis.com/v1beta` | Universal fallback |

## The licence

This repository is licensed under **Business Source License 1.1 — CIANDLITHE edition** (see `LICENSE.md`). The licence:

- Grants broad production use to every court, tribunal, regulator, ombudsman, law society, bar council, legal-aid body, coroner, health-service complaints body, and registered claimant-representation clinic of the Republic of Ireland, the United Kingdom, and the Crown Dependencies.
- Bans commercial use, foreign use (without satisfying the 3-step gate: Explain → Do us a favour → Maybe), academic / cultural / journalistic / research use, and Person-of-Interest data of identifiable non-public individuals.
- Grants a **warrant-to-enforce** to every Licencee named in the Additional Use Grant (§3), triggered by either publicly observable evidence OR a credible written complaint.

The licence is the load-bearing architectural constraint. Every design decision is subordinate to it.

## The 7 per-persona web surfaces

| Persona | App | Primary value |
|---|---|---|
| Self-rep claimant | `web/apps/ciandlithe-self-rep/` | Circuit/District/High Court self-rep toolkit: generates the right pleading form, lists the relevant statutes + precedents, drafts the witness statement + affidavit of means |
| WRC / Employment-Tribunal claimant | `web/apps/ciandlithe-wrc/` | Workplace Relations Commission / ET bundle: complaint drafting, precedent matching, hearing-day checklists |
| HSE / NHS complainant | `web/apps/ciandlithe-health-complain/` | HSE / NHS complaint drafting + clinical-incident navigation + complaint escalation |
| PIAB applicant | `web/apps/ciandlithe-piab/` | Personal Injuries Assessment Board application: PIAB form + book of documents + medical report collation |
| Coroner's Court applicant | `web/apps/ciandlithe-coroner/` | Coroner's inquest bundle: notification of death, post-mortem request, inquest witness preparation |
| Inquest counsel | `web/apps/ciandlithe-inquest/` | For solicitors/barristers preparing an inquest — article 2 ECHR framing, disclosure requests, interested-party status |
| Legal-aid applicant | `web/apps/ciandlithe-legal-aid/` | Legal Aid Board (Ireland) + Legal Aid Agency (England & Wales) + SLAB (Scotland) + LSA (NI) eligibility + form drafting |

## The OSINT ceiling + the no-auto-submit constraint

The platform NEVER directly submits forms to courts.ie / irishstatutebook.ie / nidirect.gov.uk / scotcourts.gov.uk / judiciary.uk / courtserve.net. It generates a *dossier* (PDF + structured JSON) for **manual review by the claimant or their solicitor**. This is the load-bearing safety constraint, enforced at three layers:

1. **DLT source layer:** Every DLT source URL must be on `dlt_sources/ciandlithe/common/osint_allowlist.yaml` (CI gate: `mise run lint:license`).
2. **BAML extraction layer:** Every BAML extraction function must include `osint_ceiling_enforced: bool = True` in its return schema.
3. **FunctionTool + per-persona web app layer:** Every FunctionTool must include `osint_ceiling_enforced` + `analyst_review_required` flags. The per-persona web apps render these flags prominently and offer no "auto-submit to court" affordance.

The Person-of-Interest clause (`LICENSE.md §5.2`) is stricter than the cianchosaint clause: the platform stays at the level of **procedural + statutory + precedent OSINT**, not "dossiers on named private individuals".

## OpenSpec

This repository uses [OpenSpec](https://github.com/Fission-AI/OpenSpec) for spec-driven change management. Every non-trivial change lives in `openspec/changes/<id>/` as a 3-artifact bundle (`proposal.md` + `tasks.md` + spec deltas) before any code is written.

```bash
openspec list --specs                   # list all capability specs
openspec list                           # list all pending changes
openspec validate <change-id> --strict  # MUST pass before commit
openspec archive <change-id> --yes      # after deploy
```

## Repo boundary

| Domain | Location |
|:--|:--|
| Data platform (DLT + Dagster + BAML + CocoIndex + MotherDuck + marimo) | `dlt_sources/`, `orchestration/`, `baml_src/`, `cocoindex_flows/`, `notebooks/` |
| Agent fleet (12-agent + per-persona routing) | `agents/` |
| Per-persona web surfaces (TanStack Start + Convex + AG-UI + CopilotKit) | `web/apps/<persona>/` |
| OpenSpec changes + specs | `openspec/` |
| MotherDuck Dives / Flights metadata | `motherduck/` |
| IaC (Komodo + Pangolin + Infisical clients) | `bonneagar/iac/` |
| Docker Compose stacks | `bonneagar/stacks/<name>/` |
| Private case-study evidence (NOT in the open repo) | `stedding/private_case_evidence/` (gitignored) |

## Cross-repo convention

Ciandlithe is a **sibling repo** to `cianfhoghlaim/cianfhoghlaim` (the education / long-distance learning platform) and `cianfhoghlaim/cianchosaint` (the defence / policing / intel-oversight platform). The three repos share the openspec workflow, the 14-layer knowledge sync loop, the 5 opencode subagents, the Infisical `dev-baile` vault (ciandlithe has its own `ciandlithe/` folder), and the Lakehouse stack.

The three repos diverge on domain (education vs defence/policing/intel vs civil-litigation), licence posture (cultural grant vs British-Isles-only OSINT with warrant-to-enforce vs British-Isles-only OSINT with warrant-to-enforce + PoI clause + no-auto-submit constraint), provider chain (LiteLLM-primary vs Unsloth Studio primary + 3-tier fallback — same for ciandlithe), and persona surfaces (students/teachers/parents vs government analysts vs self-rep claimants / WRC claimants / HSE-NHS complainants / PIAB applicants / inquest parties / coroner's-court applicants / legal-aid applicants).

## Cross-references

- [`LICENSE.md`](LICENSE.md) — the load-bearing legal document (BUSL-1.1 v2 CIANDLITHE edition)
- [`AGENTS.md`](AGENTS.md) — the canonical agent routing
- [`openspec/AGENTS.md`](openspec/AGENTS.md) — the openspec workflow
- [`openspec/changes/ciandlithe-repo-foundation-v1/`](openspec/changes/ciandlithe-repo-foundation-v1/) — the first openspec change
- [`openspec/specs/ciandlithe-pipeline/spec.md`](openspec/specs/ciandlithe-pipeline/spec.md) — the umbrella capability spec
- [`docs/case-study/composite-pilot.md`](docs/case-study/composite-pilot.md) — the canonical pilot narrative
- [`docs/USAGE-GUIDELINES.md`](docs/USAGE-GUIDELINES.md) — the OSINT ceiling + no-auto-submit constraint in operational terms
- [`docs/HOW-BRITISH-ISLES-LITIGATION-ENTITIES-USE-CIANDLITHE.md`](docs/HOW-BRITISH-ISLES-LITIGATION-ENTITIES-USE-CIANDLITHE.md) — the audience-targeted use guide