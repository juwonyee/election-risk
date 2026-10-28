"""Headline annual numbers for US filers from SEC EDGAR (free XBRL API).

SEC asks for a User-Agent with a contact email. The user chooses: their real email
(EDGAR_USER_AGENT="election-risk name@domain") or the placeholder. Unset -> FALLBACK_UA.
Covers 10-K (US GAAP, USD) and 20-F / 40-F filers (IFRS, any currency). For other listings the agent
reads the annual report from the country's filing system (see references/filings.md).
"""
from __future__ import annotations

import datetime as dt
import os
import urllib.error

from .util import http_json

ITEMS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet", "Revenue"],
    "operating_income": ["OperatingIncomeLoss", "ProfitLossFromOperatingActivities"],
    "pretax_income": ["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                      "ProfitLossBeforeTax"],
    "net_income": ["NetIncomeLoss", "ProfitLoss"],
    "cost_of_revenue": ["CostOfRevenue", "CostOfGoodsAndServicesSold", "CostOfSales"],
    "capex": ["PaymentsToAcquirePropertyPlantAndEquipment", "PurchaseOfPropertyPlantAndEquipment"],
}
ANNUAL_FORMS = ("10-K", "20-F", "40-F")


# Used when EDGAR_USER_AGENT is unset (the user chose the placeholder, or wasn't asked).
FALLBACK_UA = "election-risk you@example.com"


class NeedsUserAgent(Exception):
    pass


def user_agent() -> tuple[str, str]:
    """(User-Agent, which): 'env' when the user set EDGAR_USER_AGENT, else 'fallback'."""
    ua = os.environ.get("EDGAR_USER_AGENT", "").strip()
    return (ua, "env") if ua else (FALLBACK_UA, "fallback")


def _get(url: str):
    ua, which = user_agent()
    try:
        return http_json(url, headers={"User-Agent": ua}, timeout=60)
    except urllib.error.HTTPError as e:
        if e.code == 403:
            hint = ("SEC refused the placeholder contact. Ask the user whether to use their real email, then set "
                    'EDGAR_USER_AGENT="election-risk name@domain" and run again.' if which == "fallback" else
                    "SEC refused this User-Agent. Check EDGAR_USER_AGENT is 'name email' and try again later.")
            raise NeedsUserAgent(f"SEC returned 403. {hint}") from e
        raise


def lookup_cik(ticker: str) -> tuple[int, str]:
    for row in _get("https://www.sec.gov/files/company_tickers.json").values():
        if row["ticker"].upper() == ticker.upper():
            return int(row["cik_str"]), row["title"]
    raise LookupError(f"{ticker} is not in SEC's ticker list. It may not file with the SEC; use the company's "
                      "home filing system instead.")


def _latest(facts: dict, tag: str) -> dict | None:
    for taxonomy in ("us-gaap", "ifrs-full"):
        node = facts.get("facts", {}).get(taxonomy, {}).get(tag)
        if not node:
            continue
        rows = []
        for unit, vals in node.get("units", {}).items():
            for x in vals:
                if x.get("form") in ANNUAL_FORMS and x.get("start") and x.get("end"):
                    days = (dt.date.fromisoformat(x["end"]) - dt.date.fromisoformat(x["start"])).days
                    if 350 <= days <= 380:  # a full fiscal year, not a quarter or a stub
                        rows.append({**x, "unit": unit})
        if rows:
            rows.sort(key=lambda x: (x["end"], x.get("filed", "")))
            return rows[-1]
    return None


def edgar(ticker: str, extra_tags: list[str] | None = None) -> dict:
    cik, name = lookup_cik(ticker)
    facts = _get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json")
    items = dict(ITEMS)
    for t in extra_tags or []:
        items[t] = [t]
    out = {"ticker": ticker.upper(), "name": name, "cik": cik, "source": "SEC EDGAR XBRL companyfacts",
           "sec_contact": user_agent()[1], "items": {}}
    for key, tags in items.items():
        # Companies switch tags over time: take the latest year across candidates (earlier tag wins ties).
        found = [(r, t) for t in tags if (r := _latest(facts, t))]
        if not found:
            continue
        row, tag = max(found, key=lambda rt: (rt[0]["end"], -tags.index(rt[1])))
        accn = row["accn"]
        out["items"][key] = {
            "amount": row["val"], "currency": row["unit"], "tag": tag, "period": f"FY{row['end'][:4]}",
            "period_end": row["end"], "form": row["form"], "accession": accn, "status": "verified",
            "url": f"https://www.sec.gov/Archives/edgar/data/{cik}/{accn.replace('-', '')}/{accn}-index.htm",
        }
    return out
