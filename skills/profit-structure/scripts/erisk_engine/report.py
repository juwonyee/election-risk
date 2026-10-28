"""A self-contained HTML report (no server, no CDN, no tracking) built from results/all.json."""
from __future__ import annotations

import html
import webbrowser

from . import card
from .util import fmt_money, fmt_volume

CSS = """
:root{--bg:#f7f6f2;--card:#fff;--ink:#16181d;--mute:#626875;--line:#e3e1da;--up:#1f7a4d;--down:#b3372e;
--bar:#d9d6cc;--k:#2b59c3;--p:#7a4cc2;--warn:#a86a00;--chip:#efede6}
@media (prefers-color-scheme:dark){:root{--bg:#121316;--card:#1b1d22;--ink:#eceae4;--mute:#9aa0ab;--line:#2b2e35;
--up:#4cc38a;--down:#ff7b6e;--bar:#30333b;--k:#6f97ff;--p:#b48cff;--warn:#e0a640;--chip:#24272e}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);
font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif}
.wrap{max-width:880px;margin:0 auto;padding:28px 16px 48px}
.kicker{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}
h1{font-size:30px;line-height:1.2;margin:6px 0 4px}.sub{color:var(--mute)}
.asof{display:inline-block;margin-top:10px;padding:4px 10px;border-radius:99px;background:var(--chip);font-size:13px}
.lead{margin:22px 0;padding:18px 20px;border-radius:14px;background:var(--card);border:1px solid var(--line);font-size:17px}
.lead b{font-size:22px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px;margin:16px 0}
.q{font-size:18px;font-weight:650;margin:0 0 2px}.rules{color:var(--mute);font-size:13px;margin-bottom:14px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}@media(max-width:640px){.grid{grid-template-columns:1fr}}
.big{font-size:34px;font-weight:750;line-height:1.1}.up{color:var(--up)}.down{color:var(--down)}
.label{font-size:12px;color:var(--mute);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px}
.bar{height:10px;border-radius:6px;background:var(--bar);overflow:hidden;margin:4px 0 2px}
.bar>i{display:block;height:100%}.k{background:var(--k)}.p{background:var(--p)}
.row{display:flex;justify-content:space-between;gap:8px;font-size:14px}
.chip{display:inline-block;font-size:12px;padding:2px 8px;border-radius:99px;background:var(--chip);margin:2px 4px 2px 0}
.thin{color:var(--warn)}.est{color:var(--warn)}.ver{color:var(--up)}
details{margin-top:12px;font-size:14px}summary{cursor:pointer;color:var(--mute)}
.formula{font-family:ui-monospace,Consolas,monospace;font-size:13px;background:var(--chip);padding:8px 10px;
border-radius:8px;margin:8px 0;white-space:pre-wrap}
.cands{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:6px}
.cand{border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.cand .pct{font-size:22px;font-weight:700}
.box{border-left:3px solid var(--warn);padding:10px 14px;background:var(--card);border-radius:8px;margin:16px 0}
ul{padding-left:20px}a{color:inherit}
footer{margin-top:28px;color:var(--mute);font-size:12px;border-top:1px solid var(--line);padding-top:14px}
.sigs{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}@media(max-width:640px){.sigs{grid-template-columns:1fr 1fr}}
.sig{background:var(--chip);border-radius:10px;padding:10px 12px}.sig b{display:block;font-size:15px;margin:2px 0}
.sig small{color:var(--mute);font-size:12px}
.lvl{display:inline-block;color:#fff;font-weight:700;font-size:15px;padding:3px 12px;border-radius:99px}
.high{background:#b3372e}.medium{background:#a86a00}.low{background:#1f7a4d}.no-market{background:#626875}
.shot svg{width:100%;height:auto;border-radius:10px;border:1px solid var(--line);display:block}
button{font:inherit;font-size:14px;padding:6px 14px;border-radius:8px;border:1px solid var(--line);
background:var(--chip);color:var(--ink);cursor:pointer;margin-top:10px}
"""

PNG_JS = """<script>
document.getElementById('png').onclick=function(){var s=new XMLSerializer().serializeToString(
document.querySelector('.shot svg'));var i=new Image();i.onload=function(){var c=document.createElement('canvas');
c.width=1600;c.height=900;c.getContext('2d').drawImage(i,0,0);c.toBlob(function(b){var a=document.createElement('a');
a.href=URL.createObjectURL(b);a.download=this_name;a.click();});};
i.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(s);};
</script>"""

e = html.escape


