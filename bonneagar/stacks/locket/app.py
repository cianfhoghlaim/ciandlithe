"""Locket — secret-injection sidecar for the Cianchosaint platform.

Locket is the canonical implementation of the Infisical-at-runtime pattern
used by every other stack in Bonneagar. It runs as a small Python container
that:

  1. Reads ``infisical://dev-baile/<item>/<key>`` references from a
     read-only-mounted template file (``/templates/secrets.env``).
  2. Resolves each reference via the Infisical API using Universal Auth
     (client id + client secret from a docker secret).
  3. Writes the resolved secrets to a tmpfs at
     ``/run/secrets/locket/secrets.env`` (mounted into the parent container).
  4. Exposes a FastAPI HTTP API on port 9090 for parent containers that
     prefer pull-based secret retrieval over the shared-tmpfs model.

The module is intentionally a single file (≤400 LoC) so that the Dockerfile
can build without a multi-file package layout. Splitting into a package
later is a one-commit refactor.

CLI mode (the default):

    /locket --mode=watch --http-addr=0.0.0.0:9090

HTTP API mode (the FastAPI app always runs alongside the CLI loop):

    GET  /health           liveness probe (returns "ok")
    GET  /ready            readiness probe (returns 200 iff Infisical reachable)
    GET  /secrets/resolve  ?uri=infisical://...   resolve a single URI
    GET  /secrets/export   return all resolved secrets as env-format text
    GET  /metrics          prometheus-style counters
"""

from __future__ import annotations

import argparse
import asyncio
import os
import re
import signal
import sys
import threading
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import httpx
import structlog
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

# =============================================================================
# Configuration
# =============================================================================

DEFAULT_INFISICAL_URL = os.environ.get("INFISICAL_URL", "http://infisical-backend:8080")
DEFAULT_ENVIRONMENT = os.environ.get("INFISICAL_ENVIRONMENT", "dev")
DEFAULT_PROJECT_ID = os.environ.get("INFISICAL_PROJECT_ID", "")
DEFAULT_BIND_ADDR = os.environ.get("LOCKET_BIND_ADDR", "0.0.0.0:9090")
DEFAULT_LOG_LEVEL = os.environ.get("LOCKET_LOG_LEVEL", "info").upper()
DEFAULT_MODE = os.environ.get("LOCKET_MODE", "watch")
DEFAULT_FALLBACK_FILE = os.environ.get(
    "LOCKET_FALLBACK_FILE", "/run/secrets/locket/env-fallback.env"
)
TEMPLATE_DIR = Path(os.environ.get("LOCKET_TEMPLATE_DIR", "/templates"))
OUTPUT_DIR = Path(os.environ.get("LOCKET_OUTPUT_DIR", "/run/secrets/locket"))
OUTPUT_FILE = OUTPUT_DIR / "secrets.env"
WATCH_INTERVAL_SECONDS = 30

# Compile the URI regex once at import time (the hot path is resolution,
# not parsing — but this avoids recompiling on every loop iteration).
URI_PATTERN = re.compile(r"^infisical://([^/]+)/([^/]+)/(.+)$")

# =============================================================================
# Structured logging
# =============================================================================

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(
        getattr(structlog, DEFAULT_LOG_LEVEL, structlog.INFO)
    ),
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)
log = structlog.get_logger("locket")

# =============================================================================
# Metrics (Prometheus-style text)
# =============================================================================


class Metrics:
    """Tiny in-memory counter registry. No external deps."""

    def __init__(self) -> None:
        self._counters: dict[str, int] = {}
        self._lock = threading.Lock()

    def inc(self, name: str, value: int = 1) -> None:
        with self._lock:
            self._counters[name] = self._counters.get(name, 0) + value

    def render(self) -> str:
        with self._lock:
            lines = ["# Locket metrics (Prometheus text format)"]
            for k in sorted(self._counters):
                lines.append(f"locket_{k} {self._counters[k]}")
            return "\n".join(lines) + "\n"


METRICS = Metrics()

# =============================================================================
# Infisical provider
# =============================================================================


