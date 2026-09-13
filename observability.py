"""Ciandlithe observability surface.

Per the 2026-08-24-dlt-sources-to-multi-repo-scaffold-v1 change
(Phase 2.7 — Langfuse + MLflow per sister repo).

Wires the canonical Langfuse + MLflow observability surface for
ciandlithe (the BI civil-litigation sister repo), per the
`agent-observability` skill conventions:

- Layer 1 — Traces: Langfuse (`@observe` decorator + `langfuse_context`)
- Layer 2 — Experiments: MLflow (run tracking + model registry)
- Layer 3 — Cost + prompt management: Langfuse
- Layer 4 — RAGAS (Dagster `asset_check`)
- Layer 5 — Structured logging: structlog

This module is the per-sister entry point. It lazily imports the
underlying SDKs so the module is importable even when Langfuse +
MLflow are not installed (CI fallback).

Environment variables
---------------------
The Infisical contract (see `.infisical.env`) hydrates the
following env vars at runtime via Locket:

  LANGFUSE_PUBLIC_KEY=infisical://dev-baile/ciandlithe/langfuse/public-key
  LANGFUSE_SECRET_KEY=infisical://dev-baile/ciandlithe/langfuse/secret-key
  LANGFUSE_HOST=https://langfuse.ciandlithe.ie
  MLFLOW_TRACKING_URI=infisical://dev-baile/ciandlithe/mlflow/tracking-uri
  MLFLOW_EXPERIMENT_NAME=ciandlithe-civil-litigation
"""
from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Layer 1 + 3 — Langfuse (traces + cost + prompt management)
# ---------------------------------------------------------------------------


def _make_observe() -> Any:
    """Return the Langfuse `@observe` decorator, or a no-op shim.

    Per the `agent-observability` skill: every LLM-touching call MUST
    be Langfuse-observed. If the Langfuse SDK is unavailable (CI
    without the LANGFUSE_* env vars), the `@observe` decorator is
    still callable as a no-op so the wrapper imports cleanly.
    """
    try:
        from langfuse.decorators import observe as _observe  # type: ignore[import-not-found]

        return _observe
    except ImportError:  # pragma: no cover — CI fallback
        def _noop(name: str | None = None, **kwargs: Any) -> Any:
            def _decorator(fn: Any) -> Any:
                return fn

            return _decorator

        return _noop


observe = _make_observe()


def get_langfuse_client() -> Any:
    """Return a configured Langfuse client, or None when unconfigured.

    The client reads its config from the LANGFUSE_* env vars (hydrated
    via Infisical per the 3-way contract).
    """
    public_key = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
    secret_key = os.environ.get("LANGFUSE_SECRET_KEY", "")
    host = os.environ.get("LANGFUSE_HOST", "https://langfuse.ciandlithe.ie")
    if not public_key or not secret_key:
        logger.debug("get_langfuse_client: LANGFUSE_* env vars not set; returning None")
        return None
    try:
        from langfuse import Langfuse  # type: ignore[import-not-found]

        return Langfuse(
            public_key=public_key,
            secret_key=secret_key,
            host=host,
        )
    except ImportError:  # pragma: no cover
        return None


# ---------------------------------------------------------------------------
# Layer 2 — MLflow (experiments + model registry)
# ---------------------------------------------------------------------------


def get_mlflow_tracking_uri() -> str:
    """Return the MLflow tracking URI for ciandlithe.

    Per the Infisical contract:
      MLFLOW_TRACKING_URI=infisical://dev-baile/ciandlithe/mlflow/tracking-uri
    """
    return os.environ.get(
        "MLFLOW_TRACKING_URI",
        "http://localhost:5000",  # dev fallback
    )


def get_mlflow_experiment_name() -> str:
    """Return the canonical MLflow experiment name for ciandlithe."""
    return os.environ.get("MLFLOW_EXPERIMENT_NAME", "ciandlithe-civil-litigation")


def configure_mlflow() -> None:
    """Configure MLflow with the per-sister tracking URI + experiment name.

    Idempotent. Safe to call multiple times.
    """
    try:
        import mlflow  # type: ignore[import-not-found]

        mlflow.set_tracking_uri(get_mlflow_tracking_uri())
        mlflow.set_experiment(get_mlflow_experiment_name())
        logger.debug(
            "configure_mlflow: tracking_uri=%s experiment=%s",
            get_mlflow_tracking_uri(),
            get_mlflow_experiment_name(),
        )
    except ImportError:  # pragma: no cover - CI fallback
        pass


# ---------------------------------------------------------------------------
# Layer 5 — Structured logging (structlog)
# ---------------------------------------------------------------------------


def configure_structlog() -> None:
    """Configure structlog with the canonical CIANFHOGHLAIM-family JSON output.

    Per the `agent-observability` skill: every sister repo emits
    JSON-formatted structlog events that the central Langfuse +
    MLflow stack can ingest.
    """
    try:
        import structlog  # type: ignore[import-not-found]

        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    except ImportError:  # pragma: no cover - CI fallback
        pass


__all__ = [
    "observe",
    "get_langfuse_client",
    "get_mlflow_tracking_uri",
    "get_mlflow_experiment_name",
    "configure_mlflow",
    "configure_structlog",
]
