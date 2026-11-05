"""Shared hardening for calls that leave the process."""

from __future__ import annotations

import functools
import json
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from typing import Any, Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


class ExternalServiceError(RuntimeError):
    """Raised when an external call fails after the configured retries."""

    def __init__(self, service: str, cause: Exception):
        self.service = service
        self.cause = cause
        super().__init__(f"{service} call failed: {cause}")

    def fallback(self) -> dict[str, Any]:
        return {
            "error": "external_service_unavailable",
            "service": self.service,
            "message": (
                f"The {self.service} is temporarily unavailable. "
                "Please try again shortly."
            ),
            "retryable": True,
        }

    def fallback_json(self) -> str:
        return json.dumps(self.fallback())


def retry_with_backoff(
    *,
    service: str,
    retries: int = 3,
    backoff_factor: float = 1.5,
    timeout: float = 5.0,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Retry an external call with bounded execution time and exponential backoff."""
    if retries < 0:
        raise ValueError("retries must be non-negative")
    if backoff_factor < 0:
        raise ValueError("backoff_factor must be non-negative")
    if timeout <= 0:
        raise ValueError("timeout must be positive")

    def decorate(function: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(function)
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
            last_error: Exception | None = None

            for attempt in range(retries + 1):
                executor = ThreadPoolExecutor(max_workers=1)
                future = executor.submit(function, *args, **kwargs)
                try:
                    return future.result(timeout=timeout)
                except TimeoutError as exc:
                    future.cancel()
                    last_error = TimeoutError(
                        f"{service} call exceeded the {timeout:.0f}-second timeout"
                    )
                except Exception as exc:
                    last_error = exc
                finally:
                    executor.shutdown(wait=False, cancel_futures=True)

                if attempt < retries:
                    time.sleep(backoff_factor * (2**attempt))

            assert last_error is not None
            raise ExternalServiceError(service, last_error) from last_error

        return wrapped

    return decorate