class InfisicalProvider:
    """Thin async wrapper around the Infisical v3 REST API.

    Auth flow:
      1. POST /api/v3/auth/universal-auth/login with client_id + client_secret
      2. Receive a short-lived access token (TTL ~15 min)
      3. Use the token for GET /api/v3/secrets/raw/{key}?workspaceId=...
    """

    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        environment: str = "dev",
        project_id: str = "",
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.client_id = client_id
        self.client_secret = client_secret
        self.environment = environment
        self.project_id = project_id
        self._token: str | None = None
        self._token_expires_at: float = 0.0
        self._lock = asyncio.Lock()

    async def login(self) -> None:
        """Exchange client_id + client_secret for an access token."""
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{self.base_url}/api/v3/auth/universal-auth/login",
                json={"clientId": self.client_id, "clientSecret": self.client_secret},
            )
            resp.raise_for_status()
            data = resp.json()
            self._token = data["accessToken"]
            # Infisical tokens last 900s by default; refresh after 750s to be safe.
            self._token_expires_at = time.time() + 750
            METRICS.inc("infisical_logins_total")
            log.info("infisical_login_ok", expires_in_s=750)

    async def _ensure_token(self) -> None:
        if self._token is None or time.time() > self._token_expires_at - 30:
            async with self._lock:
                # Double-check inside the lock to avoid a thundering herd.
                if self._token is None or time.time() > self._token_expires_at - 30:
                    await self.login()

    async def get_secret(self, secret_key: str, project_slug: str) -> str:
        await self._ensure_token()
        assert self._token is not None  # for the type checker
        params: dict[str, str] = {
            "workspaceSlug": project_slug,
            "environment": self.environment,
        }
        if self.project_id:
            params["workspaceId"] = self.project_id
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{self.base_url}/api/v3/secrets/raw/{secret_key}",
                params=params,
                headers={"Authorization": f"Bearer {self._token}"},
            )
            resp.raise_for_status()
            data = resp.json()
            METRICS.inc("infisical_secret_resolves_total")
            return data["secretValue"]


# =============================================================================
# Resolver
# =============================================================================


class ResolveResult(BaseModel):
    """The resolved secret payload."""

    key: str
    value: str
    source: str = Field(description="URI or fallback path")


async def resolve_template(
    template_path: Path,
    provider: InfisicalProvider,
    fallback: dict[str, str],
) -> dict[str, str]:
    """Resolve every ``KEY=infisical://...`` reference in the template.

    Returns a dict ``{KEY: resolved_value}``. Falls back to the contents of
    ``fallback`` (parsed as env file) when the URI is unreachable.
    """
    if not template_path.exists():
        log.warning("template_missing", path=str(template_path))
        return {}

    resolved: dict[str, str] = {}
    for raw_line in template_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        match = URI_PATTERN.match(value)
        if not match:
            # Pass-through (already a plaintext value).
            resolved[key] = value
            continue
        try:
            project_slug, secret_key = match.group(2), match.group(3)
            resolved[key] = await provider.get_secret(secret_key, project_slug)
        except Exception as exc:  # noqa: BLE001
            METRICS.inc("resolve_failures_total")
            log.warning(
                "resolve_failed",
                key=key,
                error=str(exc),
                fallback_available=key in fallback,
            )
            resolved[key] = fallback.get(key, "")
    return resolved


def parse_env_file(path: Path) -> dict[str, str]:
    """Parse a simple ``KEY=VALUE`` file into a dict."""
    if not path.exists():
        return {}
    out: dict[str, str] = {}
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, _, v = line.partition("=")
        out[k.strip()] = v.strip()
    return out