def _bar(q: dict | None) -> str:
    if not q or q.get("prob") is None:
        return ""
    cls = "k" if q["venue"] == "Kalshi" else "p"
    thin = ' <span class="thin">thin</span>' if q["low_liquidity"] else ""
    return (f'<div class="row"><span>{e(q["venue"])}</span><b>{q["prob"]:.0%}</b></div>'
            f'<div class="bar"><i class="{cls}" style="width:{q["prob"] * 100:.1f}%"></i></div>'
            f'<div class="row" style="color:var(--mute);font-size:12px"><span>'
            f'{fmt_volume(q["volume"], q["volume_unit"])}{thin}</span></div>')


def _status(s: str) -> str:
    return f'<span class="chip {"ver" if s == "verified" else "est"}">{e(s)}</span>'


def _sources(srcs: list[dict]) -> str:
    return "<ul>" + "".join(f'<li><a href="{e(s["url"])}">{e(s.get("title") or s["url"])}</a></li>'
                            for s in srcs) + "</ul>"


def _card(r: dict, den_label: str) -> str:
    imp, pct, m = r["impact"], r["impact_pct"], r["market"]
    cls = "up" if imp["central"] >= 0 else "down"
    head = (f'<div class="q">{e(m["question"])}</div>'
            f'<div class="rules">{e(m.get("rules_summary", ""))} · <code>{e(m["event"])}</code></div>')
    impact = (f'<div><div class="label">If {e(r["event_plain"])}</div>'
              f'<div class="big {cls}">{fmt_money(imp["central"])}<span style="font-size:16px"> {"once" if imp.get("one_off") else "a year"}</span></div>'
              f'<div class="sub">{pct["central"]:+.1%} of {e(den_label)} · range {fmt_money(imp["low"])} to '
              f'{fmt_money(imp["high"])} {_status(imp["status"])}</div></div>')
    if r["type"] == "direct":
        odds = (f'<div><div class="label">Market price {e(m.get("window", ""))}</div>'
                f'{_bar(r["price"])}{_bar(r.get("cross_check"))}</div>')
        body = f'<div class="grid">{impact}{odds}</div>'
    else:
        cands = "".join(
            f'<div class="cand"><div class="label">{e(o["name"])} ({e(o["party"])})</div>'
            f'<div class="pct">{o["price"]["prob"]:.0%}</div><div class="sub">to win</div>'
            f'{_bar(o["price"])}{_bar(o.get("cross_check"))}'
            f'<div style="margin-top:6px">If they win: <b>{o["p_policy"]:.0%}</b> chance it happens</div>'
            f'<div class="sub" style="font-size:13px">{e(o["stance"])}'
            f'{(" · " + e(o["route"])) if o.get("route") else ""}'
            f'{(" · <a href=" + chr(34) + e(o["source"]) + chr(34) + ">source</a>") if o.get("source") else ""}'
            f'</div></div>'
            for o in r["outcomes"])
        body = (f'{impact}<div class="label" style="margin-top:14px">Who wins '
                f'(chance the policy follows is {e(m.get("p_policy_status", "estimated"))})</div>'
                f'<div class="cands">{cands}</div><div class="sub" style="margin-top:8px">'
                f'{e(m.get("p_policy_rationale", ""))}</div>')
    notes = "".join(f'<div class="chip thin">{e(n)}</div>' for n in r.get("notes", []))
    tags = (f'<div style="margin-top:10px"><span class="chip">chance {r["chance"]:.0%}</span>'
            f'<span class="chip">election swing {r["election_swing"]:.2f}</span>'
            f'<span class="chip {"ver" if r["meaningful"] else ""}">{"meaningful" if r["meaningful"] else "below the bar"}'
            f'</span></div>')
    more = (f'<details><summary>How this number is built</summary><div class="formula">{e(imp["formula"])}</div>'
            f'<div>Timing: {e(imp.get("timing", ""))}</div>{_sources(imp.get("sources", []))}</details>')
    return f'<section class="card">{head}{body}{tags}{notes}{more}</section>'


