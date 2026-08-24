# CIANDLITHE — Agent Routing

> **Wordplay (canonical):** *Ciandlíthe* = Irish Gaelic "cian" (long/far/longing) + "dlíthe" (laws / statutes) → "distant laws" / "far statutes". Mirrors *Cianfhoghlaim* = "cian" + "fhoghlaim" (learning) and *Cianchosaint* = "cian" + "chosaint" (defence).
>
> **Scope (per `LICENSE.md`):** OSINT-only British-Isles civil-litigation data platform. **Strictly restricted** to courts, tribunals, regulators, ombudsmen, law societies, bar councils, legal-aid bodies, coroners, health-service complaints bodies, and registered claimant-representation clinics of the Republic of Ireland, the United Kingdom of Great Britain and Northern Ireland (including the devolved administrations of Scotland, Wales, and Northern Ireland), and the Crown Dependencies (Jersey, Guernsey, Isle of Man). Foreign use requires satisfaction of the 3-step gate (Explain → Do us a favour → Maybe). The warrant-to-enforce is held by every Licencee named in `LICENSE.md § Additional Use Grant`. The OSINT ceiling + the Person-of-Interest clause are enforced at the source-URL allowlist layer (per `LICENSE.md §5`).

## Priority quick reference

### What ciandlithe IS

- A sibling repo to `cianfhoghlaim/cianfhoghlaim` (the education / long-distance learning platform) and `cianfhoghlaim/cianchosaint` (the defence / policing / intelligence-oversight platform).
- A defensive OSINT pipeline: ingest public official-government sources (Irish Statute Book, Courts.ie, NICTS, scotcourts.gov.uk, judiciary.uk, Crown Dependencies courts, HSE, NHS, GMC, WRC, PIAB, NHS Resolution, courtserve.net, BAILII, ICLR CaseMine) → BAML extraction → CocoIndex v1 embeddings → LanceDB + DuckLake + MotherDuck → TanStack Start + Convex + AG-UI + CopilotKit per-persona dashboards for self-representing claimants, WRC claimants, HSE/NHS complainants, PIAB applicants, inquest parties, coroner's-court applicants, and legal-aid applicants.
- A case study that proves open-source SOTA (Unsloth Studio + LiteLLM + MiniMax + Gemini + HuggingFace) is sufficient for British-Isles litigation preparation by self-represented and legally-aided claimants.
- A defensible answer to the question: *"why do self-rep claimants and small legal-aid clinics have to pay LexisNexis / Westlaw when the official sources are public?"*

### What ciandlithe IS NOT

- A platform for **automated form submission** to courts.ie / irishstatutebook.ie / nidirect.gov.uk / scotcourts.gov.uk / judiciary.uk / courtserve.net. The platform generates a *dossier* (PDF + structured JSON) for **manual review by the claimant or their solicitor**. This is the load-bearing safety constraint.
- A platform for **Person-of-Interest data** of identifiable private individuals. The Person-of-Interest clause in `LICENSE.md §5.2` is stricter than the cianchosaint clause.
- A platform for **foreign intelligence agencies** or foreign government bodies. `LICENSE.md §6` explicitly bans them via the 3-step gate.
- A platform for **academic / cultural / journalistic / research use**. Use `cianfhoghlaim/cianfhoghlaim` for those purposes.
- A **substitute for independent legal advice from a qualified solicitor or barrister** registered in the relevant British-Isles jurisdiction. `LICENSE.md §9` makes this explicit.

## Routing table — "where do I do X in ciandlithe?"

