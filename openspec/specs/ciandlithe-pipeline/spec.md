# ciandlithe-pipeline Capability

## Purpose

`ciandlithe-pipeline` is the umbrella capability for the `ciandlithe` repo (the British-Isles civil-litigation open-source OSINT data platform). It covers the end-to-end stack from DLT ingestion of public official-government sources through BAML extraction, CocoIndex v1 embedding, LanceDB + DuckLake + MotherDuck storage, to TanStack Start + Convex + AG-UI + CopilotKit per-persona dashboards for self-representing claimants, WRC claimants, HSE/NHS complainants, PIAB applicants, inquest parties, coroner's-court applicants, and legal-aid applicants.

The umbrella subsumes one flagship umbrella pipeline:

- **BLIP v1** — British Isles Litigation Pipeline (~50 cohorts across 7 cohorts × 6-8 sub-nations)

The full platform is OSINT-only by source-enforced construction (allowlist of source URLs in `dlt_sources/ciandlithe/common/osint_allowlist.yaml`), with an additional **Person-of-Interest clause** (`LICENSE.md §5.2`) and a **no-automated-form-submission constraint** (`LICENSE.md §3.8` + `docs/USAGE-GUIDELINES.md`). The licence in `LICENSE.md` is the load-bearing architectural constraint.

## Background

Ciandlithe is a sibling repo to `cianfhoghlaim/cianfhoghlaim` (the education / long-distance learning platform) and `cianfhoghlaim/cianchosaint` (the defence / policing / intelligence-oversight platform). It wholesale-migrates ~30 assets from both upstream repos:

- From cianfhoghlaim: the `dlt_sources/_cross/` and `dlt_sources/common/` helpers, the Ireland/medicine + England/Scotland/Wales/NI medicine DLT sources, the 4 legislation.py stubs, the 14-layer knowledge sync loop, the 5 opencode subagents, the opencode.json + .mcp.json, the `.agents/skills/` SKILL.md files, the `.cocoindex_code/` settings, the cocoindex_flows `_shared/` helpers.
- From cianchosaint: the 9 Ireland/law DLT sources, the 6 Ireland/law BAML files, the 4-tier provider chain (`baml_src/clients.baml` + `baml_src/_shared/provider_router.py`), the 13 compose stacks (`bonneagar/stacks/`), the 3 shared web packages (`web/packages/{ui-kit,auth,db}/`), the openspec workflow convention, the per-persona web-surface pattern, the BUSL-1.1 v2 licence structure.

Ciandlithe diverges from cianfhoghlaim + cianchosaint on:

- **Domain** — civil-litigation (vs education / vs defence / policing / intel)
- **Licence** — BUSL-1.1 v2 CIANDLITHE edition (vs broader cultural grant / vs defence-only OSINT) — adds the PoI clause + the no-auto-submit constraint
- **Vertical** — single umbrella BLIP v1 (vs 8 LC subjects / vs BIPP+BIDP+BIIP combined)
- **Persona surfaces** — claimants + complainants + applicants + counsel + legal-aid (vs students/teachers/parents / vs government analysts)
- **Composite pilot** — QUB/RVH + Eric + Garda + DkIT + NUIG + UCL + sodium valproate (vs Reform UK + Richard Tice debt fraud)
- **Source-of-truth for case studies** — the leabharlann `gemini_deep_research/law/` + `gemini_deep_research/medical/` PDFs (read-only context), NOT the raw evidence folders (those remain in the private `stedding/private_case_evidence/` volume)

## Requirements

### Requirement: Repo skeleton + tightened licence

The system SHALL provide a new repo `cianfhoghlaim/ciandlithe` with the canonical skeleton (AGENTS.md + README.md + pyproject.toml + mise.toml + package.json + openspec/) and a `LICENSE.md` containing the Business Source License 1.1 — CIANDLITHE edition with the Additional Use Grant for British-Isles public-sector litigation bodies, the 3-step foreign-use gate, the Person-of-Interest clause, the no-automated-form-submission constraint, and the warrant-to-enforce clause for every Licencee.

#### Scenario: Licence body contains the 3-step foreign-use gate

- **WHEN** the operator opens `LICENSE.md`
- **THEN** the document SHALL contain a section titled "Conditional foreign use — the 3-step gate"
- **AND** the gate SHALL list STEP 1 (EXPLAIN), STEP 2 (DO US A FAVOUR), and STEP 3 (MAYBE) in that order
- **AND** STEP 2 SHALL list the 4 EXHAUSTIVE exemplars (reciprocal OSINT access, treaty-level cooperation, diplomatic recognition, open-source contribution under AGPL v3.0)

#### Scenario: Licence body contains the warrant-to-enforce clause

