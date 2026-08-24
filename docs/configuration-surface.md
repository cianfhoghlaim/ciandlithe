# CIANDLITHE — Configuration Surface

> **Per the cianchosaint `configuration-surface.md` precedent** — the per-deployment configuration surface for ciandlithe.

The ciandlithe platform has 7 configuration surfaces. Every deployment footprint (citizen / law-clinic analyst / developer) configures a different subset.

## §1 — `pyproject.toml` (Python package)

Single Python package `ciandlithe`. Depends on:
- `dlt[duckdb]>=1.4.0`
- `dagster>=1.13.0`
- `baml-py>=0.223.0`
- `cocoindex>=1.0.14`
- `lancedb>=0.20.0`
- `duckdb>=1.4.0`
- `motherduck>=0.10.0`
- `pydantic>=2.10.0`
- `structlog>=25.0.0`
- `pyyaml>=6.0.0`
- `langfuse>=4.0.0`

## §2 — `mise.toml` (11 sections, ~25 tasks)

See `mise.toml` for the canonical task surface. The 11 sections:
1. **core** — dev env (sync + install + lint + test + format)
2. **lint** — openspec + licence + drift + skills
3. **sync** — knowledge sync loop (14 layers)
4. **openspec** — validate + archive + list + view
5. **ciandlithe:provider** — 4-tier provider chain health
6. **ciandlithe:browser-tool** — BrowserToolRouter health
7. **ciandlithe:osint** — OSINT allowlist audit + case-study load
8. **ciandlithe:blip:v1** — BLIP v1 milestones m1 / m2 / m3 / ga
9. **ciandlithe:composite-pilot:v1** — composite pilot workflow
10. **ciandlithe:ccc** — CocoIndex Code indexing
11. **ciandlithe:web** — per-persona web app health

## §3 — `package.json` (bun workspace)

Workspaces: `web/apps/*` + `web/packages/*`.

Scripts:
- `ci:openspec:validate-all`
- `ci:lint:license`
- `ci:lint:openspec`
- `ci:lint:skills`
- `ci:lint:drift-docs`
- `ci:test:smoke`

DevDependencies:
- `@fission-ai/openspec`
- `typescript`
- `tsx`
- `turbo`
- `@biomejs/biome`

## §4 — `baml_src/clients.baml` (4-tier client chain)

The 4 LLM clients:
- `Primary` (Unsloth Studio)
- `Fallback` (LiteLLM)
- `Emergency` (MiniMax Token Plan)
- `LastResort` (Gemini API)

## §5 — `baml_src/_shared/provider_router_config.yaml` (per-deployment overrides)

8 British-Isles jurisdiction overrides (IRELAND / NI / SCOTLAND / WALES / ENGLAND / JERSEY / GUERNSEY / IOM) + 7 BLIP v1 cohort overrides (medical_malpractice / civil_litigation_forms / personal_injury_piab_nhs / workplace_relations_wrc_et / hse_nhs_complaints / statutes_si_court_rules / court_judgments_tribunal_decisions).

## §6 — `.infisical.env` (secrets template)

All secrets resolve via `infisical://dev-baile/ciandlithe/<key>` template refs (never committed in cleartext). The corresponding runtime `.env` is gitignored + hydrated by `mise run secrets:init` + the Locket sidecar.

## §7 — `dlt_sources/ciandlithe/common/osint_allowlist.yaml` (the OSINT ceiling)

77+ canonical URLs to British-Isles public-sector litigation bodies (per `LICENSE.md §3.1–§3.7`). Enforced by `mise run lint:license`.

## §8 — `opencode.json` (5 dispatchable subagents)

The 5 subagents per the cianfhoghlaim precedent:
1. **data-platform**
2. **infrastructure**
3. **agent-platform**
4. **frontend-apps**
5. **research**

## §9 — Cross-references

- [`pyproject.toml`](../../pyproject.toml)
- [`mise.toml`](../../mise.toml)
- [`package.json`](../../package.json)
- [`baml_src/clients.baml`](../../baml_src/clients.baml)
- [`baml_src/_shared/provider_router_config.yaml`](../../baml_src/_shared/provider_router_config.yaml)
- [`.infisical.env`](../../.infisical.env)
- [`dlt_sources/ciandlithe/common/osint_allowlist.yaml`](../../dlt_sources/ciandlithe/common/osint_allowlist.yaml)
- [`opencode.json`](../../opencode.json)
- [`docs/USAGE-GUIDELINES.md`](../USAGE-GUIDELINES.md)