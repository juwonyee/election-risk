"""Kalshi and Polymarket: search, read one event, and snapshot the markets a company file uses.

Pricing rules (both venues):
  * price = bid/ask midpoint, never the last trade
  * spread over MAX_USABLE_SPREAD -> last trade (quote "last_trade") if it traded, else no price
  * volume under THIN (10,000 contracts on Kalshi, $10,000 on Polymarket) -> low_liquidity
  * ladders ("above $X") are made non-increasing with pool-adjacent-violators
  * mutually exclusive outcomes (races) are normalized to sum to 1; empty placeholder outcomes count as 0
"""
from __future__ import annotations

import json
import urllib.error
import urllib.parse

from . import rerank
from .util import Blocked, cache_dir, fnum, http_json, load_json, log, now_iso, save_json, today

KALSHI = "https://api.elections.kalshi.com/trade-api/v2"
GAMMA = "https://gamma-api.polymarket.com"
VENUES = ("Kalshi", "Polymarket")

# A 0.05/0.99 quote has a meaningless midpoint; 0.25 keeps normal thin markets and drops broken ones.
MAX_USABLE_SPREAD = 0.25
# Below this, one trader can move the price; shown as "thin" everywhere.
THIN = 10_000
PM_TAGS = ["politics", "elections", "us-politics", "midterms", "economy", "economic-policy", "trade", "tariffs"]


# ----------------------------------------------------------------------------- pricing

def _price(bid, ask, last, volume, unit) -> dict:
    mid, spread = None, None
    if bid is not None and ask is not None and ask > 0:
        spread, mid = round(ask - bid, 4), round((bid + ask) / 2, 4)
    if mid is not None and spread <= MAX_USABLE_SPREAD:
        prob, quote = mid, "mid"
    elif last is not None and volume > 0:
        prob, quote = last, "last_trade"
    else:
        prob, quote = None, "none"
    return {"yes_bid": bid, "yes_ask": ask, "last_trade": last, "spread": spread, "quote": quote,
            "prob": prob, "volume": round(volume, 2), "volume_unit": unit, "low_liquidity": volume < THIN}


def pava_decreasing(values: list[float]) -> list[float]:
    """Pool-adjacent-violators for a non-increasing sequence (equal weights)."""
    blocks: list[list[float]] = []
    for v in values:
        blocks.append([v, 1.0])
        while len(blocks) > 1 and blocks[-2][0] / blocks[-2][1] < blocks[-1][0] / blocks[-1][1]:
            s, c = blocks.pop()
            blocks[-1][0] += s
            blocks[-1][1] += c
    out: list[float] = []
    for s, c in blocks:
        out.extend([round(s / c, 4)] * int(c))
    return out


def _finish(event: dict, mutually_exclusive: bool) -> dict:
    markets = event["markets"]
    ladder = [m for m in markets if m.get("strike") is not None and m["prob"] is not None]
    if ladder and len(ladder) == len(markets) and event.get("ladder"):
        ladder.sort(key=lambda m: m["strike"])
        for m, p in zip(ladder, pava_decreasing([m["prob"] for m in ladder])):
            if abs(m["prob"] - p) > 1e-9:
                m["prob"] = p
    if mutually_exclusive:
        priced = [m for m in markets if m["prob"] is not None]
        unpriced_traded = [m for m in markets if m["prob"] is None and m["volume"] > 0]
        total = sum(m["prob"] for m in priced)
        if priced and not unpriced_traded and total > 0 and abs(total - 1) > 1e-9:
            for m in priced:
                m["prob"] = round(m["prob"] / total, 4)
    event["total_volume"] = round(sum(m["volume"] for m in markets), 2)
    event["low_liquidity"] = event["total_volume"] < THIN
    return event


# ----------------------------------------------------------------------------- Kalshi

def kalshi_raw(event: str) -> dict:
    return http_json(f"{KALSHI}/events/{urllib.parse.quote(event)}?with_nested_markets=true")["event"]


