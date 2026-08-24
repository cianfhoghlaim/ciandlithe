# CIANCHOSAINT build of locket stack. Original: n/a (new build). Licence: BUSL-1.1 (per LICENSE.md)
#
# =============================================================================
# LOCKET - Docker Image (Python 3.12-slim + FastAPI + uvicorn)
# =============================================================================
# Multi-stage build:
#   * deps     - pip install --user (no system packages needed)
#   * runtime  - python:3.12-slim + the compiled deps + the locket source
#
# The runtime container:
#   * runs as 65532:65532 (nobody:nogroup)
#   * read_only root filesystem
#   * tmpfs mounts at /run/secrets/locket (secrets) + /tmp (uvicorn workers)
#   * exposes a FastAPI HTTP API on :9090 for parent containers to query
#   * also runs the CLI mode (the file-based template → tmpfs export loop)
#
# Image is intentionally small (~80 MB) — only `fastapi`, `uvicorn`, `httpx`,
# `pydantic`, and `structlog` are installed. No DB drivers, no ML libs.
# =============================================================================

FROM python:3.12-slim AS deps

WORKDIR /build

# Install build deps (none currently needed, but keep the layer for future)
COPY requirements.txt ./
RUN pip install --no-cache-dir --user -r requirements.txt

# =============================================================================
FROM python:3.12-slim AS runtime

WORKDIR /app

# ca-certificates for the Infisical API call, tini for signal forwarding
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        ca-certificates \
        tini \
 && rm -rf /var/lib/apt/lists/*

# Copy the python deps from the deps stage
COPY --from=deps /root/.local /home/locket/.local

# Create the nobody:nogroup user (65532:65532) and the locket CLI shim
RUN groupadd --system --gid 65532 locket \
 && useradd  --system --uid 65532 --gid locket --home /app --shell /usr/sbin/nologin locket \
 && mkdir -p /app /run/secrets/locket /templates \
 && chown -R locket:locket /app /run/secrets/locket

# Copy the Locket source
COPY --chown=locket:locket app.py /app/app.py

# Build the /locket CLI shim (a tiny shell wrapper that execs python -m locket
# is NOT what we want — we want a single static binary-like entrypoint).
# We do this with a one-line shell wrapper that is small + auditable.
RUN printf '#!/bin/sh\nexec python3 /app/app.py "$@"\n' > /locket \
 && chmod 0755 /locket

ENV PATH=/home/locket/.local/bin:/usr/local/bin:/usr/bin:/bin
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

USER locket

EXPOSE 9090

# tini reaps zombie processes and forwards signals correctly
ENTRYPOINT ["/usr/bin/tini", "--"]

# Default: run the CLI mode (template → tmpfs export loop). When the user
# wants the HTTP API only, they can override `command:` in compose.yaml.
CMD ["/locket", "--mode=watch", "--http-addr=0.0.0.0:9090"]