| I want to... | Look at... |
|:--|:--|
| Add a new DLT source for a British-Isles official source | `dlt_sources/ciandlithe/<cohort>/<sub-nation>/<source>.py` — mirror the existing `dlt_sources/cianchosaint/<vertical>/<jurisdiction>/<source>.py` pattern |
| Add a new BAML extraction function | `baml_src/ciandlithe/<cohort>/<file>.baml` (extend) or `baml_src/ciandlithe/<cohort>/<new>.baml` (new file) — every function MUST set `osint_ceiling_enforced: bool = True` in its return schema |
| Configure the 4-tier provider chain | `baml_src/clients.baml` + `baml_src/_shared/provider_router.py` |
| Add a new per-persona web surface | `web/apps/ciandlithe-<persona>/` — TanStack Start + Convex + AG-UI + CopilotKit |
| Add a new openspec change | `openspec/changes/<change-id>/{proposal.md, tasks.md, cross-repo-sync.md}` + `openspec/changes/<change-id>/specs/<spec-name>/spec.md` |
| Add a new capability spec | `openspec/specs/<spec-name>/spec.md` + sibling `AGENTS.md` (≤30 lines) |
| Run the openspec validation gate | `openspec validate <change-id> --strict` (MUST pass before commit) |
| Run the licence audit | `mise run lint:license` — verifies every DLT source URL is in the OSINT allowlist AND every allowlist entry points at a British-Isles public-sector body |
| Run the provider health check | `mise run ciandlithe:provider:health-check` — pings each of the 4 providers, returns health table |
| Add a new FunctionTool | `agents/ciandlithe/tools/<cohort>_tool.py` — every FunctionTool MUST include `osint_ceiling_enforced: True` + `analyst_review_required: True` flags |
| Reference the composite pilot case study | `docs/case-study/composite-pilot.md` + `agents/ciandlithe/tools/composite_pilot.py` + `baml_src/ciandlithe/case_studies/reform_civil_suit_dossier.baml` |
| Look up the source PDF for a case study | `leabharlann/gemini_deep_research/{law,medical}/<file>.pdf` (read-only context; NOT in this repo) |

## Cross-repo convention

Ciandlithe is a sibling repo to `cianfhoghlaim/cianfhoghlaim` and `cianfhoghlaim/cianchosaint`. The three repos share:

- The openspec workflow (same `openspec/` layout, same `spec-driven` schema, same `proposal.md` + `tasks.md` + spec delta format)
- The 14-layer knowledge sync loop (per the `knowledge-sync-loop` spec — adopted from cianfhoghlaim)
- The 5 dispatchable opencode subagents (`data-platform`, `infrastructure`, `agent-platform`, `frontend-apps`, `research`)
- The `mise.toml` task namespace convention
- The Infisical `dev-baile` vault (ciandlithe lives in its own `ciandlithe/` folder within the vault)
- The MotherDuck + Lakehouse + LanceDB stack (ciandlithe uses the `md:ciandlithe` database namespace, parallel to `md:cianchosaint` and `md:cianfhoghlaim`)

The three repos diverge on:

| | cianfhoghlaim | cianchosaint | ciandlithe |
|---|---|---|---|
| **Domain** | Education (8 nations × 5 stages × bilingual EN+GA) | Defence / policing / intelligence oversight | Civil + administrative + appellate litigation |
| **Licence** | BUSL-1.1 — Cianfhoghlaim edition (broader cultural grant) | BUSL-1.1 v2 — Cianchosaint edition (British-Isles-only OSINT, warrant-to-enforce) | BUSL-1.1 v2 — Ciandlíthe edition (British-Isles-only OSINT, warrant-to-enforce, **+PoI clause**, **+no-auto-submit constraint**) |
| **Provider chain** | LiteLLM-primary | Unsloth Studio primary + 3-tier fallback | Unsloth Studio primary + 3-tier fallback (same as cianchosaint) |
| **Persona surfaces** | Students + teachers + parents | Government analysts (Garda, PSNI, MoD, MET, etc.) | Self-rep claimants + WRC claimants + HSE/NHS complainants + PIAB applicants + inquest parties + coroner's-court applicants + legal-aid applicants |
| **Vertical pipelines** | 8 LC subjects | BIPP v1 + BIDP v1 + BIIP v1 | BLIP v1 (single umbrella) |
| **Canonical pilot** | NCCA LC Irish + Mathematics | Reform UK + Richard Tice debt fraud | QUB/RVH brain-injury + Eric employer-breach + Garda data-access + DkIT/NUIG education + UCL admission + sodium valproate / HSE misprescription (composite) |

