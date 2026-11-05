"""Structured runtime instrumentation for agent executions."""

from __future__ import annotations

import functools
import json
import time
from datetime import datetime, timezone
from typing import Any, Callable, ParamSpec, TypeVar

import config

P = ParamSpec("P")
R = TypeVar("R")

LOG_PATH = config.ROOT / "runtime.log"


def _status(value: Any) -> str:
    text = json.dumps(value, ensure_ascii=True).lower()
    if "timeout" in text or "timed out" in text:
        return "TIMEOUT"
    if "429" in text or "rate_limit" in text or "rate limit" in text:
        return "RATE_LIMIT"
    if isinstance(value, dict) and value.get("status") == "completed":
        return "SUCCESS"
    if isinstance(value, dict) and value.get("status") == "stopped_error":
        return "ERROR"
    return "SUCCESS"


def _tokens_used() -> int:
    try:
        from generate import token_counts

        return int(token_counts()["total"])
    except (ImportError, KeyError, TypeError, ValueError):
        return 0


def append_entry(
    *,
    raw_input: Any,
    output: Any,
    status: str,
    duration_ms: float,
    tokens_used: int,
) -> None:
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input": raw_input if isinstance(raw_input, str) else json.dumps(raw_input),
        "output": output if isinstance(output, str) else json.dumps(output, ensure_ascii=True),
        "status": status,
        "duration_ms": round(float(duration_ms), 3),
        "tokens_used": int(tokens_used),
    }
    with LOG_PATH.open("a", encoding="utf-8") as log:
        log.write(json.dumps(entry, ensure_ascii=True) + "\n")


def instrument_execution(function: Callable[P, R]) -> Callable[P, R]:
    """Log one complete agent execution without changing its return value."""
    @functools.wraps(function)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
        raw_input = args[0] if args else kwargs.get("query_dict", "")
        before = _tokens_used()
        started = time.perf_counter()
        try:
            result = function(*args, **kwargs)
        except Exception as exc:
            append_entry(
                raw_input=raw_input,
                output=str(exc),
                status=_status(str(exc)),
                duration_ms=(time.perf_counter() - started) * 1000,
                tokens_used=max(0, _tokens_used() - before),
            )
            raise

        append_entry(
            raw_input=raw_input,
            output=result,
            status=_status(result),
            duration_ms=(time.perf_counter() - started) * 1000,
            tokens_used=max(0, _tokens_used() - before),
        )
        return result

    return wrapped