def kalshi_event(event: str, mutually_exclusive: bool | None = None) -> dict:
    ev = kalshi_raw(event)
    markets = []
    for m in ev.get("markets", []):
        rec = _price(fnum(m.get("yes_bid_dollars")), fnum(m.get("yes_ask_dollars")),
                     fnum(m.get("last_price_dollars")), fnum(m.get("volume_fp")) or 0.0, "contracts")
        rec.update({"ticker": m.get("ticker"), "outcome": m.get("yes_sub_title"), "title": m.get("title"),
                    "strike": fnum(m.get("floor_strike")), "close_time": m.get("close_time")})
        markets.append(rec)
    ladder = bool(markets) and all(m.get("strike_type") in ("greater", "greater_or_equal")
                                   for m in ev.get("markets", []))
    me = ev.get("mutually_exclusive") if mutually_exclusive is None else mutually_exclusive
    return _finish({"venue": "Kalshi", "event": event, "title": ev.get("title"), "ladder": ladder,
                    "url": f"https://kalshi.com/markets/{(ev.get('series_ticker') or '').lower()}",
                    "markets": markets}, bool(me))


# ----------------------------------------------------------------------------- Polymarket

def pm_get(path: str, **params):
    url = f"{GAMMA}{path}?{urllib.parse.urlencode(params)}" if params else f"{GAMMA}{path}"
    try:
        return http_json(url)
    except urllib.error.HTTPError as e:
        if e.code in (403, 451):
            raise Blocked(f"Polymarket returned HTTP {e.code} from this network (geo-restricted)") from e
        raise


def pm_raw(slug: str) -> dict:
    found = pm_get("/events", slug=slug)
    if not found:
        raise LookupError(f"Polymarket event '{slug}' not found")
    return found[0]


def pm_event(slug: str, mutually_exclusive: bool = False) -> dict:
    ev = pm_raw(slug)
    markets = []
    for m in ev.get("markets", []):
        if m.get("closed"):
            continue
        rec = _price(fnum(m.get("bestBid")), fnum(m.get("bestAsk")), fnum(m.get("lastTradePrice")),
                     fnum(m.get("volumeNum")) or fnum(m.get("volume")) or 0.0, "USD")
        rec.update({"ticker": m.get("slug"), "outcome": m.get("groupItemTitle") or "Yes",
                    "title": m.get("question"), "strike": None, "close_time": m.get("endDate")})
        markets.append(rec)
    return _finish({"venue": "Polymarket", "event": slug, "title": ev.get("title"), "ladder": False,
                    "url": f"https://polymarket.com/event/{slug}", "markets": markets}, mutually_exclusive)


def fetch_event(venue: str, event: str, mutually_exclusive: bool = False) -> dict:
    if venue == "Kalshi":
        return kalshi_event(event, True if mutually_exclusive else None)
    if venue == "Polymarket":
        return pm_event(event, mutually_exclusive)
    raise ValueError(f"unknown venue {venue}")


# ----------------------------------------------------------------------------- search indexes (daily)

def _kalshi_index() -> list[dict]:
    rows, cursor, pages = [], "", 0
    while True:
        q = {"status": "open", "limit": "200"}
        if cursor:
            q["cursor"] = cursor
        data = http_json(f"{KALSHI}/events?{urllib.parse.urlencode(q)}")
        pages += 1
        rows += [{"event": e["event_ticker"], "title": e.get("title", ""), "sub_title": e.get("sub_title", "")}
                 for e in data.get("events", [])]
        cursor = data.get("cursor") or ""
        if pages % 10 == 0:
            log(f"  ...Kalshi index: {len(rows)} events")
        if not cursor or pages > 1000:
            return rows