## Composite pilot reference

The 7 composite-pilot parties (all driven from `leabharlann/gemini_deep_research/law/` + `medical/` PDFs as read-only context — NOT from the private `stedding/private_case_evidence/` folders):

1. **QUB / Royal Victoria Hospital brain-injury** (medical_malpractice, NI) — `law/qub_royal_victoria_malpractice.pdf` + `medical/misdiagnosis_brain_damage_recovery.pdf` + `law/maximizing_civil_suit_damages_against_qub.pdf`
2. **Eric (employer / breach of contract)** (employer_breach, Cross-border NI ↔ ROI) — `law/suing_ceo_for_breach_abuse_damages.pdf` + `law/cross_border_legal_action_research.pdf` + `law/monroes.pdf`
3. **Garda discrimination / data-access** (garda_discrimination, ROI) — `law/garda_discrimination_lawsuit_preparation.pdf` + `law/garda_data_and_accommodation_request.pdf` + `law/garda_brutality_dual_citizenship_and_justice.pdf`
4. **DkIT disability / education complaint** (education_discrimination, ROI) — `law/discrimination_case_strategy_university_of_galway.pdf` + `law/cbd_discrimination_lawsuit_preparation.pdf` + `law/challenging_university_rejection_and_ombudsman_decision.pdf`
5. **NUIG / UoG rejection + abuse of power** (education_discrimination, ROI) — `law/discrimination_case_strategy_university_of_galway.pdf` + `law/cbd_dispensary_manager_discrimination_lawsuit.pdf`
6. **UCL offer / DBS** (admission_breach, England) — `law/ucl_sar_equality_act_claim.pdf`
7. **Sodium valproate / HSE misprescription** (medical_malpractice, ROI) — `medical/irish_sodium_valproate_inquiry_and_healthcare.pdf` + `medical/sodium_valproate_lawsuits_and_inquiries.pdf` + `medical/essential_tbi_medication.pdf`

The composite pilot validates the workflow end-to-end before any expansion. See `docs/case-study/composite-pilot.md` for the canonical narrative.

## Cross-references

- [`LICENSE.md`](LICENSE.md) — the load-bearing legal document (BUSL-1.1 v2 CIANDLITHE edition)
- [`openspec/AGENTS.md`](openspec/AGENTS.md) — the openspec workflow
- [`openspec/specs/ciandlithe-pipeline/spec.md`](openspec/specs/ciandlithe-pipeline/spec.md) — the umbrella capability spec
- [`docs/case-study/composite-pilot.md`](docs/case-study/composite-pilot.md) — the canonical pilot narrative
- [`docs/USAGE-GUIDELINES.md`](docs/USAGE-GUIDELINES.md) — the OSINT ceiling + the no-auto-submit constraint in operational terms
- [`docs/HOW-BRITISH-ISLES-LITIGATION-ENTITIES-USE-CIANDLITHE.md`](docs/HOW-BRITISH-ISLES-LITIGATION-ENTITIES-USE-CIANDLITHE.md) — the audience-targeted use guide

## OpenSpec

This repository uses [OpenSpec](https://github.com/Fission-AI/OpenSpec) for spec-driven change management. Every non-trivial change lives in `openspec/changes/<id>/` as a 3-artifact bundle (`proposal.md` + `tasks.md` + spec deltas) before any code is written.

```bash
openspec list --specs                   # list all capability specs
openspec list                           # list all pending changes
openspec validate <change-id> --strict  # MUST pass before commit
openspec archive <change-id> --yes      # after deploy
```