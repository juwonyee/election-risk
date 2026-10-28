"""erisk: find the prediction markets that move a company's profit, and size them.

Results go to ./election-risk-out/<COMPANY>/ (override with ERISK_OUT). Data on stdout (JSON or markdown),
progress on stderr. No prompts.

Commands:
  markets pull [--refresh]                            every open Nov 3 election market and direct policy market,
                                                      as two lists in election-risk-out/_markets/ (daily cache)
  markets search WORDS... [--any W...] [--venue both|kalshi|polymarket] [--prices] [--refresh]
                 [--about TEXT] [--no-rerank]           with OPENROUTER_API_KEY: ordered by Jev relevance
  markets show EVENT --venue kalshi|polymarket        prices + rules text for one event
  book status [--include-house]                       policy-book contests covered / still to research
  book find [--tag T] [--state ST] [--text WORD]      book rows by issue tag, state (+ federal), word
  book info                                           where the book came from, date, fingerprint
  book download [--accept-risk]                       the maintainers' book (only after the user agrees)
  filings edgar TICKER [--tags TAG...]                headline annual numbers (US and 20-F/40-F filers)
  validate --company C                                check markets.json before computing
  snapshot --company C [--refresh]                    fetch prices for the markets in markets.json
  compute --company C [--no-report] [--no-open]       results, summary.md, card.svg, report.html (opens)

Examples:
  erisk.py markets search ohio governor --prices
  erisk.py markets show GOVPARTYGA-26 --venue kalshi
  erisk.py validate --company SO && erisk.py snapshot --company SO && erisk.py compute --company SO

Exit codes: 0 ok, 1 validation errors or missing input, 2 a source was unreachable (see gaps).
"""
from __future__ import annotations

import argparse
import os
import sys
import urllib.error

from . import book, card, compute, filings, markets, report, universe
from . import validate as validate_mod
from .util import Blocked, load_json, stdout_utf8, workspace


def _ws(company: str):
    ws = workspace(company)
    if not (ws / "markets.json").exists():
        sys.exit(f"Error: {ws / 'markets.json'} not found. Write it first (see references/markets-schema.md), "
                 f"or pass the folder path with --company.")
    return ws


def cmd_markets(a) -> int:
    if a.action == "pull":
        res = universe.pull(a.refresh)
        print(markets.dumps(res))
        return 2 if res["gaps"] else 0
    if a.action == "search":
        if not a.words and not a.any:
            sys.exit("Error: give search words, e.g. `markets search ohio governor`")
        res = markets.search(a.words, a.any, a.venue, a.prices, a.refresh, about=a.about,
                             rerank_hits=not a.no_rerank)
        print(markets.dumps(res))
        return 2 if res["gaps"] and not res["results"] else 0
    if a.action == "show":
        if not a.words:
            sys.exit("Error: `markets show EVENT --venue kalshi|polymarket`")
        venue = {"kalshi": "Kalshi", "polymarket": "Polymarket"}[a.venue if a.venue != "both" else "kalshi"]
        try:
            print(markets.dumps(markets.show(venue, a.words[0])))
        except Blocked as x:
            print(markets.dumps({"gaps": [markets.gap(venue, a.words[0], str(x))]}))
            return 2
        except urllib.error.HTTPError as x:
            sys.exit(f"Error: {venue} returned HTTP {x.code} for {a.words[0]}. Check it with `markets search`.")
        return 0
    sys.exit("Error: markets pull|search|show")


def cmd_book(a) -> int:
    if a.action == "status":
        res = book.status(a.include_house)
    elif a.action == "find":
        res = book.find(a.tag, a.state, a.text)
    elif a.action == "info":
        res = book.info()
    else:
        res = book.download(a.accept_risk)
    print(markets.dumps(res))
    return 1 if res.get("error") or res.get("ok") is False else 0


def cmd_filings(a) -> int:
    try:
        out = filings.edgar(a.ticker, a.tags)
    except filings.NeedsUserAgent as x:
        print(markets.dumps({"gaps": [{"source": "SEC EDGAR", "item": a.ticker, "reason": str(x),
                                       "fix": "Ask the user whether to use their real email; set EDGAR_USER_AGENT and "
                                              "rerun, or read the numbers from the company's IR annual report."}]}))
        return 2
    except LookupError as x:
        sys.exit(f"Error: {x}")
    print(markets.dumps(out))
    return 0


def cmd_validate(a) -> int:
    ws = _ws(a.company)
    mk = markets.load_snapshots(ws) if (ws / "snapshots").exists() else None
    res = validate_mod.validate(load_json(ws / "markets.json"), mk)
    print(markets.dumps(res))
    return 0 if res["ok"] else 1


def cmd_snapshot(a) -> int:
    ws = _ws(a.company)
    res = markets.snapshot(ws, a.refresh)
    print(markets.dumps(res))
    return 2 if res["gaps"] else 0


def cmd_compute(a) -> int:
    ws = _ws(a.company)
    data = compute.run(ws)
    print((ws / "summary.md").read_text(encoding="utf-8"))
    svg = card.build(data)
    if svg:
        (ws / "card.svg").write_text(svg, encoding="utf-8")
        print(f"Card: {(ws / 'card.svg').resolve()}", file=sys.stderr)
    else:
        (ws / "card.svg").unlink(missing_ok=True)
        print("Card: none (no market reaches the company, so no card was written)", file=sys.stderr)
    if not a.no_report:
        path = ws / "report.html"
        report.write(path, report.build(data), open_it=not a.no_open and not os.environ.get("ERISK_NO_OPEN"))
        print(f"Report: {path.resolve()}", file=sys.stderr)
    return 2 if data["gaps"] else 0


def main(argv=None) -> int:
    stdout_utf8()
    ap = argparse.ArgumentParser(prog="erisk", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("markets")
    m.add_argument("action", choices=["pull", "search", "show"])
    m.add_argument("words", nargs="*")
    m.add_argument("--any", nargs="*", default=[])
    m.add_argument("--venue", choices=["both", "kalshi", "polymarket"], default="both")
    m.add_argument("--prices", action="store_true")
    m.add_argument("--refresh", action="store_true", help="rebuild today's list or search index")
    m.add_argument("--about", help="what the market should price, in plain words, for Jev relevance "
                                   "(default: the search words)")
    m.add_argument("--no-rerank", action="store_true", help="keep keyword order even with OPENROUTER_API_KEY")
    b = sub.add_parser("book")
    b.add_argument("action", choices=["status", "find", "info", "download"])
    b.add_argument("--tag")
    b.add_argument("--state")
    b.add_argument("--text", help="a word in the tag or position, e.g. nuclear")
    b.add_argument("--include-house", action="store_true")
    b.add_argument("--accept-risk", action="store_true", help="the user agreed to use a book built by others")
    f = sub.add_parser("filings")
    f.add_argument("source", choices=["edgar"])
    f.add_argument("ticker")
    f.add_argument("--tags", nargs="*", default=[])
    for name in ("validate", "snapshot", "compute"):
        p = sub.add_parser(name)
        p.add_argument("--company", required=True, help="ticker folder under election-risk-out, or a path")
        if name == "snapshot":
            p.add_argument("--refresh", action="store_true", help="refetch even if today's prices exist")
        if name == "compute":
            p.add_argument("--no-report", action="store_true", help="skip report.html")
            p.add_argument("--no-open", action="store_true", help="write report.html but don't open a browser")
    a = ap.parse_args(argv)
    return {"markets": cmd_markets, "book": cmd_book, "filings": cmd_filings, "validate": cmd_validate, "snapshot": cmd_snapshot,
            "compute": cmd_compute}[a.cmd](a)
