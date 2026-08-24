# CIANDLITHE — Deployment

> **Per the cianchosaint `DEPLOYMENT.md` precedent** — the canonical deployment procedure for ciandlithe.

The ciandlithe platform has 3 deployment footprints (citizen / law-clinic analyst / developer). This document covers the canonical procedure for each.

## §1 — Pre-flight

Verify your environment:

```bash
mise --version      # >= 2024.x
docker --version    # >= 27.x
docker compose version  # >= 2.x
bun --version       # >= 1.4.x
uv --version        # >= 0.4.x
openspec --version  # 1.4.1
git --version
```

## §2 — The 13 stacks (deploy in order)

| # | Stack | Port | Purpose | Deploy command |
|--:|:--|--:|:--|:--|
| 1 | infisical | 8443 | Secrets management | `cd bonneagar/stacks/infisical && docker compose up -d` |
| 2 | motherduck | (SaaS) | Cloud DuckDB via Postgres endpoint | (SaaS — no deploy) |
| 3 | lakehouse | 3900-3904, 5433, 8181-8182 | Garage S3 + Postgres + Lakekeeper | `cd bonneagar/stacks/lakehouse && docker compose up -d` |
| 4 | litellm | 4000 | LLM gateway | `cd bonneagar/stacks/litellm && docker compose up -d` |
| 5 | unsloth-serve | 8889 | Tier-1 local LLM | `cd bonneagar/stacks/unsloth-serve && docker compose up -d` |
| 6 | langfuse | 3000 | LLM observability | `cd bonneagar/stacks/langfuse && docker compose up -d` |
| 7 | crawl4ai | 11235 | Self-hosted browser scraper | `cd bonneagar/stacks/crawl4ai && docker compose up -d` |
| 8 | stagehand | 11300 | Stagehand + headless Chrome | `cd bonneagar/stacks/stagehand && docker compose up -d` |
| 9 | changedetection | 5000 | Page-change monitor | `cd bonneagar/stacks/changedetection && docker compose up -d` |
| 10 | komodo | 9120 | GitOps deployment orchestrator | `cd bonneagar/stacks/komodo && docker compose up -d` |
| 11 | pangolin | 8443 (alt) | Reverse proxy + identity | `cd bonneagar/stacks/pangolin && docker compose up -d` |
| 12 | locket | (sidecar) | Secret-injection sidecar | (sidecar — bundled with each app) |
| 13 | traefik | 80/443 | Edge proxy + TLS termination | `cd bonneagar/stacks/traefik && docker compose up -d` |

## §3 — The 3 deployment footprints

### §3.1 — Self-hosted citizen footprint (the recommended starting point)

```bash
git clone https://github.com/cianfhoghlaim/ciandlithe
cd ciandlithe
mise install
mise run core
# Open the per-persona web app at http://localhost:7777
```

The `mise run core` task syncs deps + installs + lints + tests + formats. After it succeeds:
```bash
# Choose your per-persona app
cd web/apps/ciandlithe-self-rep && docker compose up -d  # or ciandlithe-wrc, etc.
```

### §3.2 — Law-clinic analyst footprint (cloud deployment)

```bash
# Provision cloud (arm1-oci or Hetzner)
./bonneagar/iac/bootstrap-arm-oci.sh

# Deploy all 13 stacks
for stack in infisical lakehouse litellm unsloth-serve langfuse crawl4ai stagehand changedetection komodo pangolin traefik; do
  cd "bonneagar/stacks/$stack" && docker compose up -d
done

# Deploy all 7 per-persona web apps
for app in ciandlithe-self-rep ciandlithe-wrc ciandlithe-health-complain ciandlithe-piab ciandlithe-coroner ciandlithe-inquest ciandlithe-legal-aid; do
  cd "web/apps/$app" && docker compose up -d
done

# Provision MotherDuck SaaS database
./scripts/motherduck-provision.sh

# Provision Pangolin ingress
./scripts/pangolin-provision.sh

# Provision Cloudflare Workers + Workers AI
./scripts/cloudflare-provision.sh
```

### §3.3 — Developer / contributor footprint

```bash
git clone https://github.com/cianfhoghlaim/ciandlithe
cd ciandlithe
mise install
mise run core
# OpenSpec authoring
openspec list --specs
openspec list
openspec validate --all --strict
# CCC indexing
bun run ccc:init
bun run ccc:index
```

## §4 — The CI gates

Every deployment MUST pass these gates before going live:

| Gate | Tool | When |
|---|---|---|
| `openspec validate --all --strict` | openspec CLI | Pre-commit |
| `mise run lint:license` | mise task (Python) | CI |
| `mise run lint:drift-docs` | mise task (Python) | CI |
| `mise run lint:skills` | mise task (Python) | CI |
| `mise run openspec:validate-all` | mise task (CLI) | CI |
| `mise run test:smoke` | mise task (pytest) | CI |

## §5 — Cross-references

- [`DEMO-PATHS.md`](DEMO-PATHS.md) — the 3 demo paths
- [`LIVE-DEPLOYMENT-PLAN.md`](LIVE-DEPLOYMENT-PLAN.md) — Cloudflare + arm1-oci + MotherDuck SaaS plan
- [`configuration-surface.md`](configuration-surface.md) — the per-deployment configuration surface
- [`LICENSE.md`](../LICENSE.md) — the load-bearing legal document
- [`AGENTS.md`](../AGENTS.md) — canonical agent routing