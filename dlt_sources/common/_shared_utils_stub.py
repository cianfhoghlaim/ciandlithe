# CIANDLITHE wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
# CIANDLITHE wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/ciandlithe-repo-bootstrap-v2/specs/ciandlithe-bootstrap-v2/spec.md).
# Migrated to ciandlithe: 2026-08-23
# Licence: BUSL-1.1 v2 CIANDLITHE edition (per LICENSE.md)
#
# This file is part of the ciandlithe DLT common helper layer. The
# namespace rename from cianfhoghlaim -> ciandlithe has NOT been
# applied to the body of this file (yet); the wholesale-copy is
# intentionally verbatim so that the diff against the upstream
# cianfhoghlaim/cianfhoghlaim commit is preserved for traceability.
# Subsequent openspec changes will apply namespace refactors
# incrementally as the per-domain pipeline bases (BIPP v1 / BIDP v1 /
# BIIP v1) are constructed.
#
# Per the openspec/changes/ciandlithe-repo-bootstrap-v2/proposal.md:
# "Each migrated file SHALL start with a comment block stating
# `Original: cianfhoghlaim/cianfhoghlaim @ <commit-sha>` and
# `Migrated to ciandlithe: <date>` and `Licence: BUSL-1.1 v2 CIANDLITHE edition (per LICENSE.md)`"
#

"""
cianfhoghlaim.cianfhoghlaim.dlt_sources.common._shared_utils_stub — in-tree replacement
for `shared.utils`.

The `cianfhoghlaim.dlt_sources.http_client` module does
`from shared.utils import (CircuitBreaker, CircuitBreakerOpen,
RateLimiter, RateLimitError, RetryableError)`. The `shared` package
is not in this monorepo, so the import fails. This stub provides
minimal but functional implementations of all five symbols so the
http_client module loads cleanly.
"""
from __future__ import annotations

import time


class CircuitBreakerOpen(Exception):
    """Raised when a circuit breaker rejects a call."""


class RetryableError(Exception):
    """Marker for errors that should be retried."""


class RateLimitError(RetryableError):
    """Raised on HTTP 429 / rate-limit responses."""


class RateLimiter:
    """Simple in-process sliding-window rate limiter.

    Public API (matching the call sites in http_client.py):
        limiter = RateLimiter(max_calls=10, period=1.0)
        limiter.acquire()        # blocks until a slot is free
    """

    def __init__(self, max_calls: int, period: float) -> None:
        self.max_calls = max_calls
        self.period = period
        self._timestamps: list[float] = []

    def acquire(self) -> None:
        now = time.monotonic()
        # Drop timestamps outside the window.
        self._timestamps = [t for t in self._timestamps if now - t < self.period]
        if len(self._timestamps) >= self.max_calls:
            # Sleep until the oldest timestamp expires.
            sleep_for = self.period - (now - self._timestamps[0])
            if sleep_for > 0:
                time.sleep(sleep_for)
            self._timestamps = [t for t in self._timestamps if time.monotonic() - t < self.period]
        self._timestamps.append(time.monotonic())


class CircuitBreaker:
    """Simple in-process circuit breaker.

    Public API:
        breaker = CircuitBreaker(failure_threshold=5, recovery_time=30)
        if not breaker.allow_request():
            raise CircuitBreakerOpen(...)
        try:
            ... do work ...
        except Exception:
            breaker.record_failure()
        else:
            breaker.record_success()
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_time: float = 30.0,
        half_open_max_calls: int = 1,
    ) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.half_open_max_calls = half_open_max_calls
        self._failures = 0
        self._opened_at: float | None = None
        self._half_open_in_flight = 0

    def allow_request(self) -> bool:
        if self._opened_at is None:
            return True
        if time.monotonic() - self._opened_at < self.recovery_time:
            return False
        # Recovery window elapsed — half-open mode.
        if self._half_open_in_flight >= self.half_open_max_calls:
            return False
        self._half_open_in_flight += 1
        return True

    def record_success(self) -> None:
        self._failures = 0
        self._opened_at = None
        self._half_open_in_flight = 0

    def record_failure(self) -> None:
        self._failures += 1
        if self._failures >= self.failure_threshold and self._opened_at is None:
            self._opened_at = time.monotonic()


__all__ = [
    "CircuitBreaker",
    "CircuitBreakerOpen",
    "RateLimitError",
    "RateLimiter",
    "RetryableError",
]