def _board(data: dict) -> str:
    """The desk board on top: one signal per analyst, the two verdicts, the share card."""
    b = data.get("board")
    if not b:
        return ""
    sigs = "".join(f'<div class="sig"><small>{e(s["analyst"])}{"" if s["analyst"] == "Red Team" else " analyst"}'
                   f'</small><b>{e(s["signal"])}</b><small>{e(s["note"])}</small></div>' for s in b["signals"])
    verdicts = "".join(
        f'<div><div class="label">{k.capitalize()} risk</div>'
        f'<span class="lvl {b[k]["level"].replace(" ", "-")}">{e(b[k]["level"].upper())}</span>'
        f'<div style="margin-top:8px">{e(b[k]["text"])}</div></div>' for k in ("election", "policy"))
    svg = card.build(data)
    shot = (f'<section class="card"><div class="label">Share card</div><div class="shot">{svg}</div>'
            f'<button id="png">Save card as PNG</button></section>'
            + PNG_JS.replace("this_name", repr(f"{data['company']['ticker']}-election-risk.png")) if svg else "")
    return (f'<section class="card"><div class="label">Desk board</div><div class="sigs">{sigs}</div>'
            f'<div class="label" style="margin-top:18px">Risk Officer</div><div class="grid">{verdicts}</div>'
            f'<div class="sub" style="margin-top:12px;font-size:13px">High = share of profit × chance (policy) or '
            f'× election swing (election) of at least 2% of profit; Medium at least 0.5%.</div></section>{shot}')


def _desk(role: str, what: str) -> str:
    return f'<h2 style="margin:30px 0 4px;font-size:20px">{e(role)}</h2><div class="sub">{e(what)}</div>'


def build(data: dict) -> str:
    c, d, results = data["company"], data["denominator"], data["results"]
    ranked = sorted(results, key=lambda r: -abs(r["impact"]["central"]))
    lead = _board(data)
    asof = ", ".join(dict.fromkeys(a.replace("T", " ")[:16] + " UTC" for a in data.get("prices_as_of", []))) or "n/a"
    notes = data.get("notes") or {}
    locked = ""
    if notes.get("locked_in"):
        locked = '<section class="card"><div class="label">Locked in regardless of the election</div><ul>' +                  "".join(f"<li>{e(x)}</li>" for x in notes["locked_in"]) + "</ul></section>"
    red = list(notes.get("weak_links") or []) + list(data.get("red_team") or [])
    red_html = ('<section class="card"><ul>' + "".join(f"<li>{e(x)}</li>" for x in red) + "</ul></section>"
                if red else '<section class="card">No flags.</section>')
    gaps = ""
    if data.get("gaps"):
        gaps = '<div class="box"><b>Not included yet</b><ul>' + "".join(
            f"<li>{e(g['source'])} <code>{e(g['item'])}</code>: {e(g['reason'])}. {e(g['fix'])}</li>"
            for g in data["gaps"]) + "</ul></div>"
    bk = data.get("book") or {}
    book_line = (f'Policy book: {e(str(bk.get("source")))}, last edited {e(str(bk.get("last_edit")))}, '
                 f'{bk.get("files")} contests, fingerprint <code>{e(str(bk.get("fingerprint")))}</code>.'
                 if bk.get("files") else "No policy book was used: race chances are the analyst's own.")
    structure = ('Full profit structure: <code>structure.md</code> in this folder.' if data.get("structure")
                 else "")
    base = f'{e(d["period"])} {e(d["label"])} {fmt_money(d["amount"], signed=False)}'
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(c['short'])} election risk</title>
<style>{CSS}</style></head><body><div class="wrap">
<div class="kicker">{e(c['name'])} ({e(c['ticker'])}) · Election risk desk</div>
<h1>What Nov 3 could do to {e(c['short'])}'s profit</h1>
<div class="asof">Prices as of {e(asof)}</div>
{lead}{gaps}
{_desk("Exposure analyst", "Where the profit comes from and what a government can move.")}
<section class="card">Base: {base} <a href="{e(d['source']['url'])}">source</a> {_status(d['status'])}<br>{structure}</section>
{locked}
{_desk("Policy analyst", "What each winner would do, how, and the chance it happens if they win.")}
<section class="card">{book_line} Chances come from historical rates (an upper bound for two years), not forecasts.</section>
{_desk("Market analyst and Risk Officer", "Each market, its price, and the yearly profit change if it resolves.")}
{''.join(_card(r, d['label']) for r in ranked)}
{_desk("Red Team", "Weak spots a skeptical reviewer would raise.")}
{red_html}
<footer>Prices are bid/ask midpoints. Thin = under 10,000 contracts (Kalshi) or $10,000 traded (Polymarket).
Markets are shown as information only, not as a suggestion to trade.<br>{e(data['disclaimer'])}<br>
Generated {e(data['generated_at'])} by {e(data['repo'])}</footer></div></body></html>"""


def write(path, text: str, open_it: bool) -> None:
    path.write_text(text, encoding="utf-8")
    if open_it:
        try:
            webbrowser.open(path.resolve().as_uri())
        except Exception:
            pass  # no browser (CI, remote shell): the path is printed instead
