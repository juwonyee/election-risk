"""Shared helpers: HTTP, paths, formatting. Standard library only."""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO_URL = "github.com/juwonyee/election-risk"
USER_AGENT = "election-risk/1.0 (+https://github.com/juwonyee/election-risk)"
DISCLAIMER = (
    "Analyst draft for human review. Scenario estimates, not investment advice or a recommendation "
    "to trade any security or contract. Prediction-market prices are shown as information only."
)


class Blocked(Exception):
    """A source refused this network (geo-restriction or similar). Never work around it."""


def http_json(url: str, headers: dict | None = None, retries: int = 3, timeout: int = 30, body=None):
    """GET, or POST `body` as JSON when given."""
    h = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if body is not None:
        h["Content-Type"] = "application/json"
    h.update(headers or {})
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, headers=h)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            # 429: rate limited. Three tries with 2s, 4s backoff clears Kalshi's and Gamma's limits in practice.
            if e.code == 429 and attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
                continue
            raise
        except (urllib.error.URLError, OSError):  # connection resets and timeouts
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
                continue
            raise
    raise RuntimeError("unreachable")


def fnum(v) -> float | None:
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def today() -> str:
    return dt.datetime.now(dt.timezone.utc).date().isoformat()


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


# ----------------------------------------------------------------------------- paths

def out_root() -> Path:
    """Where results go: ./election-risk-out in the user's working directory (override with ERISK_OUT)."""
    return Path(os.environ.get("ERISK_OUT", "election-risk-out"))


def workspace(company: str) -> Path:
    """A company folder: an existing path, or a name under election-risk-out/ (e.g. SO)."""
    p = Path(company)
    if "/" in company or os.sep in company or (p / "markets.json").exists():
        return p
    return out_root() / company


def cache_dir() -> Path:
    d = Path(os.environ.get("ERISK_CACHE", Path.home() / ".cache" / "election-risk"))
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_json(p: Path):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def save_json(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def stdout_utf8() -> None:
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8")


def log(msg: str) -> None:
    print(msg, file=sys.stderr)


# ----------------------------------------------------------------------------- formatting

def fmt_money(x: float, signed: bool = True) -> str:
    sign = "−" if x < 0 else ("+" if signed and x > 0 else "")
    a = abs(x)
    if a >= 1e9:
        s = f"${a / 1e9:.2f}B" if a < 1e10 else f"${a / 1e9:.1f}B"
    elif a >= 1e6:
        s = f"${a / 1e6:.0f}M" if a >= 1e8 else f"${a / 1e6:.1f}M"
    elif a >= 1e3:
        s = f"${a / 1e3:.0f}K" if a >= 1e5 else f"${a / 1e3:.1f}K"
    else:
        s = f"${a:.0f}"
    return sign + s


def fmt_volume(volume: float, unit: str) -> str:
    return f"${volume:,.0f} traded" if unit == "USD" else f"{volume:,.0f} contracts"
