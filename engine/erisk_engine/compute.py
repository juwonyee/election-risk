"""Market-first math: for each market tied to a company, the yearly profit change if it resolves, and its price.

  direct: if the market resolves Yes, profit changes by impact          price = market
  race:   if candidate X wins, the policy follows with p_policy(X)      price = market per candidate

No expected values are shown: the answer is the size of the swing and what the market says its odds are.

Each result also gets:
  chance          direct: the market price; race: sum over candidates of price to win x p_policy
  election_swing  race: p_policy of the market leader minus the runner-up's (absolute); direct: entry
                  "election.swing" if the agent tied the policy to a Nov 3 contest, else 0
  meaningful      |impact| >= 1% of the base, market volume >= 10,000, chance >= 5%
Headlines: the election headline is the biggest meaningful result with a swing of 0.10 or more; the policy
headline is the biggest meaningful result with a smaller swing. The Red Team list flags weak spots.
"""
from __future__ import annotations

from . import book
from .markets import THIN, load_snapshots
from .util import DISCLAIMER, REPO_URL, fmt_money, load_json, now_iso, save_json

MEANINGFUL_SHARE = 0.01
MEANINGFUL_CHANCE = 0.05
HEADLINE_SWING = 0.10
# Research: an attorney general's party changes suits against companies by 3-11 points (probability table E),
# so a race decided only through `sue` rows cannot move the chance by more than this.
SUE_SWING_CAP = 0.11


def per(imp: dict) -> str:
    """'a year' for a yearly run-rate, 'once' for a one-off amount (impact.one_off)."""
    return "once" if imp.get("one_off") else "a year"


def _quote(m: dict) -> dict:
    return {k: m.get(k) for k in ("venue", "ticker", "prob", "yes_bid", "yes_ask", "quote", "volume", "volume_unit",
                                  "low_liquidity", "event_url", "as_of")}


def _pick(mk: dict, market: dict, ticker: str) -> tuple[dict | None, dict | None, str | None]:
    """Main price and cross-check price. Falls back to the other venue if the main one has no price."""
    src = market.get("source", "Kalshi")
    cc = market.get("cross_check") or {}
    other_t = (cc.get("tickers") or {}).get(ticker)
    main = mk.get((src, ticker))
    other = mk.get((cc.get("source"), other_t)) if other_t else None
    if main and main.get("prob") is not None:
        return main, other, None
    if other and other.get("prob") is not None:
        return other, None, f"{src} price unavailable; using {cc['source']}"
    return None, None, f"no {src} price for {ticker}"


def compute_entry(e: dict, mf: dict, mk: dict) -> tuple[dict | None, str | None]:
    den = mf["denominator"]["amount"]
    imp = e["impact"]
    r = {"id": e["id"], "type": e["type"], "hook": e["hook"], "event_plain": e["event_plain"],
         "market": e["market"], "impact": imp,
         "impact_pct": {k: imp[k] / den for k in ("central", "low", "high")}, "notes": []}
    if e["type"] == "direct":
        main, other, note = _pick(mk, e["market"], e["market"]["yes_ticker"])
        if not main:
            return None, note
        if note:
            r["notes"].append(note)
        r.update({"price": _quote(main), "cross_check": _quote(other) if other else None,
                  "chance": main["prob"], "volume": main.get("event_volume", main["volume"]),
                  "election_swing": float((e.get("election") or {}).get("swing") or 0)})
    else:
        outs = []
        for o in e["market"]["outcomes"]:
            main, other, note = _pick(mk, e["market"], o["ticker"])
            if not main:
                return None, note
            if note:
                r["notes"].append(note)
            if o["p_policy"] > 0 and not o.get("source"):
                r["notes"].append(f"{o['last']}: chance {o['p_policy']:.2f} counted as 0, no source link.")
                o = {**o, "p_policy_given": o["p_policy"], "p_policy": 0.0, "unsourced": True}
            outs.append({**o, "price": _quote(main), "cross_check": _quote(other) if other else None,
                         "if_wins_chance": o["p_policy"]})
        r["outcomes"] = outs
        r["chance_policy_overall"] = r["chance"] = sum(o["price"]["prob"] * o["p_policy"] for o in outs)
        lead = sorted(outs, key=lambda o: -o["price"]["prob"])
        r["election_swing"] = abs(lead[0]["p_policy"] - lead[1]["p_policy"]) if len(lead) > 1 else 0.0
        sue_only = all((o.get("route") or "").startswith("sue") for o in outs if o["p_policy"] > 0)
        if sue_only and any(o["p_policy"] > 0 for o in outs) and r["election_swing"] > SUE_SWING_CAP:
            r["notes"].append(f"Election swing capped at {SUE_SWING_CAP:.2f} from {r['election_swing']:.2f}: "
                              f"attorneys general of both parties bring suits against companies.")
            r["election_swing"] = SUE_SWING_CAP
            r["swing_capped"] = True
        r["volume"] = max(mk.get((o["price"]["venue"], o["price"]["ticker"]), {}).get("event_volume", 0) or
                          o["price"]["volume"] for o in outs)
    r["meaningful"] = (abs(r["impact_pct"]["central"]) >= MEANINGFUL_SHARE and r["volume"] >= THIN
                       and r["chance"] >= MEANINGFUL_CHANCE)
    return r, None


