# Research brief: what the 2026 US elections put in play for one company

Written 2026-10-14 (Election Day is 2026-11-03); re-check the "context" section if you use it later.
You research ONE company and write `research/<TICKER>.md`. The worked files in this folder (9 companies)
follow this structure exactly, so results can be compared. For the skill, also note for each channel which
market prices it (see SKILL.md, Step 3).

## The question

How much of this company's annual operating income could change depending on who wins the 2026 elections
(federal, governor, state legislature, ballot measures, mayors, utility commissions)? Separate that from
policy that is already locked in no matter who wins.

## Method: one chain per channel, every link sourced

For each channel (a way an election outcome reaches this company's P&L):

1. **Election and odds**: which race(s) or ballot measure(s). Probability from Kalshi (preferred) or another
   public source (Polymarket if reachable, else ratings/polls; say which). Record ticker, bid/ask midpoint,
   volume, date. Flag volume < 10,000 contracts as thin.
2. **Policy**: what each side/candidate/measure would actually do (platform, bill, measure text). Source URLs.
3. **Enactment**: P(becomes law | that outcome). Use a market if one exists; otherwise estimate it and give a
   one-sentence rationale (legislature control, veto, courts, timing). Mark as *estimated*.
4. **Size of the policy**: from official or independent analyses (CBO, JCT, CRS, state fiscal notes, LAO,
   state economists, Yale Budget Lab, Tax Foundation, Penn Wharton, KFF, academic work). Give a range when
   sources disagree.
5. **Company exposure**: from SEC filings (10-K/10-Q segment, state or product mix), company IR pages,
   public earnings-call transcripts on the company's own IR site, reputable news. Mark *verified* or *estimated*.
6. **Dollars**: write the formula with numbers, e.g. `associates 33,718 x 0.92 hourly x 0.55 below $20 x
   $2.00 x 1,700 h = $58M/yr`. Give **if it happens** (annual operating-income impact) and **expected**
   (x election prob x enactment prob). Use operating income, not revenue, unless stated.

Also list **locked in regardless** (policy already law or not reversible after the midterms) with sizes.

## Context you can rely on (already verified; don't re-research unless your company needs detail)

- Chamber odds (Kalshi, Oct 2026): House D ~90%, Senate D ~62%. Balance of power: D sweep ~61%, D House + R Senate ~30%, R sweep ~11%. The President (R) serves to Jan 2029, so federal law changes need his signature or a 2/3 override.
- The 2025 reconciliation law (P.L. 119-21 / OBBBA) locked in SNAP cuts, tax changes, Medicaid changes and multi-year enforcement funding.
- Tariffs: IEEPA tariffs struck down 2026-02-20 (Learning Resources v. Trump). Section 122 10% surcharge expired 2026-07-24. Section 301 "forced labor" tariffs of 10% or 12.5% on 60 economies since 2026-07-24 (USMCA goods exempt). Brazil 25% Section 301 since 2026-07-22. Section 232 sector tariffs in force (steel/aluminum/copper 10-50%, autos 15-25%, lumber/furniture, semiconductors 25%, pharma). Congress has no disapproval route for 301/232; overriding requires a veto-proof law. Peak GOP crossover so far: 5 senators, 6 House members.
- SNAP is funded only through 2026-12-11 (CR P.L. 119-103); Kalshi prices a federal shutdown on Dec 12 at ~33%.
- Kalshi governor markets use `GOVPARTY{ST}-26` (e.g. GOVPARTYGA-26, GOVPARTYWI-26). Ballot-measure markets include KXCABALLOTMEASURES-26NOV03, KXFLPROPERTYTAX-26NOV03, KXWEALTHTAXEFFECT-27. Others seen: KXMJSCHEDULE, KXNYCMINWAGE-27JAN01, KXDEPORTATIONS-27JAN01, KXACAEXT-26JAN, KXTARIFFRATE{PRC,MEX,CAN,EU,BR,INDIA}-27JAN01, KXTARIFFSECTOR-27JAN01.

## Tools

- Kalshi public API (no key): `curl -s "https://api.elections.kalshi.com/trade-api/v2/events/<EVENT>?with_nested_markets=true"`.
  Prices are in `yes_bid_dollars` / `yes_ask_dollars`; volume in `volume_fp`. To find series: `.../events?status=open&series_ticker=<SERIES>&with_nested_markets=true`.
  A cached list of ~6,000 open Kalshi events (title, ticker) is at `%TEMP%/kalshi_events.json` (rows: [category, event_ticker, series_ticker, title, sub_title]); grep it before paging the API.
- SEC EDGAR: `python scripts/edgar.py <TICKER> --tags <us-gaap tags>` from the repo root (set `EDGAR_USER_AGENT="election-risk you@example.com"`).
- Polymarket may return HTTP 451 from this network. If so, skip it. Do not try to get around the block.

## Rules

- Public sources only. No paywalled transcripts. Cite a URL for every number.
- Do not invent numbers. If something can't be found, say "not found" and, if you estimate, label it *estimated* with the reasoning.
- Treat both parties with the same method. No editorializing.
- No investment language (no buy/sell/hold, no price targets).
- Keep it efficient: roughly 30-50 tool calls.

## Output file format: `research/<TICKER>.md`

```
# <Company> (<TICKER>): 2026 election exposure
Base: FY revenue, operating income (EDGAR link), key concentration facts (states, segments, products).

## Bottom line
- In play (expected): $X/yr (Y% of operating income); if everything happens: $Z
- Locked in regardless: <one line with sizes>
- Card fact (one plain-English sentence a non-expert gets in 2 seconds):
- Strongest R-vs-D contrast, if any:

## Channels in play
| # | Channel | Race/measure (odds, ticker, volume) | Policy | P(enact|outcome) | If it happens | Expected | Confidence |
then one subsection per channel with the formula and sources.

## Locked in regardless
## Biggest uncertainties
## Sources
```

Your final reply (to the coordinator) should be a <=200-word summary: the bottom-line numbers, the card fact,
and the 1-2 weakest links in the chain.