- **WHEN** the operator opens `LICENSE.md`
- **THEN** the document SHALL contain a section titled "Warrant to enforce — granted to the Licencees"
- **AND** the section SHALL grant to every body named in the Additional Use Grant (§3.1–§3.7) the right to enforce the licence terms
- **AND** the section SHALL specify the trigger conditions in a separate "Trigger conditions for the warrant-to-enforce" section covering both publicly observable evidence (production deployment, derivative works, source copy-paste) AND credible written complaints

#### Scenario: Licence body contains the Person-of-Interest clause

- **WHEN** the operator opens `LICENSE.md`
- **THEN** the document SHALL contain a section titled "OSINT ceiling + Person-of-Interest clause"
- **AND** §5.2 SHALL prohibit ingestion of identifiable natural persons who are not public officials except under the 3 lawful-basis conditions (voluntary public disclosure + public legal proceeding + GDPR lawful basis)

#### Scenario: Licence body contains the no-automated-form-submission constraint

- **WHEN** the operator opens `LICENSE.md`
- **THEN** the document SHALL contain a section titled "Additional Use Grant" (§3.8)
- **AND** §3.8 SHALL enumerate the permitted Additional Uses (OSINT-driven litigation preparation, inter-jurisdictional research, public-service procurement evaluation, educational training, policy research)
- **AND** §3.8 SHALL NOT include any automated form submission as a permitted use

### Requirement: 4-tier model provider chain

The system SHALL provide a `ModelProviderRouter` module at `baml_src/_shared/provider_router.py` that routes every LLM call through a 4-tier fallback chain: (1) Unsloth Studio local API, (2) LiteLLM Proxy, (3) MiniMax Token Plan, (4) Gemini API. Mirrors the cianchosaint implementation wholesale.

#### Scenario: Primary provider is Unsloth Studio

- **WHEN** a BAML extraction function requests an LLM completion
- **THEN** the `ModelProviderRouter` SHALL first attempt the call against Unsloth Studio at `http://unsloth-serve:8889/api/v1`
- **AND** the call SHALL have a 30-second timeout
- **AND** the response SHALL be logged in Langfuse with the `provider_used` span attribute set to `"unsloth_studio"`

#### Scenario: Fallback to LiteLLM after primary failure

- **WHEN** the Unsloth Studio request fails (HTTP 5xx or timeout)
- **AND** the circuit-breaker for Unsloth Studio is closed
- **THEN** the router SHALL record the failure against Unsloth Studio's circuit-breaker
- **AND** SHALL attempt the call against the LiteLLM Proxy at `https://litellm.ciandlithe.ie`
- **AND** the response SHALL be logged in Langfuse with the `provider_used` span attribute set to `"litellm"`

### Requirement: OSINT source URL allowlist

The system SHALL provide an OSINT allowlist at `dlt_sources/ciandlithe/common/osint_allowlist.yaml` that enumerates every source URL that may be ingested by any DLT source file under `dlt_sources/ciandlithe/`. The allowlist SHALL contain only URLs that point to public-facing pages of British-Isles public-sector litigation bodies (per `LICENSE.md §5.1`).

#### Scenario: CI gate `mise run lint:license` enforces the allowlist

- **WHEN** the developer adds a new DLT source file at `dlt_sources/ciandlithe/**/*.py`
- **AND** the file references a URL not present in `osint_allowlist.yaml`
- **THEN** the `mise run lint:license` CI gate SHALL exit with code 1
- **AND** SHALL emit a structlog error listing the offending URLs

#### Scenario: Allowlist entry points at a British-Isles body

- **WHEN** the operator inspects `osint_allowlist.yaml`
- **THEN** every URL SHALL point at a public-facing page of a body named in `LICENSE.md §3.1–§3.7`
- **AND** no URL shall point at a foreign body (foreign bodies are subject to the 3-step gate in `LICENSE.md §6`)

### Requirement: No-automated-form-submission constraint

The system SHALL provide no agent affordance that submits a form to courts.ie / irishstatutebook.ie / nidirect.gov.uk / scotcourts.gov.uk / judiciary.uk / courtserve.net or any other British-Isles court / tribunal / regulator endpoint. The platform generates a *dossier* (PDF + structured JSON) for manual review by the claimant or their solicitor.

#### Scenario: Every FunctionTool surfaces `analyst_review_required: True`

- **WHEN** the operator invokes any FunctionTool at `agents/ciandlithe/tools/*.py`
- **THEN** the FunctionTool's response SHALL include the `analyst_review_required: bool = True` flag
- **AND** the FunctionTool's response SHALL include the `osint_ceiling_enforced: bool = True` flag

#### Scenario: No per-persona web app exposes an "auto-submit to court" affordance