def _pm_index() -> list[dict]:
    seen: dict[str, dict] = {}

    def page(**q):
        for off in range(0, 3000, 100):  # Gamma refuses offsets past ~2,500 with HTTP 422
            try:
                evs = pm_get("/events", closed="false", limit=100, offset=off, **q)
            except urllib.error.HTTPError as e:
                if e.code == 422:
                    return
                raise
            for e in evs or []:
                seen[e["slug"]] = {"event": e["slug"], "title": e.get("title") or "", "sub_title": "",
                                   "volume": float(e.get("volume") or 0)}
            if not evs or len(evs) < 100:
                return

    page(order="volume", ascending="false")
    for tag in PM_TAGS:
        page(tag_slug=tag)
    return sorted(seen.values(), key=lambda e: -e["volume"])


def load_index(venue: str, refresh: bool = False) -> dict:
    path = cache_dir() / f"{venue.lower()}_index.json"
    if not refresh and path.exists():
        idx = load_json(path)
        if idx.get("built") == today():
            return idx
    log(f"Building today's {venue} index (pages through open events; a few minutes)...")
    idx = {"built": today(), "events": _kalshi_index() if venue == "Kalshi" else _pm_index()}
    save_json(path, idx)
    return idx


def search(words: list[str], anys: list[str], venue: str = "both", prices: bool = False,
           refresh: bool = False, limit: int = 40, about: str | None = None, rerank_hits: bool = True) -> dict:
    """Return {"results": [...], "gaps": [...]} so a blocked venue never hides the other's results.

    With OPENROUTER_API_KEY set (and rerank_hits), hits are ordered by Jev relevance to `about`
    (default: the search words) and the result carries a "rerank" block; on any Jev failure the keyword
    order stays and the failure is listed in gaps.
    """
    out, gaps = [], []
    use_jev = rerank_hits and rerank.enabled()
    topic = about or " ".join(words + anys)
    jev = {"model": rerank.model(), "topic": topic, "scored": 0, "cost_usd": 0.0}
    for v in VENUES:
        if venue not in ("both", v.lower()):
            continue
        try:
            idx = load_index(v, refresh)
        except Blocked as e:
            gaps.append(gap(v, "search", str(e)))
            continue
        except Exception as e:  # network trouble on one venue should not stop the search
            gaps.append(gap(v, "search", f"{type(e).__name__}: {e}"))
            continue
        hits = []
        for e in idx["events"]:
            text = f"{e['title']} {e['sub_title']}".lower()
            if all(w.lower() in text for w in words) and (not anys or any(a.lower() in text for a in anys)):
                hits.append(e)
        n_hits = len(hits)
        if use_jev and hits:
            try:
                hits, cost = rerank.order(topic, hits)
                jev["scored"] += min(len(hits), rerank.MAX_HITS)
                jev["cost_usd"] = round(jev["cost_usd"] + cost, 6)
            except Exception as x:
                gaps.append({"source": "OpenRouter (Jev)", "item": f"{v} relevance order",
                             "reason": f"{type(x).__name__}: {x}",
                             "fix": "Results keep keyword order. Check OPENROUTER_API_KEY and its credits, "
                                    "or rerun with --no-rerank."})
        for i, e in enumerate(hits[:limit]):
            row = {"venue": v, "event": e["event"], "title": e["title"], "sub_title": e.get("sub_title", "")}
            if "relevance" in e:
                row["relevance"] = e["relevance"]
            if prices and i < 15:
                try:
                    ev = fetch_event(v, e["event"])
                    row["markets"] = [{k: m[k] for k in ("ticker", "outcome", "prob", "volume", "volume_unit",
                                                         "low_liquidity")} for m in ev["markets"][:10]]
                except Exception as x:
                    row["error"] = f"{type(x).__name__}: {x}"
            out.append(row)
        log(f"{v}: {n_hits} match(es) in {len(idx['events'])} open events (index {idx['built']})")
    res = {"results": out, "gaps": gaps}
    if jev["scored"]:
        res["rerank"] = jev
    return res