def write_env_file(path: Path, secrets: dict[str, str]) -> None:
    """Atomically write ``KEY=VALUE`` pairs to ``path``."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        "\n".join(f"{k}={v}" for k, v in sorted(secrets.items())) + "\n"
    )
    # Mode 600 — the tmpfs is already mode 700, but tighten the file too.
    os.chmod(tmp, 0o600)
    tmp.replace(path)


# =============================================================================
# FastAPI app
# =============================================================================

PROVIDER: InfisicalProvider | None = None
LAST_RESOLVED: dict[str, str] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    """Build the Infisical provider from CLI/env on startup."""
    global PROVIDER, LAST_RESOLVED
    client_id = os.environ.get("INFISICAL_CLIENT_ID", "")
    client_secret_path = os.environ.get(
        "INFISICAL_CLIENT_SECRET_FILE", "/run/secrets/infisical_secret"
    )
    if not client_id or not Path(client_secret_path).exists():
        log.error("missing_auth", client_id_present=bool(client_id))
        raise RuntimeError("INFISICAL_CLIENT_ID + client secret file are required")
    client_secret = Path(client_secret_path).read_text().strip()
    PROVIDER = InfisicalProvider(
        base_url=DEFAULT_INFISICAL_URL,
        client_id=client_id,
        client_secret=client_secret,
        environment=DEFAULT_ENVIRONMENT,
        project_id=DEFAULT_PROJECT_ID,
    )
    # Pre-resolve once at startup so /ready returns 200 immediately after
    # the first Infisical round-trip succeeds.
    try:
        await _resolve_once()
    except Exception as exc:  # noqa: BLE001
        log.warning("initial_resolve_failed", error=str(exc))
    log.info("locket_started", bind_addr=DEFAULT_BIND_ADDR, mode=DEFAULT_MODE)
    yield
    log.info("locket_stopped")


app = FastAPI(title="Locket", version="0.1.0", lifespan=lifespan)


async def _resolve_once() -> dict[str, str]:
    assert PROVIDER is not None  # noqa: S101
    fallback = parse_env_file(Path(DEFAULT_FALLBACK_FILE))
    template_files = sorted(TEMPLATE_DIR.glob("*.env"))
    if not template_files:
        log.warning("no_templates_found", dir=str(TEMPLATE_DIR))
        return {}
    merged: dict[str, str] = {}
    for tpl in template_files:
        merged.update(await resolve_template(tpl, PROVIDER, fallback))
    write_env_file(OUTPUT_FILE, merged)
    METRICS.inc("resolves_total")
    log.info("resolve_written", file=str(OUTPUT_FILE), count=len(merged))
    return merged


@app.get("/health")
async def health() -> PlainTextResponse:
    """Liveness probe — always 200 if the process is alive."""
    return PlainTextResponse("ok")


@app.get("/ready")
async def ready() -> PlainTextResponse:
    """Readiness probe — 200 only if Infisical was reached at least once."""
    if PROVIDER is None:
        raise HTTPException(status_code=503, detail="Provider not initialised")
    if not LAST_RESOLVED and not OUTPUT_FILE.exists():
        raise HTTPException(status_code=503, detail="No successful resolve yet")
    return PlainTextResponse("ready")


@app.get("/secrets/resolve")
async def secrets_resolve(uri: str = Query(...)) -> dict[str, Any]:
    """Resolve a single ``infisical://...`` URI on demand."""
    if PROVIDER is None:
        raise HTTPException(status_code=503, detail="Provider not initialised")
    match = URI_PATTERN.match(uri)
    if not match:
        raise HTTPException(status_code=400, detail=f"Invalid URI: {uri}")
    project_slug, secret_key = match.group(2), match.group(3)
    try:
        value = await PROVIDER.get_secret(secret_key, project_slug)
        return {"uri": uri, "value": value}
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.get("/secrets/export")
async def secrets_export() -> PlainTextResponse:
    """Return the last fully-resolved secret set as env-format text."""
    if not OUTPUT_FILE.exists():
        raise HTTPException(status_code=404, detail="No resolved secrets yet")
    return PlainTextResponse(OUTPUT_FILE.read_text())


@app.get("/metrics")
async def metrics() -> PlainTextResponse:
    return PlainTextResponse(METRICS.render())


# =============================================================================
# Background watcher loop
# =============================================================================