- **WHEN** the operator opens any per-persona web app at `web/apps/ciandlithe-<persona>/`
- **THEN** the app SHALL offer a "Download dossier (PDF + JSON)" button
- **AND** the app SHALL NOT offer any "Submit to court" / "File on my behalf" / "Send to court registry" affordance

### Requirement: Person-of-Interest clause enforcement

The system SHALL enforce the Person-of-Interest clause (`LICENSE.md §5.2`) at the BAML extraction layer: every BAML extraction function MUST include an `osint_ceiling_enforced: bool = True` field in its return schema. Any extraction that surfaces a non-allowlisted source URL or a named private individual (not a public official) MUST fail the extraction.

#### Scenario: BAML extraction names a private individual → extraction fails

- **WHEN** a BAML extraction function returns a result that names a private individual (not a public official)
- **THEN** the extraction SHALL set `osint_ceiling_enforced = False`
- **AND** the FunctionTool wrapper SHALL mark the result as `analyst_review_required = True`
- **AND** the per-persona web app SHALL display a warning banner and SHALL NOT auto-render the named individual in any shared view

### Requirement: BLIP v1 sub-pipeline (British Isles Litigation Pipeline)

The system SHALL provide the BLIP v1 sub-pipeline ingesting 7 cohorts × 6-8 jurisdictions = ~50 cohorts. The 7 cohorts are civil-litigation forms, medical-malpractice / clinical-negligence, personal injury / PIAB / NHS-litigation, workplace-relations / WRC / ET, HSE / NHS complaints, statutes + SIs + court rules, and court judgments + tribunal decisions. The 6-8 jurisdictions are Republic of Ireland, Northern Ireland, Scotland, Wales, England, Jersey, Guernsey, Isle of Man.

#### Scenario: BLIP v1 milestone gate m1 (Republic of Ireland)

- **WHEN** the operator runs `mise run ciandlithe:blip:v1:m1`
- **THEN** the Ireland sources SHALL be ingested (7 cohorts × 1 jurisdiction = 7 cohorts minimum)
- **AND** the `ireland_litigation_documents_ingested_check` Dagster asset check SHALL pass (cohort count >= 7)
- **AND** the `ireland_litigation_extractions_ragas_check` SHALL pass (RAGAS faithfulness score >= 0.70)
- **AND** the `ireland_litigation_lance_chunks_check` SHALL pass (chunk count >= 7_000)

#### Scenario: BLIP v1 milestone gate m2 (United Kingdom)

- **WHEN** the operator runs `mise run ciandlithe:blip:v1:m2`
- **THEN** the NI / Scotland / Wales / England sources SHALL be ingested (7 cohorts × 4 jurisdictions = 28 cohorts)
- **AND** the `uk_litigation_documents_ingested_check` Dagster asset check SHALL pass (cohort count >= 28)
- **AND** the `uk_litigation_extractions_ragas_check` SHALL pass (RAGAS faithfulness score >= 0.70)
- **AND** the `uk_litigation_lance_chunks_check` SHALL pass (chunk count >= 28_000)

#### Scenario: BLIP v1 milestone gate m3 (Crown Dependencies)

- **WHEN** the operator runs `mise run ciandlithe:blip:v1:m3`
- **THEN** the Jersey / Guernsey / Isle of Man sources SHALL be ingested (7 cohorts × 3 jurisdictions = 21 cohorts)
- **AND** the `crown_dependencies_litigation_documents_ingested_check` Dagster asset check SHALL pass (cohort count >= 21)
- **AND** the `crown_dependencies_litigation_extractions_ragas_check` SHALL pass (RAGAS faithfulness score >= 0.70)
- **AND** the `crown_dependencies_litigation_lance_chunks_check` SHALL pass (chunk count >= 21_000)

#### Scenario: BLIP v1 milestone gate v1 GA (all 8 sub-nations)

- **WHEN** the operator runs `mise run ciandlithe:blip:v1:ga`
- **THEN** all 6-8 jurisdictions SHALL be ingested (7 cohorts × 6-8 jurisdictions = ~50 cohorts)
- **AND** the `all_british_isles_litigation_documents_ingested_check` Dagster asset check SHALL pass (cohort count >= 48)
- **AND** the `all_british_isles_litigation_extractions_ragas_check` SHALL pass (RAGAS faithfulness score >= 0.70)
- **AND** the `all_british_isles_litigation_lance_chunks_check` SHALL pass (chunk count >= 48_000)

### Requirement: Composite pilot workflow

The system SHALL provide a composite pilot workflow exercising all 7 cohorts × 4 jurisdictions via 7 leabharlann PDFs (one per pilot party). The 7 pilot parties are the QUB/RVH brain-injury case, the Eric employer/breach case, the Garda discrimination case, the DkIT disability case, the NUIG rejection case, the UCL admission case, and the sodium valproate misprescription case. Each pilot party → 1 FunctionTool → 1 BAML extraction function → 1 BAML schema class → 1 cross-referenced dossier for analyst review.