def show(venue: str, event: str) -> dict:
    """One event with prices and the rules text, so the agent can check the market matches the policy."""
    ev = fetch_event(venue, event)
    if venue == "Kalshi":
        raw = kalshi_raw(event)
        rules = {m["ticker"]: (m.get("rules_primary") or "") + " " + (m.get("rules_secondary") or "")
                 for m in raw.get("markets", [])}
    else:
        raw = pm_raw(event)
        rules = {m.get("slug"): m.get("description") or "" for m in raw.get("markets", [])}
    texts = list(dict.fromkeys(r.strip() for r in rules.values() if r.strip()))
    ev["rules"] = texts[0][:3000] if len(texts) == 1 else {k: v.strip()[:1200] for k, v in rules.items()}
    return ev


# ----------------------------------------------------------------------------- snapshots for a company

def gap(source: str, item: str, reason: str) -> dict:
    fix = "Run the same command again later; it only fetches what is missing."
    if "geo-restricted" in reason:
        fix = ("This network cannot reach Polymarket. Results use Kalshi only. If you can reach Polymarket "
               "where you are, run `snapshot` again and its prices will be added.")
    elif "404" in reason or "not found" in reason:
        fix = "Check the ticker or slug with `markets search`; the market may have closed or been renamed."
    return {"source": source, "item": item, "reason": reason, "fix": fix}


def needed_events(markets_file: dict) -> dict[tuple[str, str], bool]:
    """(venue, event) -> mutually_exclusive, for every market the entries use (source and cross-check)."""
    need: dict[tuple[str, str], bool] = {}
    for e in markets_file.get("entries", []):
        mk, race = e.get("market", {}), e.get("type") == "race"
        need[(mk.get("source", "Kalshi"), mk.get("event"))] = race
        cc = mk.get("cross_check")
        if cc:
            need[(cc["source"], cc["event"])] = race
    return need


def snapshot(ws, refresh: bool = False) -> dict:
    """Fetch prices for a company folder into snapshots/<venue>.json. Same-day files are reused."""
    mf = load_json(ws / "markets.json")
    gaps = []
    result = {}
    need = needed_events(mf)
    for venue in VENUES:
        events = {ev: me for (v, ev), me in need.items() if v == venue}
        if not events:
            continue
        path = ws / "snapshots" / f"{venue.lower()}.json"
        snap = load_json(path) if path.exists() else {}
        if refresh or snap.get("as_of_date") != today():
            snap = {"venue": venue, "events": {}}
        missing = [e for e in events if e not in snap.get("events", {})]
        blocked = None
        for ev in missing:
            if blocked:
                gaps.append(gap(venue, ev, blocked))
                continue
            try:
                snap["events"][ev] = fetch_event(venue, ev, events[ev])
                log(f"  ok   {venue} {ev}")
            except Blocked as x:
                blocked = str(x)
                gaps.append(gap(venue, ev, blocked))
            except urllib.error.HTTPError as x:
                gaps.append(gap(venue, ev, f"HTTP {x.code}"))
            except Exception as x:
                gaps.append(gap(venue, ev, f"{type(x).__name__}: {x}"))
        if snap["events"]:
            snap.update({"venue": venue, "fetched_at": snap.get("fetched_at") if not missing else now_iso(),
                         "as_of_date": today()})
            save_json(path, snap)
        result[venue] = {"events": len(snap["events"]), "fetched_now": len(missing)}
    save_json(ws / "gaps.json", {"checked_at": now_iso(), "gaps": gaps})
    return {"snapshots": result, "gaps": gaps}


def load_snapshots(ws) -> dict:
    """(venue, ticker) -> market record with event metadata."""
    out = {}
    for venue in VENUES:
        path = ws / "snapshots" / f"{venue.lower()}.json"
        if not path.exists():
            continue
        snap = load_json(path)
        for ev in snap["events"].values():
            for m in ev["markets"]:
                out[(venue, m["ticker"])] = {**m, "venue": venue, "event": ev["event"], "event_url": ev["url"],
                                             "event_volume": ev["total_volume"], "as_of": snap.get("fetched_at")}
    return out


def dumps(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)
