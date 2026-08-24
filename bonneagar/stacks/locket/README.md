<!-- CIANDLITHE build of locket stack. Original: n/a (new build). Licence: BUSL-1.1 (per LICENSE.md) -->

# Locket

## Overview

Locket is the canonical Python implementation of the **secret-injection
sidecar pattern** used by every other stack in Bonneagar. It runs as a
small (≤80 MB) container that:

1. Reads `infisical://dev-baile/<item>/<key>` references from a
   read-only-mounted template file (`/templates/secrets.env`).
2. Resolves each reference via the Infisical API using Universal Auth
   (client id + client secret from a docker secret).
3. Writes the resolved secrets to a tmpfs at
   `/run/secrets/locket/secrets.env` (mounted into the parent container
   via a shared tmpfs volume).
4. Exposes a FastAPI HTTP API on port 9090 for parent containers that
   prefer **pull-based** secret retrieval over the shared-tmpfs model.

## Why This Matters for Ciandlithe

Locket is the runtime bridge between Infisical (the secret store of
record in the `dev-baile` vault) and every other container in the fleet.
Without Locket, every stack would either (a) bake secrets into the image,
(b) mount a plaintext `.env` file, or (c) reimplement the resolution
loop. Locket centralises the auth + resolution + audit story in one
auditable Python service.

## Key Features

- **Infisical Universal Auth** — client_id + client_secret via docker secret
- **File-based mode** — template → tmpfs export loop (the default consumer pattern)
- **HTTP API mode** — `/health`, `/ready`, `/secrets/resolve`, `/secrets/export`
- **Tmpfs isolation** — secrets never touch disk; tmpfs mode 700 uid=65532
- **Read-only rootfs** — no write paths inside the container except tmpfs mounts
- **Structured logging** — structlog JSON output, ready for Langfuse ingestion
- **Fallback file** — `--fallback-file` allows offline operation when
  Infisical is unreachable (the contents of the fallback file override
  any `infisical://` reference)

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│ CONSUMER STACK (e.g. stagehand)                                          │
│                                                                          │
│   sidecar.yaml mounts:                                                   │
│     * ./secrets.env  → /templates/secrets.env:ro                         │
│     * docker secret infisical_secret → /run/secrets/infisical_secret     │
│     * tmpfs stack-secrets  → /run/secrets/locket                         │
│                                                                          │
│   parent container reads:                                                │
│     * env_file: /run/secrets/locket/secrets.env (auto-resolved)          │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ LOCKET SIDECAR                                                           │
│                                                                          │
│   ┌──────────────────────────────────────────────────────────────────┐   │
│   │ Python 3.12 / FastAPI / uvicorn (PID 1 under tini)               │   │
│   │                                                                  │   │
│   │   loop:                                                          │   │
│   │     1. Read /templates/secrets.env                               │   │
│   │     2. POST /api/v3/secrets/raw to Infisical for each key        │   │
│   │     3. Write resolved env to /run/secrets/locket/secrets.env     │   │
│   │     4. (mode=watch) sleep 30s + repeat on file mtime change     │   │
│   │                                                                  │   │
│   │   HTTP API (always on, port 9090):                               │   │
│   │     GET  /health          liveness probe                         │   │
│   │     GET  /ready           readiness probe (Infisical reachable?)  │   │
│   │     GET  /secrets/resolve?uri=infisical://...  resolve one       │   │
│   │     GET  /secrets/export  return all resolved secrets as env     │   │
│   │     GET  /metrics         prometheus-style counters              │   │
│   └──────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼  HTTPS (Universal Auth)
┌──────────────────────────────────────────────────────────────────────────┐
│ INFISICAL (`dev-baile` environment)                                      │
│                                                                          │
│   POST /api/v3/secrets/raw/{secretKey}?workspaceId=...&environment=dev   │
│   GET  /api/v3/auth/universal-auth/login                                 │
└──────────────────────────────────────────────────────────────────────────┘
```

## Deployment

### Docker Compose (Standalone — for verification)

```bash
cd bonneagar/stacks/locket
cp .env.example .env.local  # documented in Environment Variables below
docker compose up -d
curl -fs http://localhost:9090/health
curl -fs http://localhost:9090/ready
```

### As a Sidecar to Another Stack

The consumer stack's `sidecar.yaml` brings up Locket against the
Infisical service. The contract is:

```yaml
services:
  locket:
    image: ciandlithe/locket:local
    user: "65532:65532"
    # ... (see any of the 11 other stacks' sidecar.yaml for the full block)
  <consumer>:
    depends_on:
      locket:
        condition: service_healthy
    env_file:
      - /run/secrets/locket/secrets.env
```

## Environment Variables

| Variable                  | Required | Description                                       | Default                              |
|:--|:--|:--|:--|
| `INFISICAL_URL`           | Yes      | Infisical base URL                                | `http://infisical-backend:8080`      |
| `INFISICAL_ENVIRONMENT`   | No       | Infisical environment slug                        | `dev`                                |
| `INFISICAL_PROJECT_ID`    | No       | Infisical project id (overrides name resolution)  | —                                    |
| `INFISICAL_CLIENT_ID`     | Yes      | Universal Auth client id (from docker secret)     | —                                    |
| `LOCKET_BIND_ADDR`        | No       | HTTP API bind address                             | `0.0.0.0:9090`                       |
| `LOCKET_LOG_LEVEL`        | No       | Log level (`debug`/`info`/`warn`/`error`)         | `info`                               |
| `LOCKET_MODE`             | No       | `once` / `watch` / `exec`                         | `watch`                              |
| `INFISICAL_FALLBACK_FILE` | No       | Path to offline fallback env file                 | `/run/secrets/locket/env-fallback.env` |

## Access

- **HTTP API** (internal): `http://locket:9090/{health,ready,secrets/...}`
- **HTTP API** (Pangolin, admin-only): `https://locket.ciandlithe.ie`
- **File-based secrets**: `/run/secrets/locket/secrets.env` (tmpfs, mode 700)

## Health Check

```bash
docker ps --filter name=locket --format "table {{.Names}}\t{{.Status}}"
curl -fs http://localhost:9090/health
curl -fs http://localhost:9090/ready
```

## Security Model

Per the Locket Sidecar Contract in `infrastructure-stacks/spec.md`:

| Control             | Value                                              |
|:--|:--|
| User                | `65532:65532` (nobody:nogroup)                     |
| `no-new-privileges` | `true`                                             |
| `cap_drop`          | `ALL`                                              |
| `read_only`         | `true`                                             |
| tmpfs `/run/secrets` | `size=1m,mode=0700,uid=65532,gid=65532`            |
| Client secret       | docker secret, never env var                       |

The Infisical client secret NEVER appears in `docker inspect` output,
shell history, or process listing. It is mounted as
`/run/secrets/infisical_secret` (mode 0400) and read by Locket via
`file:` URI.

## Source

- **Repository**: `bonneagar/stacks/locket/` (this directory)
- **Python source**: `app.py` (single-file FastAPI app, ≤400 LoC)
- **Pattern contract**: `openspec/specs/infrastructure-stacks/spec.md`
  (the Locket Sidecar Contract section)
