"""The full list of open markets an analysis reads: Nov 3 election contests and direct policy markets.

`erisk markets pull` writes two plain lists under election-risk-out/_markets/ (one line per event) so an agent
can read every market instead of searching for a few:
  elections.md  contests decided by the Nov 3 vote (winner and control markets; margins, turnout and
                vote-share side markets are dropped). Single House districts go to house-districts.md.
  policy.md     markets whose Yes is a policy, bill, regulator action, tariff or company event.
Volume under MIN_VOLUME is dropped. The pull is cached for the day; --refresh refetches.
"""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.parse

from .markets import KALSHI, MAX_USABLE_SPREAD, pm_get
from .util import Blocked, fnum, http_json, load_json, log, now_iso, out_root, save_json, today

MIN_VOLUME = 1_000
PM_TAGS = ["midterms", "politics", "economy", "business", "tech"]
# US Nov 3 contests: Polymarket tags them; Kalshi settles them on 2026-11-03..10, at the Jan/Feb 2027 seating,
# or a year out on 2027-11-02..04. Foreign elections close on other dates.
PM_ELECTION_TAGS = {"midterms", "nov-4-elections", "house-elections", "senate-midterms", "governor-midterms"}
KALSHI_CLOSE = (("2026-11-03", "2026-11-10"), ("2027-01-01", "2027-02-01"), ("2027-11-02", "2027-11-04"))
SIDE = re.compile(r"margin|vote percent|vote share|share of|turnout|drop out|how many|seats|run for|nominee|"
                  r"primary|recount|concede|be called|debate|endorse|popular vote|combo|closest|2nd place|"
                  r"mention|say|tweet|approval rating|poll|by county|county winner|"
                  r"flip|which states|sweep|split ticket|first called|pending|leave office|wave|tsunami|odds hit|resign|"
                  r"bluest|reddest|within \d|switch|underperform|exit poll|matters most|voters\?|ridership|"
                  r"secretary-general|greenland|exact outcome|governorships|lose the house majority|map used|"
                  r"announce|pull the| & |party (will )?wins? (white|latino|young|black|women|men|independ)|"
                  r"favorite on|closer senate|number of rounds|ap call|outright|tossup|safe republican|biden-trump|"
                  r"minority leader|number of republican|core four|any statewide|on a federal|on-time|"
                  r"independent or 3rd|worst|best tossup|citizenship|leave (the )?(race|house|senate|party|democratic|republican|office|cabinet|administration|ballot)|"
                  r"change parties|trickle|senate seat on|"
                  r"supermajorit|premier|older (wo)?men|silver|trump\+|rally|closer governor", re.I)
# Direct policy markets: the Yes is a law, rule, tariff, regulator or court action, or a government deal.
POLICY = re.compile(r"tariff|tax|bill|act|law|legislat|regulat|ban|banned|moratorium|"
                    r"fda|ftc|fcc|sec|doj|epa|antitrust|merger|block(s|ed)? the|"
                    r"subsid|minimum wage|medicaid|medicare|aca|obamacare|health insurance|drug pric|"
                    r"sanction|usmca|trade (deal|agreement)|executive order|shutdown|reconciliation|"
                    r"budget|price (cap|control)|data ?center|nuclear|drilling|pipeline|ev|tax credit|"
                    r"stablecoin|clarity|genius act|prediction market|sports? betting|gambling|casino|"
                    r"cannabis|marijuana|rate cap|credit card|student loan|rent|zoning|export control|"
                    r"tiktok|section 230|privacy|kids online|supreme court|court rule|ruling|lawsuit|"
                    r"settle|stake in|government stake|nationali[sz]|ballot measure|proposition|referendum|"
                    r"electricity|utility|ratepayer|wildfire|insurance|offshore|lng|oil|coal|solar|wind",
                    re.I)
NOISE = re.compile(r"spend in|card spend|price on|price \(|oil price|production per day|volume sold|capacity at|"
                   r"ad spend|moneyline|budget balance|rental price|market cap|ipo|stock price|earnings|"
                   r"cost growth|which counties|won outright|happen on time", re.I)
