"""Optional: order search hits by relevance with Jev (TypeSafe) through OpenRouter.

Runs only when OPENROUTER_API_KEY is set; without it, search keeps its keyword order. Only the search topic
and market titles are sent, never a company's or user's numbers. Each hit gets one yes/no question ("does
this market price the topic?") and Jev's probability of yes becomes its `relevance`.
"""
from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor

from .util import http_json

DECISIONS = "https://openrouter.ai/api/alpha/decisions"
DEFAULT_MODEL = "~typesafe/jev-latest"
# Questions per request: keeps requests far below ~32 KB, where Jev switches to its slower long-context mode.
CHUNK = 20
# Hits scored per venue. Keyword hits past this keep their order below the scored ones.
MAX_HITS = 200

TRUE = ("The market resolves on this topic itself: the same race, measure, bill, order or policy, so its price "
        "measures the topic's odds.")
FALSE = "The market is about something else, or only shares words with the topic."


def enabled() -> bool:
    return bool(os.environ.get("OPENROUTER_API_KEY"))


def model() -> str:
    return os.environ.get("ERISK_JEV_MODEL") or DEFAULT_MODEL


def _ask(topic: str, hits: list[dict]) -> tuple[list[float], float]:
    questions = {f"m{i}": {"type": "noul",
                           "instructions": f"Prediction market: {h['title']} {h.get('sub_title', '')}".strip()
                                           + "\nDoes this market price the topic in the state?",
                           "criteria": {"true": TRUE, "false": FALSE}}
                 for i, h in enumerate(hits)}
    res = http_json(DECISIONS, headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
                    body={"model": model(), "state": {"topic": topic}, "questions": questions}, timeout=60)
    answers = res.get("answers") or {}
    scores = [float((answers.get(f"m{i}") or {}).get("noul", 0.0)) for i in range(len(hits))]
    return scores, float((res.get("usage") or {}).get("cost") or 0.0)


def order(topic: str, hits: list[dict]) -> tuple[list[dict], float]:
    """Return (hits with `relevance`, most relevant first; cost in USD). Raises on any API failure."""
    head, tail = hits[:MAX_HITS], hits[MAX_HITS:]
    chunks = [head[i:i + CHUNK] for i in range(0, len(head), CHUNK)]
    with ThreadPoolExecutor(max_workers=4) as pool:
        done = list(pool.map(lambda c: _ask(topic, c), chunks))
    scored = []
    for chunk, (scores, _) in zip(chunks, done):
        scored += [{**h, "relevance": round(s, 3)} for h, s in zip(chunk, scores)]
    scored.sort(key=lambda h: -h["relevance"])  # stable: ties keep keyword order
    return scored + tail, round(sum(cost for _, cost in done), 6)