def headlines(results: list[dict]) -> dict:
    ranked = sorted((r for r in results if r["meaningful"]), key=lambda r: -abs(r["impact"]["central"]))
    election = next((r for r in ranked if r["election_swing"] >= HEADLINE_SWING), None)
    policy = next((r for r in ranked if r["election_swing"] < HEADLINE_SWING), None)
    return {"election": election["id"] if election else None, "policy": policy["id"] if policy else None}


def headline_text(r: dict, company: str) -> str:
    pct = f"{r['impact_pct']['central']:+.1%}".replace("-", "−")
    imp = f"{fmt_money(r['impact']['central'])} {per(r['impact'])} ({pct} of profit)"
    if r["type"] == "race":
        a, b = sorted(r["outcomes"], key=lambda o: -o["price"]["prob"])[:2]
        hi, lo = (a, b) if a["p_policy"] >= b["p_policy"] else (b, a)
        if r.get("swing_capped"):
            return (f"{r['event_plain'].rstrip('.')[0].upper()}{r['event_plain'].rstrip('.')[1:]}: "
                    f"{hi['p_policy']:.0%} if {_wins(hi['last'])} ({hi['price']['prob']:.0%} on "
                    f"{hi['price']['venue']}); an attorney general of either party would likely pursue it, so who "
                    f"wins moves the chance by at most {r['election_swing']:.0%}. For {company}: {imp}.")
        return (f"If {_wins(hi['last'])} ({hi['price']['prob']:.0%} on {hi['price']['venue']}), the chance that "
                f"{r['event_plain'].rstrip('.')} is {hi['p_policy']:.0%}, vs {lo['p_policy']:.0%} if "
                f"{_wins(lo['last'])}. For {company}: {imp}.")
    return (f"{r['price']['venue']} puts {r['price']['prob']:.0%} on: {r['event_plain'].rstrip('.')}. "
            f"For {company}: {imp}.")


def red_team(results: list[dict]) -> list[str]:
    """Weak spots a skeptical reviewer would raise. Mechanical checks only; the agent adds its own in notes."""
    out = []
    for r in results:
        name = r["event_plain"].rstrip(".")
        if r["type"] == "race":
            for o in r["outcomes"]:
                if o.get("unsourced"):
                    out.append(f"{name}: {o['last']}'s position has no source link, so its chance "
                               f"{o['p_policy_given']:.2f} was counted as 0.")
            routes = {(o.get("route") or "").split(":")[0].strip() for o in r["outcomes"] if o["p_policy"] > 0}
            if "sue" in routes:
                out.append(f"{name}: research finds an attorney general's party changes suits against companies by "
                           f"only 3-11 points, so the election swing is capped at {SUE_SWING_CAP:.2f}.")
            if "appoint" in routes and r["meaningful"]:
                out.append(f"{name}: research finds a new commission majority moves allowed returns by about 0.15 "
                           f"percentage points; check the impact is sized on that, not on a promised freeze or cut.")
        if r["volume"] < THIN:
            out.append(f"{name}: thin market ({r['volume']:,.0f}); one trader can move the price.")
        lo, hi = sorted(abs(r["impact"][k]) for k in ("low", "high"))
        if lo and hi / lo > 3:
            out.append(f"{name}: the impact range is wide ({fmt_money(r['impact']['low'])} to "
                       f"{fmt_money(r['impact']['high'])}); read how it was built.")
        if r["impact"]["status"] == "estimated" and r["meaningful"]:
            out.append(f"{name}: the impact is an estimate, not a reported number.")
    return out


def _price_text(r: dict) -> str:
    if r["type"] == "direct":
        p, cx = r["price"], r["cross_check"]
        s = f"{p['prob']:.0%} {p['venue']}{' (thin)' if p['low_liquidity'] else ''}"
        return s + (f" · {cx['prob']:.0%} {cx['venue']}" if cx else "")
    outs = r["outcomes"]
    s = " / ".join(f"{o['last']} {o['price']['prob']:.0%}" for o in outs) + f" {outs[0]['price']['venue']}"
    if all(o["cross_check"] for o in outs):
        s += " · " + " / ".join(f"{o['cross_check']['prob']:.0%}" for o in outs) + f" {outs[0]['cross_check']['venue']}"
    return s