NOT_US = re.compile(r"canad(a|ian)(?! tariff)|mexic|brazil|argentin|colombia|peru|chile|venezuel|ecuador|"
                    r"uk|britain|british|england|scotland|germany|german|france|french|spain|spanish|"
                    r"italy|ital|nether|poland|polish|hungar|bulgari|romania|ukrain|russia|israel|netanyahu|"
                    r"knesset|iran|india|japan|korea|china|chinese|taiwan|australia|new south wales|kenya|"
                    r"nigeria|south africa|el salvador|navajo|saxony|scottish|poilievre|honduras|philippin|turkey|turkish|saudi|imran khan|"
                    r"pakistan|eu|european", re.I)
HOUSE_DISTRICT = re.compile(r"\b[A-Z]{2}-\d{1,2}\b")


def _dir():
    return out_root() / "_markets"


def _kalshi() -> list[dict]:
    rows, cursor = [], ""
    while True:
        q = {"status": "open", "limit": "200", "with_nested_markets": "true"}
        if cursor:
            q["cursor"] = cursor
        data = http_json(f"{KALSHI}/events?{urllib.parse.urlencode(q)}", timeout=60)
        for e in data.get("events", []):
            outs = []
            for m in e.get("markets", []):
                if m.get("status") != "active":
                    continue
                b, a = fnum(m.get("yes_bid_dollars")), fnum(m.get("yes_ask_dollars"))
                usable = b is not None and a and a - b <= MAX_USABLE_SPREAD
                px = (b + a) / 2 if usable else fnum(m.get("last_price_dollars")) or None
                outs.append({"label": m.get("yes_sub_title") or m.get("title") or "", "price": px,
                             "volume": fnum(m.get("volume_fp")) or 0.0, "close": (m.get("close_time") or "")[:10]})
            title = e.get("title", "") + (f" | {e['sub_title']}" if e.get("sub_title") else "")
            rows.append({"id": f"kalshi:{e['event_ticker']}", "title": title, "category": e.get("category") or "",
                         "tags": [], "outcomes": outs})
        cursor = data.get("cursor") or ""
        if len(rows) % 2000 < 200:
            log(f"  ...Kalshi: {len(rows)} open events")
        if not cursor:
            return rows


def _polymarket() -> list[dict]:
    seen: dict[str, dict] = {}
    for tag in PM_TAGS:
        cursor = None
        while True:
            q = {"closed": "false", "limit": 100, "tag_slug": tag}
            if cursor:
                q["after_cursor"] = cursor
            data = pm_get("/events/keyset", **q)
            for e in data.get("events", []):
                outs = []
                for m in e.get("markets", []):
                    if m.get("closed") or not m.get("active", True):
                        continue
                    try:
                        px = float(_list(m.get("outcomePrices"))[0])
                    except (IndexError, TypeError, ValueError):
                        px = None
                    outs.append({"label": m.get("groupItemTitle") or m.get("question") or "", "price": px,
                                 "volume": fnum(m.get("volume")) or 0.0, "close": (m.get("endDate") or "")[:10]})
                seen[e["slug"]] = {"id": f"polymarket:{e['slug']}", "title": e.get("title") or "", "category": "",
                                   "tags": [t.get("slug") for t in e.get("tags") or []], "outcomes": outs}
            cursor = data.get("next_cursor")
            if not cursor or not data.get("events"):
                break
        log(f"  ...Polymarket: {len(seen)} open events after tag '{tag}'")
    return list(seen.values())


def _list(v) -> list:
    """Gamma encodes outcomePrices as a JSON-string array."""
    return v if isinstance(v, list) else json.loads(v or "[]")


def classify(ev: dict) -> str | None:
    """'election', 'policy' or None (dropped)."""
    title = ev["title"]
    if sum(o["volume"] for o in ev["outcomes"]) < MIN_VOLUME or SIDE.search(title) or NOISE.search(title):
        return None
    closes = [o["close"] for o in ev["outcomes"] if o["close"]]
    if ev["id"].startswith("kalshi:"):
        if ev["category"] == "Elections":
            us_nov3 = any(lo <= c <= hi for c in closes for lo, hi in KALSHI_CLOSE)
            return "election" if us_nov3 and not NOT_US.search(title) else None
        is_election = False
    else:
        tags = set(ev["tags"])
        is_election = (bool(tags & PM_ELECTION_TAGS) or any(t.endswith("-midterm") for t in tags)
                       or "referendums-midterms" in tags) and "global-elections" not in tags
        if is_election:
            return "election" if not NOT_US.search(title) else None
        if tags & {"sports", "crypto-prices", "weather", "pop-culture", "global-elections", "world-elections"}:
            return None
    return "policy" if POLICY.search(title) and not NOT_US.search(title) else None


