"""Run ten queries and append a cost summary to README.md.

Usage:
    python measure_runtime.py
"""

from __future__ import annotations

import json
from pathlib import Path

from agent import run_agent
from utils.data_loader import get_example_wardrobe

ROOT = Path(__file__).parent
README = ROOT / "README.md"
LOG_PATH = ROOT / "runtime.log"
QUERIES = [
    "vintage graphic tee under $30",
    "90s track jacket in size M",
    "silk slip dress in midi length under $40",
    "platform sneakers size 8",
    "denim jacket under $50",
    "designer ballgown size XXS under $5",
    "cropped cardigan under $35",
    "leather boots size 8",
    "linen shirt under $25",
    "wool coat in size L under $80",
]


def _append_readme(entries: list[dict], average_tokens: float) -> None:
    extract = "\n".join(json.dumps(entry, ensure_ascii=True) for entry in entries[-10:])
    section = (
        "\n\n## Instrumentation\n\n"
        "The following ten JSON lines were appended to `runtime.log` by "
        "`measure_runtime.py`:\n\n```jsonl\n"
        f"{extract}\n```\n"
        "\n## What It Costs\n\n"
        "Cost is measured with the model's reported token counts. "
        "Retrieval-only or fallback runs report zero model tokens.\n\n"
        f"- Total measured tokens: {sum(int(e['tokens_used']) for e in entries[-10:])}\n"
        "- Number of runs: 10\n"
        f"- Arithmetic: total tokens / runs = "
        f"{sum(int(e['tokens_used']) for e in entries[-10:])} / 10 = "
        f"{average_tokens:.2f} tokens per run\n"
    )
    text = README.read_text(encoding="utf-8")
    marker = "\n## Instrumentation\n"
    if marker in text:
        text = text[: text.index(marker)]
    README.write_text(text.rstrip() + section, encoding="utf-8")


def main() -> None:
    before = LOG_PATH.read_text(encoding="utf-8").splitlines() if LOG_PATH.exists() else []
    for query in QUERIES:
        run_agent(query, get_example_wardrobe())

    new_entries = [json.loads(line) for line in LOG_PATH.read_text(encoding="utf-8").splitlines()]
    entries = new_entries[len(before):]
    if len(entries) != 10:
        raise RuntimeError(f"Expected 10 new runtime entries, found {len(entries)}")
    average_tokens = sum(int(entry["tokens_used"]) for entry in entries) / 10
    _append_readme(entries, average_tokens)
    print(f"Recorded {len(entries)} runs; average tokens per run: {average_tokens:.2f}")


if __name__ == "__main__":
    main()