def _wins(name: str) -> str:
    """'Becerra wins', 'Democrats win'."""
    return f"{name} {'win' if name.endswith('s') else 'wins'}"


def _what_text(r: dict) -> str:
    if r["type"] == "direct":
        return f"{r['event_plain']} (`{r['market']['event']}`)"
    chances = ", ".join(f"{o['p_policy']:.0%} if {_wins(o['last'])}" for o in r["outcomes"])
    return f"{r['event_plain']}: {chances} (`{r['market']['event']}`)"


def summary_markdown(mf: dict, results: list[dict], gaps: list[dict], heads: dict | None = None,
                     book_info: dict | None = None) -> str:
    c, d = mf["company"], mf["denominator"]
    L = [f"# {c['name']} ({c['ticker']}): what the Nov 3 elections and policy markets could do to its profit", "",
         f"Base: {d['period']} {d['label']} {fmt_money(d['amount'], signed=False)} ({d['status']}).", ""]
    for key, label in (("election", "Election headline"), ("policy", "Policy headline")):
        h = (heads or {}).get(key)
        L.append(f"**{label}:** {h['text'] if h else 'none (no result passes the bar)'}")
    L += ["", "| Market (what resolves) | Price | Chance | If it happens, per year | Share of profit | Election swing "
          "| Meaningful |", "|---|---|---|---|---|---|---|"]
    for r in sorted(results, key=lambda r: -abs(r["impact"]["central"])):
        L.append(f"| {_what_text(r)} | {_price_text(r)} | {r['chance']:.0%} | {fmt_money(r['impact']['central'])} "
                 f"({fmt_money(r['impact']['low'])} to {fmt_money(r['impact']['high'])}) | "
                 f"{r['impact_pct']['central']:+.1%} | {r['election_swing']:.2f} | {'yes' if r['meaningful'] else 'no'} |")
    L += ["", "Meaningful = at least 1% of profit, market volume at least 10,000, chance at least 5%. Election swing = "
          "how much the chance moves with who wins (chances are upper bounds from historical rates)."]
    notes = mf.get("notes") or {}
    if notes.get("locked_in"):
        L += ["", "**Locked in regardless:**"] + [f"- {x}" for x in notes["locked_in"]]
    if notes.get("weak_links"):
        L += ["", "**Weakest links:**"] + [f"- {x}" for x in notes["weak_links"]]
    flags = red_team(results)
    if flags:
        L += ["", "**Red Team:**"] + [f"- {x}" for x in flags]
    if book_info and book_info.get("files"):
        L += ["", f"Policy book: {book_info['source']}, last edited {book_info['last_edit']}, {book_info['files']} "
                  f"contests, fingerprint {book_info['fingerprint']}."]
    if gaps:
        L += ["", "**Not included (could not reach a source):**"]
        L += [f"- {g['source']} `{g['item']}`: {g['reason']}. {g['fix']}" for g in gaps]
    L += ["", "Markets are shown as information only, not as a suggestion to trade.", "", f"*{DISCLAIMER}*", ""]
    return "\n".join(L)


def run(ws) -> dict:
    mf = load_json(ws / "markets.json")
    mk = load_snapshots(ws)
    gaps_path = ws / "gaps.json"
    gaps = list(load_json(gaps_path)["gaps"]) if gaps_path.exists() else []
    results = []
    for e in mf["entries"]:
        r, problem = compute_entry(e, mf, mk)
        if r is None:
            gaps.append({"source": e["market"].get("source"), "item": e["id"], "reason": problem,
                         "fix": "Run `snapshot` again; if it persists, check the ticker with `markets show`."})
            continue
        results.append(r)
    as_of = sorted({q["as_of"] for r in results for q in _quotes(r) if q.get("as_of")})
    heads = headlines(results)
    by_id = {r["id"]: r for r in results}
    out = {"company": mf["company"], "denominator": mf["denominator"], "notes": mf.get("notes") or {},
           "results": results, "gaps": gaps, "prices_as_of": as_of, "generated_at": now_iso(),
           "headlines": {k: {"id": v, "text": headline_text(by_id[v], mf["company"]["short"])} if v else None
                         for k, v in heads.items()},
           "red_team": red_team(results), "book": book.info(),
           "structure": (ws / "structure.md").exists(), "disclaimer": DISCLAIMER, "repo": REPO_URL}
    save_json(ws / "results" / "all.json", out)
    (ws / "summary.md").write_text(summary_markdown(mf, results, gaps, out["headlines"], out["book"]),
                                   encoding="utf-8")
    return out


def _quotes(r: dict) -> list[dict]:
    if r["type"] == "direct":
        return [q for q in (r["price"], r["cross_check"]) if q]
    return [q for o in r["outcomes"] for q in (o["price"], o["cross_check"]) if q]