def _line(ev: dict) -> str:
    outs = sorted(ev["outcomes"], key=lambda o: -o["volume"])
    vol = sum(o["volume"] for o in outs)
    top = "; ".join(f"{o['label'][:40]} {o['price']:.2f}" for o in outs[:12] if o["price"] is not None)
    close = max((o["close"] for o in outs if o["close"]), default="")
    return f"{ev['id']} | {ev['title'][:120]} | vol {vol:,.0f} | closes {close} | {top}"


HEADER = {
    "election": ("Nov 3 election markets",
                 "Contests decided by the Nov 3 vote: winner and chamber-control markets. Side markets (margin, "
                 "turnout, vote share) are dropped. Single House districts are in house-districts.md."),
    "house": ("Single House district markets",
              "One line per district. They move policy only through House control; in testing none moved a large "
              "company on its own."),
    "policy": ("Direct policy markets",
               "Markets whose Yes is the policy itself: a bill becoming law, a regulator acting, a tariff, a "
               "moratorium, a court ruling, a company event. Not decided by the Nov 3 vote unless the line says so."),
}


def pull(refresh: bool = False) -> dict:
    d = _dir()
    meta_path = d / "pull.json"
    if not refresh and meta_path.exists() and load_json(meta_path).get("as_of_date") == today():
        return {**load_json(meta_path), "cached": True}
    gaps, events = [], []
    raw_path = d / "raw.json"
    if not refresh and raw_path.exists() and load_json(raw_path).get("as_of_date") == today():
        raw = load_json(raw_path)
        return write_lists(raw["events"], raw.get("gaps", []), raw["pulled_at"])
    log("Pulling every open Kalshi event (about 2 minutes)...")
    try:
        events += _kalshi()
    except Blocked as x:
        gaps.append({"source": "Kalshi", "item": "pull", "reason": str(x)})
    except (urllib.error.URLError, OSError) as x:
        gaps.append({"source": "Kalshi", "item": "pull", "reason": f"{type(x).__name__}: {x}"})
    log("Pulling Polymarket politics, midterms, economy, business and tech events (about 2 minutes)...")
    try:
        events += _polymarket()
    except Blocked as x:
        gaps.append({"source": "Polymarket", "item": "pull", "reason": str(x)})
    except (urllib.error.URLError, OSError) as x:
        gaps.append({"source": "Polymarket", "item": "pull", "reason": f"{type(x).__name__}: {x}"})
    pulled = now_iso()
    save_json(raw_path, {"as_of_date": today(), "pulled_at": pulled, "gaps": gaps, "events": events})
    return write_lists(events, gaps, pulled)


def write_lists(events: list[dict], gaps: list[dict], pulled: str) -> dict:
    d = _dir()
    meta_path = d / "pull.json"
    kinds: dict[str, list[dict]] = {"election": [], "policy": []}
    for ev in events:
        k = classify(ev)
        if k:
            kinds[k].append(ev)
    counts = {}
    for k, evs in kinds.items():
        house = [e for e in evs if k == "election" and HOUSE_DISTRICT.search(e["title"])]
        rest = [e for e in evs if e not in house]
        vol = lambda e: -sum(o["volume"] for o in e["outcomes"])
        parts = [("elections.md" if k == "election" else "policy.md", k, rest)]
        if house:
            parts.append(("house-districts.md", "house", house))
        for name, kind, group in parts:
            title, about = HEADER[kind]
            text = (f"# {title} (open, volume >= {MIN_VOLUME:,}), pulled {pulled}\n\n{about} Kalshi volume = "
                    f"contracts, Polymarket = USD. One line per event: venue:event | title | total volume | last "
                    f"close date | top outcomes with Yes price.\n\n"
                    + "\n".join(_line(e) for e in sorted(group, key=vol)) + "\n")
            d.mkdir(parents=True, exist_ok=True)
            (d / name).write_text(text, encoding="utf-8")
            counts[name] = len(group)
    meta = {"pulled_at": pulled, "as_of_date": today(), "files": {n: str(d / n) for n in counts}, "counts": counts,
            "gaps": gaps}
    save_json(meta_path, meta)
    return meta
