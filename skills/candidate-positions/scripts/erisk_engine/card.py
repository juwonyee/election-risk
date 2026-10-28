"""One 16:9 share card (card.svg): company, its risk verdict, one number, what it takes, the odds.

Plain SVG, no fonts or images to fetch, so it opens anywhere and converts to PNG with any browser (the
report has a button for it). The number is the one behind the higher of the two desk-board verdicts, so
every run with a market gets a card, a Low one included.
"""
from __future__ import annotations

import html
import textwrap

from .compute import sides, why_below, _wins
from .util import REPO_URL, fmt_money

W, H = 1600, 900
FONT = "-apple-system,Segoe UI,Inter,Roboto,Helvetica,Arial,sans-serif"
INK, MUTE, BG = "#16181d", "#626875", "#f7f6f2"
LEVEL_COLOR = {"high": "#b3372e", "medium": "#a86a00", "low": "#1f7a4d", "no market": MUTE}


def _text(x, y, s, size, weight=400, fill=INK, anchor="start", tail="") -> str:
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}">{html.escape(s)}{tail}</text>')


def build(data: dict) -> str | None:
    b = data.get("board") or {}
    kind = b.get("card")
    if not kind:
        return None
    v = b[kind]
    r = next(x for x in data["results"] if x["id"] == v["id"])
    c, imp = data["company"], r["impact"]
    date = (data.get("prices_as_of") or [""])[-1][:10]
    if r["type"] == "race":
        hi, _ = sides(r)
        if_line = f"if {_wins(hi['last'])} and {r['event_plain'].rstrip('.')}"
        odds = (f"{hi['p_policy']:.0%} if {_wins(hi['last'])}  ·  {hi['last']} {hi['price']['prob']:.0%} to win "
                f"on {hi['price']['venue']}")
    else:
        if_line = f"if {r['event_plain'].rstrip('.')}"
        odds = f"{r['price']['venue']} {r['price']['prob']:.0%}"
    if v.get("below_bar"):
        why = why_below(r)
        odds = why[0].upper() + why[1:]
    label = f"{kind.upper()} RISK  {v['level'].upper()}"
    pill_w = len(label) * 19 + 72
    color = "#1f7a4d" if imp["central"] >= 0 else "#b3372e"
    per = "once" if imp.get("one_off") else "a year"
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
             f'<rect width="{W}" height="{H}" fill="{BG}"/>',
             _text(90, 150, c["short"], 72, 750, tail=f'<tspan fill="{MUTE}" font-size="40" font-weight="500">'
                                                      f'  {html.escape(c["ticker"])}</tspan>'),
             f'<rect x="{W - 90 - pill_w}" y="92" width="{pill_w}" height="72" rx="36" '
             f'fill="{LEVEL_COLOR[v["level"]]}"/>',
             _text(W - 90 - pill_w / 2, 140, label, 32, 700, "#ffffff", "middle"),
             _text(90, 470, fmt_money(imp["central"]), 230, 800, color,
                   tail=f'<tspan fill="{MUTE}" font-size="60" font-weight="500"> {per}</tspan>')]
    y = 570
    for line in textwrap.wrap(if_line, 54)[:2]:
        parts.append(_text(90, y, line, 50, 500, "#2a2d34"))
        y += 64
    parts.append(_text(90, y + 16, odds, 40, 500, MUTE))
    parts.append(_text(90, H - 60, f"AI risk desk for the Nov 3 midterms  ·  prices {date}  ·  not investment advice",
                       26, 400, MUTE))
    parts.append(_text(W - 90, H - 60, REPO_URL, 26, 600, MUTE, "end"))
    parts.append("</svg>")
    return "\n".join(parts)
