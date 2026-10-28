"""One 16:9 share card (card.svg) for the headline: company, the yearly profit change, the market's odds.

Plain SVG, no fonts or images to fetch, so it opens anywhere and converts to PNG with any browser.
The election headline is used when there is one, else the policy headline; no headline, no card.
"""
from __future__ import annotations

import html
import textwrap

from .util import REPO_URL, fmt_money

W, H = 1600, 900
FONT = "-apple-system,Segoe UI,Inter,Roboto,Helvetica,Arial,sans-serif"


def _text(x, y, s, size, weight=400, fill="#16181d", anchor="start") -> str:
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}">{html.escape(s)}</text>')


def build(data: dict) -> str | None:
    heads = data.get("headlines") or {}
    kind = "election" if heads.get("election") else ("policy" if heads.get("policy") else None)
    if not kind:
        return None
    r = next(x for x in data["results"] if x["id"] == heads[kind]["id"])
    c, imp = data["company"], r["impact"]
    up = imp["central"] >= 0
    color = "#1f7a4d" if up else "#b3372e"
    if r["type"] == "race":
        a, b = sorted(r["outcomes"], key=lambda o: -o["price"]["prob"])[:2]
        hi, lo = (a, b) if a["p_policy"] >= b["p_policy"] else (b, a)
        odds = [f"{hi['last']} {hi['price']['prob']:.0%} to win  ·  then {hi['p_policy']:.0%} chance it happens",
                f"{lo['last']} {lo['price']['prob']:.0%} to win  ·  then {lo['p_policy']:.0%}"]
        venue = hi["price"]["venue"]
        verb = "win" if hi["last"].endswith("s") else "wins"
        if_line = f"If {hi['last']} {verb} and {r['event_plain'].rstrip('.')}"
    else:
        odds = [f"{r['price']['venue']}: {r['price']['prob']:.0%} chance"]
        venue = r["price"]["venue"]
        if_line = f"If {r['event_plain'].rstrip('.')}"
    asof = (data.get("prices_as_of") or [""])[-1].replace("T", " ")[:16]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
             f'<rect width="{W}" height="{H}" fill="#f7f6f2"/>',
             f'<rect x="0" y="0" width="16" height="{H}" fill="{color}"/>',
             _text(90, 120, f"{'ELECTION' if kind == 'election' else 'POLICY'} RISK  ·  NOV 3, 2026", 30, 600, "#626875"),
             _text(90, 210, f"{c['short']} ({c['ticker']})", 72, 750)]
    y = 300
    for line in textwrap.wrap(if_line, 52)[:3]:
        parts.append(_text(90, y, line, 46, 500, "#2a2d34"))
        y += 60
    parts.append(_text(90, y + 110, f"{fmt_money(imp['central'])} {'once' if imp.get('one_off') else 'a year'}", 120, 800, color))
    parts.append(_text(90, y + 175, f"{r['impact_pct']['central']:+.1%} of {data['denominator']['label']}".replace("-", "−", 1), 40, 500,
                       "#626875"))
    oy = y + 260
    for line in odds:
        parts.append(_text(90, oy, line, 36, 500))
        oy += 50
    parts.append(_text(90, H - 60, f"{venue} prices as of {asof} UTC  ·  scenario estimate, not investment advice",
                       26, 400, "#626875"))
    parts.append(_text(W - 80, H - 60, REPO_URL, 26, 600, "#626875", "end"))
    parts.append("</svg>")
    return "\n".join(parts)