#### Scenario: Composite pilot FunctionTool returns a `CompositePilotDossier`

- **WHEN** the operator invokes `composite_pilot_tool(cohort=<cohort>)` with cohort in {medical_malpractice, garda_discrimination, education_discrimination, employer_breach, admission_breach, civil_action_outline}
- **THEN** the FunctionTool SHALL return a `CompositePilotDossier` dict
- **AND** the `osint_ceiling_enforced` field SHALL be set to `True`
- **AND** the `analyst_review_required` field SHALL be set to `True`
- **AND** the `source_pdf_urls` field SHALL contain the corresponding leabharlann PDF URL(s) (read-only context)

#### Scenario: Composite pilot NEVER submits forms

- **WHEN** the composite pilot FunctionTool executes
- **THEN** the FunctionTool SHALL NOT issue any POST/PUT request to courts.ie / irishstatutebook.ie / nidirect.gov.uk / scotcourts.gov.uk / judiciary.uk / courtserve.net or any other court / tribunal / regulator endpoint
- **AND** the FunctionTool SHALL return a dossier (PDF + JSON) for manual review only

### Requirement: OpenSpec workflow convention

The system SHALL follow the cianchosaint openspec workflow convention: every openspec change lives in `openspec/changes/<id>/` as a 3-artifact bundle (`proposal.md` + `tasks.md` + spec deltas) before any code is written.

#### Scenario: Spec directory MUST contain both `spec.md` AND `AGENTS.md`

- **GIVEN** a developer creates `openspec/specs/<new-spec>/spec.md`
- **AND** does NOT create `openspec/specs/<new-spec>/AGENTS.md`
- **WHEN** the developer runs `openspec validate <new-spec> --strict`
- **THEN** the validation SHALL exit with code 1
- **AND** SHALL emit a structlog error pointing at the missing AGENTS.md file

#### Scenario: AGENTS.md longer than 30 lines fails validation

- **GIVEN** a developer's `openspec/specs/<spec-name>/AGENTS.md` exceeds 30 lines
- **WHEN** the developer runs `openspec validate <spec-name> --strict`
- **THEN** the validation SHALL exit with code 1
- **AND** SHALL emit a structlog error stating the line count

### Requirement: Cross-repo openspec sync documentation

The system SHALL require every openspec change touching >1 repo (ciandlithe + cianfhoghlaim + cianchosaint + leabharlann) to include a `cross-repo-sync.md` file at `openspec/changes/<id>/cross-repo-sync.md` listing:

1. The commit plan for each repo
2. The branch name + remote URL for each push target
3. The order of operations (which repo MUST be committed first)

#### Scenario: Cross-repo change omits cross-repo-sync.md fails validation

- **GIVEN** a developer creates `openspec/changes/<id>/` that declares `Affected repos: ciandlithe, cianfhoghlaim`
- **AND** does NOT include `cross-repo-sync.md`
- **WHEN** the developer runs `openspec validate <id> --strict`
- **THEN** the validation SHALL exit with code 1
- **AND** SHALL emit a structlog error pointing at the missing file

#### Scenario: Cross-repo-sync.md specifies the correct commit order

- **GIVEN** a change touches cianfhoghlaim + cianchosaint + ciandlithe
- **WHEN** the developer runs `openspec validate <id> --strict`
- **THEN** the validator SHALL verify that the cross-repo-sync.md file specifies cianfhoghlaim commits BEFORE cianchosaint commits BEFORE ciandlithe commits
- **AND** SHALL exit with code 0 if the order is correct

## Cross-references

- [`../../LICENSE.md`](../../LICENSE.md) — the load-bearing legal document
- [`../../AGENTS.md`](../../AGENTS.md) — the canonical agent routing
- [`../../openspec/AGENTS.md`](../../openspec/AGENTS.md) — the openspec workflow
- [`../../docs/case-study/composite-pilot.md`](../../docs/case-study/composite-pilot.md) — the canonical pilot narrative
- [`./AGENTS.md`](./AGENTS.md) — the per-spec agent routing
- [Sibling spec: cianchosaint-pipeline in cianchosaint](https://github.com/cianfhoghlaim/cianchosaint/blob/main/openspec/specs/cianchosaint-pipeline/spec.md) — the partial pipeline that ciandlithe extends (the 4-tier provider chain + the licence posture + the deployment runbook)
- [Sibling spec: official-law-pipeline in cianfhoghlaim](https://github.com/cianfhoghlaim/cianfhoghlaim/blob/main/openspec/specs/) — the partial law + medicine pipeline that ciandlithe wholesale-migrates