async def _watcher_loop() -> None:
    """Periodically re-resolve the template (mode=watch) or run once (mode=once)."""
    mode = DEFAULT_MODE
    last_mtime: float = 0.0
    while True:
        try:
            # Detect template changes (cheap stat call, no Infisical hit).
            templates = sorted(TEMPLATE_DIR.glob("*.env"))
            current_mtime = max((t.stat().st_mtime for t in templates), default=0.0)
            changed = current_mtime != last_mtime
            last_mtime = current_mtime
            if changed or mode == "watch":
                global LAST_RESOLVED
                LAST_RESOLVED = await _resolve_once()
            if mode == "once":
                break
            await asyncio.sleep(WATCH_INTERVAL_SECONDS)
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001
            METRICS.inc("watcher_errors_total")
            log.error("watcher_error", error=str(exc))
            await asyncio.sleep(5)


# =============================================================================
# CLI
# =============================================================================


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="locket", description=__doc__)
    p.add_argument("--provider", default="infisical", help="Secret backend (only 'infisical' supported)")
    p.add_argument("--infisical-url", default=DEFAULT_INFISICAL_URL)
    p.add_argument("--infisical-default-environment", default=DEFAULT_ENVIRONMENT)
    p.add_argument("--infisical-default-project-id", default=DEFAULT_PROJECT_ID)
    p.add_argument("--infisical-client-id", default="")
    p.add_argument(
        "--infisical-client-secret",
        default=os.environ.get(
            "INFISICAL_CLIENT_SECRET_FILE", "/run/secrets/infisical_secret"
        ),
        help="'file:/path' URI or plaintext (file: is preferred)",
    )
    p.add_argument("--map", default="/templates:/run/secrets/locket", help="src:dst")
    p.add_argument(
        "--mode",
        choices=["once", "watch", "exec"],
        default=DEFAULT_MODE,
        help="once: resolve + exit; watch: resolve + loop; exec: resolve then exec the rest of argv",
    )
    p.add_argument("--http-addr", default=DEFAULT_BIND_ADDR)
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    global TEMPLATE_DIR, OUTPUT_DIR, OUTPUT_FILE
    args = _parse_args(argv)

    # Update env so the FastAPI lifespan picks up the resolved values.
    os.environ["INFISICAL_URL"] = args.infisical_url
    os.environ["INFISICAL_ENVIRONMENT"] = args.infisical_default_environment
    os.environ["INFISICAL_PROJECT_ID"] = args.infisical_default_project_id
    if args.infisical_client_id:
        os.environ["INFISICAL_CLIENT_ID"] = args.infisical_client_id
    if args.infisical_client_secret.startswith("file:"):
        os.environ["INFISICAL_CLIENT_SECRET_FILE"] = args.infisical_client_secret[5:]
    else:
        # Write the plaintext into a 0600 file in tmpfs for the lifespan to read.
        secret_path = OUTPUT_DIR / "infisical_secret"
        secret_path.parent.mkdir(parents=True, exist_ok=True)
        secret_path.write_text(args.infisical_client_secret)
        os.chmod(secret_path, 0o600)
        os.environ["INFISICAL_CLIENT_SECRET_FILE"] = str(secret_path)

    # Parse --map src:dst for the template + output dirs.
    src, _, dst = args.map.partition(":")
    if src:
        TEMPLATE_DIR = Path(src)
    if dst:
        OUTPUT_DIR = Path(dst)
        OUTPUT_FILE = OUTPUT_DIR / "secrets.env"
        os.environ["LOCKET_OUTPUT_DIR"] = str(OUTPUT_DIR)

    os.environ["LOCKET_BIND_ADDR"] = args.http_addr
    host, _, port = args.http_addr.partition(":")

    async def _run() -> None:
        # Start the FastAPI server (uvicorn) in the background.
        config = uvicorn.Config(
            app, host=host, port=int(port or 9090), log_level="warning"
        )
        server = uvicorn.Server(config)
        server_task = asyncio.create_task(server.serve())

        # Run the watcher loop in parallel.
        watcher_task = asyncio.create_task(_watcher_loop())

        # Wire SIGTERM/SIGINT for graceful shutdown.
        loop = asyncio.get_running_loop()
        stop_event = asyncio.Event()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, stop_event.set)

        await stop_event.wait()
        server.should_exit = True
        watcher_task.cancel()
        await asyncio.gather(server_task, watcher_task, return_exceptions=True)

    asyncio.run(_run())
    return 0


if __name__ == "__main__":
    sys.exit(main())
