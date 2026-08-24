# CIANDLITHE wholesale-copy of cianchosaint/cianchosaint @ main branch.
#
# Original: cianchosaint/cianchosaint (per the openspec/changes/
#   cianchosaint-langfuse-prompt-management-v1/specs/cianchosaint-langfuse-prompt-management/spec.md).
# Migrated to ciandlithe: 2026-08-24
# Licence: BUSL-1.1 v2 CIANDLITHE edition (per LICENSE.md)

"""CIANDLITHE — Langfuse v3 prompt management resolver.

Mirror of the cianchosaint `langfuse_prompt_resolver.py` for the
ciandlithe composite pilot + the per-cohort BAML extractions.

Per `openspec/changes/ciandlithe-langfuse-prompt-management-v1/`
(planned, after ciandlithe-blip-v1 lands).
"""

from __future__ import annotations

import logging
import os
import threading
import time
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


LANGFUSE_HOST = os.environ.get(
    "LANGFUSE_HOST",
    "https://langfuse.ciandlithe.ie",
)
LANGFUSE_PUBLIC_KEY = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
LANGFUSE_SECRET_KEY = os.environ.get("LANGFUSE_SECRET_KEY", "")

CIRCUIT_BREAKER_THRESHOLD = int(os.environ.get("LANGFUSE_CIRCUIT_BREAKER_THRESHOLD", "3"))
CIRCUIT_BREAKER_RESET_SECONDS = int(os.environ.get("LANGFUSE_CIRCUIT_BREAKER_RESET_SECONDS", "60"))

# The canonical prompt names for ciandlithe
CANONICAL_PROMPT_NAMES = {
    "extract_composite_pilot_dossier": "ExtractCompositePilotDossier",
    "extract_court_form": "ExtractCourtForm",
    "extract_court_fee": "ExtractCourtFee",
    "extract_judgement": "ExtractJudgement",
    "extract_court_rule": "ExtractCourtRule",
    "extract_piab_page": "ExtractPIABPage",
    "extract_legal_aid_page": "ExtractLegalAidPage",
    "extract_hse_incident_report": "ExtractHSEIncidentReport",
    "extract_coroner_inquest_finding": "ExtractCoronerInquestFinding",
    "extract_nhs_incident_report": "ExtractNHSIncidentReport",
    "extract_gmc_ftpan_decision": "ExtractGMCFTPANDecision",
    "extract_daily_court_list": "ExtractDailyCourtList",
    "extract_court_judgment": "ExtractCourtJudgment",
    "extract_legal_case_profile": "ExtractLegalCaseProfile",
    "extract_political_graph_relationship": "ExtractPoliticalGraphRelationship",
}


@dataclass
class LangfusePromptHit:
    """One Langfuse prompt resolution result."""

    prompt_name: str
    prompt_version: int | None
    prompt_text: str
    variables: dict[str, Any]
    langfuse_host: str
    resolved_at: str
    fallback_used: bool


@dataclass
class LangfuseCircuitBreaker:
    """3-strike circuit-breaker per Langfuse prompt resolution."""

    fail_threshold: int = CIRCUIT_BREAKER_THRESHOLD
    reset_seconds: float = float(CIRCUIT_BREAKER_RESET_SECONDS)

    failure_count: int = 0
    last_failure_time: float = 0.0
    is_open: bool = False

    def record_failure(self) -> None:
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.fail_threshold:
            self.is_open = True

    def record_success(self) -> None:
        self.failure_count = 0
        self.is_open = False

    def is_open_now(self) -> bool:
        if self.is_open and (time.time() - self.last_failure_time) > self.reset_seconds:
            self.is_open = False
            self.failure_count = 0
        return self.is_open


class LangfusePromptUnavailable(Exception):
    """Raised when Langfuse is unavailable AND no fallback is provided."""


