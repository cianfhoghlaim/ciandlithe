<!-- CIANDLITHE build of stagehand stack. Original: n/a (new build). Licence: BUSL-1.1 (per LICENSE.md) -->

# Stagehand

## Overview

Stagehand (https://stagehand.dev/) is a browser automation framework from
Browserbase that uses an LLM to drive a browser via Chrome DevTools Protocol.
The open-source variant runs against a self-hosted Chromium instance; the
commercial Browserbase variant uses Browserbase's cloud fleet.

This stack wires the open-source variant: a Node.js HTTP API (port 3000)
backed by a headless Chromium container (CDP on port 9222). LLM provider
keys come from the Locket sidecar → Infisical `dev-baile` vault.

## Why This Matters for Ciandlithe

Stagehand gives the agent fleet LLM-driven browser automation as a managed
service — a more deterministic alternative to fire-and-forget Firecrawl
calls when the workflow needs login flows, multi-step form interactions,
or DOM-observation-driven decisions. Stagehand is the "agent in the
browser" primitive; Crawl4AI is the "fetch and extract" primitive; the
two complement each other.

## Key Features

- LLM-driven browser automation via the Stagehand SDK
- Headless Chromium sidecar (chromedp/headless-shell, port 9222)
- OpenAI / Anthropic / DeepSeek / Google as the LLM backend
- Optional Browserbase cloud fallback
- Locket-injected secrets (no plaintext in the repo)
- HTTP API on port 3000 with the standard 6 Stagehand operations
  (`/goto`, `/act`, `/extract`, `/observe`, `/close`, `/health`)

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│ INTERNET (Pangolin Enterprise on arm1-oci)                               │
│                                                                          │
│   https://stagehand.ciandlithe.ie/                                     │
│         │                                                                │
│         ▼                                                                │
│   Pangolin private resource target:                                      │
│   http://stagehand:3000                                                  │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ BUNCHLOCH (MacBook M4 Max) — stagehand-net bridge                        │
│                                                                          │
│   ┌─────────────────┐    ws://chromium:9222    ┌─────────────────────┐  │
│   │ stagehand       │ ───────────────────────▶ │ chromium            │  │
│   │ (Node.js, :3000)│                          │ (headless-shell)    │  │
│   └─────────────────┘                          └─────────────────────┘  │
│                                                                          │
│   ┌─────────────────┐                                                    │
│   │ locket sidecar  │ ◀── /templates/secrets.env                         │
│   │ (:9090 health)  │ ◀── /run/secrets/locket (tmpfs)                     │
│   └─────────────────┘                                                    │
└──────────────────────────────────────────────────────────────────────────┘
```

## Deployment

### Docker Compose (Local Development)

```bash
cd bonneagar/stacks/stagehand
cp .env.example .env.local
# edit .env.local with your OPENAI_API_KEY (or leave blank to use Locket)
docker compose up -d
```

### Docker Compose (Production with Locket Secret Injection)

```bash
cd bonneagar/stacks/stagehand
docker compose -f compose.yaml -f sidecar.yaml -f pangolin.yaml up -d
```

### Komodo (GitOps)

Deployed via Komodo on arm1-oci. Komodo syncs from the Forgejo repo and
applies `compose.yaml` + `sidecar.yaml`. No `.env` file is needed —
Locket resolves all secrets from the Infisical `dev-baile` vault at runtime.

## Environment Variables

| Variable                 | Required | Description                                  | Default          |
|:--|:--|:--|:--|
| `OPENAI_API_KEY`         | No       | OpenAI API key (drives Stagehand by default) | —                |
| `ANTHROPIC_API_KEY`      | No       | Anthropic Claude API key                     | —                |
| `DEEPSEEK_API_KEY`       | No       | DeepSeek API key                             | —                |
| `GOOGLE_API_KEY`         | No       | Google Gemini API key                        | —                |
| `BROWSERBASE_API_KEY`    | No       | Browserbase cloud fallback                   | —                |
| `BROWSERBASE_PROJECT_ID` | No       | Browserbase project id                       | —                |
| `STAGEHAND_MODEL`        | No       | Default Stagehand model                      | `gpt-4o`         |
| `STAGEHAND_LOG_LEVEL`    | No       | Log level (`debug`/`info`/`warn`/`error`)    | `info`           |
| `BROWSER_WS_ENDPOINT`    | No       | CDP endpoint override                        | `ws://chromium:9222` |

## Access

- **URL**: `https://stagehand.ciandlithe.ie` (private, Pangolin Member role required)
- **Internal port**: 3000 (Stagehand HTTP API)
- **CDP port**: 9222 (internal only, not exposed via Pangolin)

## Health Check

```bash
docker ps --filter name=stagehand --format "table {{.Names}}\t{{.Status}}"
curl -fs http://localhost:3000/health
```

## Upstream

- **Repository**: https://github.com/browserbasehq/stagehand
- **Documentation**: https://docs.stagehand.dev/
- **Image base**: `chromedp/headless-shell:stable` (the Chromium sidecar)
