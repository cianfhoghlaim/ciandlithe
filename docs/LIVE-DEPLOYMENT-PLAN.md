# CIANDLITHE — Live Deployment Plan

> **Per the cianchosaint `LIVE-DEPLOYMENT-PLAN.md` precedent** — the canonical Cloudflare + arm1-oci + MotherDuck SaaS deployment plan.

## §1 — Cloud architecture

```
                                     ┌─────────────────────────────────────────────┐
                                     │   Cloudflare (ciandlithe.ie)                │
                                     │   - Workers + Workers AI                    │
                                     │   - R2 binding for dossier PDFs             │
                                     │   - Pages for the 7 per-persona web apps    │
                                     └──────────────────┬──────────────────────────┘
                                                        │
                                                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│   Pangolin (reverse proxy + identity) at arm1-oci                    │
│   - ciandlithe.ie → arm1-oci                                        │
│   - litellm.ciandlithe.ie → arm1-oci                                │
│   - langfuse.ciandlithe.ie → arm1-oci                               │
└──────────────────┬──────────────────────────────────────────────────┘
                   │
       ┌───────────┴───────────┐
       │                       │
       ▼                       ▼
┌──────────────────┐    ┌──────────────────────┐
│   13 stacks on   │    │   MotherDuck SaaS     │
│   arm1-oci       │    │   md:ciandlithe       │
│                  │    │   (cloud DuckDB)      │
│ - infisical      │    └──────────────────────┘
│ - lakehouse      │
│ - litellm        │
│ - unsloth-serve  │
│ - langfuse       │
│ - crawl4ai       │
│ - stagehand      │
│ - changedetection │
│ - komodo         │
│ - pangolin       │
│ - locket         │
│ - traefik        │
└──────────────────┘
```

## §2 — DNS

| Domain | Target | Provider |
|---|---|---|
| `ciandlithe.ie` | arm1-oci static IP | Cloudflare |
| `litellm.ciandlithe.ie` | arm1-oci static IP | Cloudflare |
| `langfuse.ciandlithe.ie` | arm1-oci static IP | Cloudflare |
| `unsloth.ciandlithe.ie` | arm1-oci static IP | Cloudflare |

## §3 — Cloudflare Workers

Per-persona web apps deployed as Cloudflare Workers (TanStack Start on Cloudflare Pages + Workers AI for the 4-tier fallback):

- `ciandlithe-self-rep.ciandlithe.ie`
- `ciandlithe-wrc.ciandlithe.ie`
- `ciandlithe-health-complain.ciandlithe.ie`
- `ciandlithe-piab.ciandlithe.ie`
- `ciandlithe-coroner.ciandlithe.ie`
- `ciandlithe-inquest.ciandlithe.ie`
- `ciandlithe-legal-aid.ciandlithe.ie`

Each Worker:
- Reads from the Convex schema (per-persona)
- Calls the BAML FunctionTools via the 4-tier provider chain
- Renders the AG-UI chat window + the per-cohort tab
- Downloads the PDF + JSON dossier to Cloudflare R2

## §4 — MotherDuck SaaS

The `md:ciandlithe` database namespace (parallel to `md:cianfhoghlaim` + `md:cianchosaint`) is the cloud DuckDB destination for the BLIP v1 cohort ingestion.

## §5 — Cloudflare R2 binding

Per-persona dossier PDFs are stored in Cloudflare R2 (the dossier download endpoint).

## §6 — Cross-references

- [`DEPLOYMENT.md`](DEPLOYMENT.md) — the deployment procedure
- [`DEMO-PATHS.md`](DEMO-PATHS.md) — the 3 demo paths
- [`configuration-surface.md`](configuration-surface.md) — per-deployment config