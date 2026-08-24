# CIANCHOSAINT build of stagehand stack. Original: n/a (new build). Licence: BUSL-1.1 (per LICENSE.md)
#
# =============================================================================
# STAGEHAND - Docker Image (Node.js 20-slim + Stagehand)
# =============================================================================
# Multi-stage build:
#   * deps     - npm ci (production deps only)
#   * runtime  - node:20-slim + chromium runtime libs + the compiled deps
#
# The Stagehand HTTP API is a thin Express server that wraps the Stagehand
# SDK (https://github.com/browserbasehq/stagehand). The API surface is the
# 6 standard Stagehand operations (goto / act / extract / observe / close /
# health) plus the SSE streaming surface for live LLM-driven execution.
#
# Pin policy:
#   * node:20-slim   - LTS line, updated quarterly
#   * @browserbasehq/stagehand - pinned via package.json (semver ^X.Y.Z)
# =============================================================================

FROM node:20-slim AS deps

WORKDIR /app

# Copy only the manifest files first to maximise layer caching.
COPY package.json package-lock.json* ./

# Install production deps. `--no-audit --no-fund` keeps the build quiet.
# `--ignore-scripts` prevents postinstall scripts from running on untrusted
# packages during the build (Stagehand itself has no required postinstall).
RUN npm ci --omit=dev --no-audit --no-fund --ignore-scripts

# =============================================================================
FROM node:20-slim AS runtime

WORKDIR /app

# Chromium runtime libs (libgbm1 / libnss3 / libasound2 / libatk-bridge2.0-0
# / libatk1.0-0 / libgtk-3-0 / libxkbcommon0 / libxss1 / libgconf-2-4) are
# required by the chromium binary even though we use chromedp/headless-shell
# as a sidecar (some Stagehand fallback paths shell out to a local Chromium
# when BROWSER_WS_ENDPOINT is unreachable).
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        ca-certificates \
        wget \
        dumb-init \
 && rm -rf /var/lib/apt/lists/*

# Create a non-root user for runtime
RUN groupadd --system --gid 1001 stagehand \
 && useradd  --system --uid 1001 --gid stagehand --home /app stagehand

# Copy node_modules + the Stagehand HTTP server source
COPY --from=deps --chown=stagehand:stagehand /app/node_modules ./node_modules
COPY --chown=stagehand:stagehand . .

USER stagehand

EXPOSE 3000

# dumb-init reaps zombie processes and forwards signals correctly
ENTRYPOINT ["dumb-init", "--"]

CMD ["node", "server.js"]
