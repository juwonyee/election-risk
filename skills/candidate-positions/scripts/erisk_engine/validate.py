"""Check a company's markets.json before computing. Errors say what is wrong and what to put instead."""
from __future__ import annotations

from .markets import VENUES

STATUSES = ("verified", "estimated")


def _impact(where: str, imp, errs: list, warns: list) -> None:
    if not isinstance(imp, dict):
        errs.append(f"{where}: missing 'impact' object with central/low/high/status/formula/sources")
        return
    for k in ("central", "low", "high"):
        if not isinstance(imp.get(k), (int, float)):
            errs.append(f"{where}.impact.{k}: must be a number in US dollars per year (e.g. -130000000)")
    if all(isinstance(imp.get(k), (int, float)) for k in ("central", "low", "high")):
        lo, hi = sorted([imp["low"], imp["high"]])
        if not lo <= imp["central"] <= hi:
            errs.append(f"{where}.impact: central {imp['central']} is outside low..high ({imp['low']}..{imp['high']})")
        if imp["central"] != 0 and any(imp[k] != 0 and (imp[k] > 0) != (imp["central"] > 0) for k in ("low", "high")):
            warns.append(f"{where}.impact: low/high have a different sign from central; check the direction")
    if imp.get("status") not in STATUSES:
        errs.append(f"{where}.impact.status: must be 'verified' or 'estimated'")
    if not imp.get("formula"):
        errs.append(f"{where}.impact.formula: write the arithmetic with numbers, e.g. '4 GW x $1.62B/GW x 10% = $660M'")
    srcs = imp.get("sources") or []
    if not srcs or any(not s.get("url") for s in srcs):
        errs.append(f"{where}.impact.sources: give at least one {{title, url}}; every source needs a url")


def validate(mf: dict, snapshots: dict | None = None) -> dict:
    errs: list[str] = []
    warns: list[str] = []
    c = mf.get("company") or {}
    for k in ("name", "short", "ticker"):
        if not c.get(k):
            errs.append(f"company.{k}: required")
    d = mf.get("denominator") or {}
    if not isinstance(d.get("amount"), (int, float)) or d.get("amount", 0) <= 0:
        errs.append("denominator.amount: positive yearly profit in US dollars (convert other currencies; see fx)")
    for k in ("label", "period"):
        if not d.get(k):
            errs.append(f"denominator.{k}: required (e.g. label 'operating profit', period 'FY2025')")
    if d.get("status") not in STATUSES:
        errs.append("denominator.status: 'verified' (from a filing) or 'estimated'")
    if not (d.get("source") or {}).get("url"):
        errs.append("denominator.source.url: link the filing or page the number comes from")
    if d.get("currency") and d.get("currency") != "USD" and not (d.get("fx") or {}).get("rate"):
        errs.append("denominator.fx: a non-USD company needs {rate, date, source} for the conversion")

    entries = mf.get("entries") or []
    if not entries:
        errs.append("entries: empty. Add at least one direct or race entry (channels with no market are left out)")
    ids = set()
    for i, e in enumerate(entries):
        where = f"entries[{i}]({e.get('id', '?')})"
        if not e.get("id"):
            errs.append(f"{where}.id: required and unique")
        elif e["id"] in ids:
            errs.append(f"{where}.id: duplicate id")
        ids.add(e.get("id"))
        if e.get("type") not in ("direct", "race"):
            errs.append(f"{where}.type: 'direct' (market Yes = the policy) or 'race' (market = who wins). "
                        "Risks with no market are left out.")
            continue
        for k in ("hook", "event_plain"):
            if not e.get(k):
                errs.append(f"{where}.{k}: required plain-English text")
        m = e.get("market") or {}
        if m.get("source") not in VENUES:
            errs.append(f"{where}.market.source: one of {VENUES}")
        for k in ("event", "question", "rules_summary"):
            if not m.get(k):
                errs.append(f"{where}.market.{k}: required (rules_summary = one line on how the market resolves)")
        tickers = []
        if e["type"] == "direct":
            if not m.get("yes_ticker"):
                errs.append(f"{where}.market.yes_ticker: the market whose Yes is the policy")
            tickers = [m.get("yes_ticker")]
            el = e.get("election")
            if el is not None and (not isinstance(el.get("swing"), (int, float)) or not el.get("contest")):
                errs.append(f"{where}.election: {{contest, swing}} where swing (0-1) is the difference in the "
                            "policy book p between the contest's two leaders; omit if no Nov 3 contest decides it")
            if not m.get("window"):
                warns.append(f"{where}.market.window: say by when, e.g. 'before Mar 1, 2028'")
        else:
            outs = m.get("outcomes") or []
            if len(outs) < 2:
                errs.append(f"{where}.market.outcomes: a race needs every candidate or party with a ticker")
            for j, o in enumerate(outs):
                for k in ("ticker", "name", "last", "party", "stance"):
                    if not o.get(k):
                        errs.append(f"{where}.market.outcomes[{j}].{k}: required")
                if not isinstance(o.get("p_policy"), (int, float)) or not 0 <= o["p_policy"] <= 1:
                    errs.append(f"{where}.market.outcomes[{j}].p_policy: chance (0-1) the policy follows if they win")
                elif o["p_policy"] > 0 and not o.get("source"):
                    warns.append(f"{where}.market.outcomes[{j}].source: a p_policy above 0 needs the URL of the "
                                 "position (from the policy book row); without one the engine counts the chance as 0")
                if o.get("p_policy") and not o.get("route"):
                    warns.append(f"{where}.market.outcomes[{j}].route: give the probability-table route, "
                                 "e.g. 'make: other party'")
            if m.get("p_policy_status") not in STATUSES:
                errs.append(f"{where}.market.p_policy_status: usually 'estimated'")
            if not m.get("p_policy_rationale"):
                errs.append(f"{where}.market.p_policy_rationale: one sentence (legislature, veto, courts, timing)")
            tickers = [o.get("ticker") for o in outs]
        cc = m.get("cross_check")
        if cc:
            if cc.get("source") not in VENUES or cc.get("source") == m.get("source"):
                errs.append(f"{where}.market.cross_check.source: the other venue")
            missing = [t for t in tickers if t not in (cc.get("tickers") or {})]
            if missing:
                warns.append(f"{where}.market.cross_check.tickers: no mapping for {missing}")
        _impact(where, e.get("impact"), errs, warns)
        if snapshots is not None:
            for t in tickers:
                if t and (m.get("source"), t) not in snapshots:
                    warns.append(f"{where}: {m.get('source')} market {t} has no price yet. Run `snapshot` "
                                 "(if it still fails, check the ticker with `markets show`)")
    return {"ok": not errs, "errors": errs, "warnings": warns}