class LangfusePromptResolver:
    """The canonical Langfuse v3 prompt resolver for ciandlithe."""

    def __init__(
        self,
        host: str | None = None,
        public_key: str | None = None,
        secret_key: str | None = None,
        inline_fallbacks: dict[str, str] | None = None,
    ) -> None:
        self.host = host or LANGFUSE_HOST
        self.public_key = public_key or LANGFUSE_PUBLIC_KEY
        self.secret_key = secret_key or LANGFUSE_SECRET_KEY
        self.inline_fallbacks = inline_fallbacks or {}
        self.circuit_breaker = LangfuseCircuitBreaker()
        self._client: Any = None
        self._client_lock = threading.Lock()
        self._last_span: dict[str, Any] = {}

    @property
    def is_configured(self) -> bool:
        return bool(self.public_key) and bool(self.secret_key)

    def _get_client(self) -> Any:
        if self._client is not None:
            return self._client
        with self._client_lock:
            if self._client is not None:
                return self._client
            try:
                from langfuse import Langfuse

                self._client = Langfuse(
                    public_key=self.public_key,
                    secret_key=self.secret_key,
                    host=self.host,
                )
            except ImportError as exc:
                logger.warning("langfuse_sdk_not_installed", extra={"error": str(exc)})
                raise
        return self._client

    def resolve(
        self,
        prompt_name: str,
        variables: dict[str, Any] | None = None,
    ) -> LangfusePromptHit:
        """Resolve a prompt via Langfuse.

        Mirrors the cianchosaint implementation (per cross-repo sync).
        """
        variables = variables or {}
        if self.circuit_breaker.is_open_now():
            return self._fallback(prompt_name, variables)
        if not self.is_configured:
            return self._fallback(prompt_name, variables)
        try:
            client = self._get_client()
            prompt = client.get_prompt(prompt_name)
            prompt_text = prompt.compile(**variables)
            self.circuit_breaker.record_success()
            from datetime import datetime, timezone

            return LangfusePromptHit(
                prompt_name=prompt_name,
                prompt_version=getattr(prompt, "version", None),
                prompt_text=prompt_text,
                variables=variables,
                langfuse_host=self.host,
                resolved_at=datetime.now(timezone.utc).isoformat(),
                fallback_used=False,
            )
        except Exception as exc:  # noqa: BLE001
            self.circuit_breaker.record_failure()
            return self._fallback(prompt_name, variables)

    def _fallback(
        self,
        prompt_name: str,
        variables: dict[str, Any],
    ) -> LangfusePromptHit:
        from datetime import datetime, timezone

        inline_text = self.inline_fallbacks.get(
            prompt_name,
            f"[MISSING_PROMPT_FALLBACK] prompt_name={prompt_name!r}",
        )
        compiled = inline_text
        for k, v in variables.items():
            compiled = compiled.replace(f"{{{{{k}}}}}", str(v))
        return LangfusePromptHit(
            prompt_name=prompt_name,
            prompt_version=None,
            prompt_text=compiled,
            variables=variables,
            langfuse_host="(inline_fallback)",
            resolved_at=datetime.now(timezone.utc).isoformat(),
            fallback_used=True,
        )

    def register_inline_fallback(self, prompt_name: str, prompt_text: str) -> None:
        self.inline_fallbacks[prompt_name] = prompt_text

    def health_check(self) -> dict[str, Any]:
        from datetime import datetime, timezone

        base: dict[str, Any] = {
            "langfuse_host": self.host,
            "is_configured": self.is_configured,
            "circuit_breaker_open": self.circuit_breaker.is_open_now(),
            "circuit_breaker_failure_count": self.circuit_breaker.failure_count,
            "last_span": self._last_span,
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }
        if not self.is_configured:
            base["status"] = "not_configured"
            return base
        if self.circuit_breaker.is_open_now():
            base["status"] = "circuit_breaker_open"
            return base
        try:
            client = self._get_client()
            auth_ok = client.auth_check()
            base["status"] = "ok" if auth_ok else "auth_failed"
            return base
        except Exception as exc:  # noqa: BLE001
            base["status"] = "unreachable"
            base["error"] = str(exc)
            return base

    @staticmethod
    def canonical_prompt_names() -> list[str]:
        return list(CANONICAL_PROMPT_NAMES.keys())

    @staticmethod
    def canonical_baml_function(prompt_name: str) -> str:
        return CANONICAL_PROMPT_NAMES.get(prompt_name, prompt_name)


_DEFAULT_RESOLVER: LangfusePromptResolver | None = None


def get_default_resolver() -> LangfusePromptResolver:
    """Return the canonical singleton LangfusePromptResolver."""
    global _DEFAULT_RESOLVER
    if _DEFAULT_RESOLVER is None:
        _DEFAULT_RESOLVER = LangfusePromptResolver()
    return _DEFAULT_RESOLVER


__all__ = [
    "CANONICAL_PROMPT_NAMES",
    "LANGFUSE_HOST",
    "LangfuseCircuitBreaker",
    "LangfusePromptHit",
    "LangfusePromptResolver",
    "LangfusePromptUnavailable",
    "get_default_resolver",
]