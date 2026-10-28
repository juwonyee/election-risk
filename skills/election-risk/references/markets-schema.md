# markets.json

One file per company at `election-risk-out/<TICKER>/markets.json`.
Complete example (one direct, one race with a Polymarket cross-check):
[`examples/SO/markets.json`](https://github.com/juwonyee/election-risk/blob/main/examples/SO/markets.json) on GitHub. Check it with `erisk validate --company <TICKER>`.

## Contents
- Top level
- Direct entry
- Race entry
- Cross-check (second venue)
- Rules

## Top level

```jsonc
{
  "schema": "election-risk/markets@2",
  "company": {"name": "Southern Company", "short": "Southern Company", "ticker": "SO"},
  "denominator": {
    "label": "operating profit", "amount": 7285000000, "period": "FY2025", "status": "verified",
    "source": {"title": "Southern Company 10-K FY2025", "url": "https://www.sec.gov/..."}
    // non-USD companies add: "currency": "KRW", "amount_local": 2050000000000,
    //                        "fx": {"rate": 1376.0, "date": "2026-10-14", "source": "Federal Reserve H.10"}
  },
  "notes": {
    "locked_in": ["Base rates frozen through 2028", "..."],          // shown, not computed
    "weak_links": ["4 GW to $660M uses a ~10% pre-tax return (estimated)", "..."]
  },
  "entries": [ /* direct | race */ ]
}
```

`amount` is always US dollars per year. `status`: `verified` (filing, official page) or `estimated`.

## Direct entry: the market resolving Yes is the policy

```jsonc
{
  "id": "so-ga-4gw", "type": "direct",
  "hook": "Georgia's utility regulators decide how fast Georgia Power grows.",
  "event_plain": "Georgia approves 4 more gigawatts for Georgia Power",       // reads after "if"
  "market": {
    "source": "Kalshi", "event": "KXGA4GW-26AUG", "yes_ticker": "KXGA4GW-26AUG-28MAR01",
    "question": "Will Georgia regulators approve 4 more gigawatts before Mar 1, 2028?",
    "window": "before Mar 1, 2028",
    "rules_summary": "Yes if the Georgia PSC certifies at least 4,000 MW of new capacity for Georgia Power before Mar 1, 2028."
  },
  "impact": {
    "central": 660000000, "low": 450000000, "high": 800000000, "status": "estimated",
    "formula": "4 GW x $1.62B/GW = $6.5B rate base x ~10% pre-tax return = ~$660M a year",
    "timing": "run-rate around 2030",
    "sources": [{"title": "...", "url": "https://..."}]
  }
}
```

## Race entry: the market prices who wins

```jsonc
{
  "id": "so-ga-governor", "type": "race",
  "hook": "...", "event_plain": "Georgia pauses new data-center construction",
  "market": {
    "source": "Kalshi", "event": "GOVPARTYGA-26",
    "question": "Who will be inaugurated as Georgia's governor?",
    "rules_summary": "Resolves to the party of the person inaugurated as governor.",
    "outcomes": [
      {"ticker": "GOVPARTYGA-26-D", "name": "Keisha Lance Bottoms", "last": "Bottoms", "party": "D",
       "stance": "temporary statewide pause on new data centers", "route": "make: other party",
       "p_policy": 0.15, "source": "https://..."},
      {"ticker": "GOVPARTYGA-26-R", "name": "Rick Jackson", "last": "Jackson", "party": "R",
       "stance": "no stated position", "route": "none", "p_policy": 0.0}
    ],
    "p_policy_status": "estimated",
    "p_policy_rationale": "Policy book GA-governor.md: a pause needs the Republican legislature (table A, other party)."
  },
  "impact": { /* same shape as direct; the impact if the policy happens */ }
}
```

`p_policy` = chance (0-1) the policy follows if that candidate wins: **copy it from the policy book row**
(`erisk book find --tag ... --state ...`), with that row's `route` and `source`. A candidate with no row gets 0.
The engine computes the election swing (leader's p minus runner-up's) and the overall chance.

## Direct entry tied to a Nov 3 contest (optional)

When a direct market prices a policy that a Nov 3 contest also decides (e.g. a federal bill and House
control), keep the direct entry and add the contest, so the report can show how much the election moves it:

```jsonc
"election": {"contest": "US-house-control.md", "swing": 0.30,
             "note": "Republican House 0.35 (reconciliation) vs Democratic House ~0"}
```

## Cross-check (second venue)

Add to `market` when the other venue lists the same outcome. Its price is shown next to the main one and
never enters the math. If the main venue has no price, the engine falls back to the cross-check and says so.

```jsonc
"cross_check": {"source": "Polymarket", "event": "georgia-governor-winner-2026",
  "tickers": {"GOVPARTYGA-26-D": "will-the-democrats-win-the-georgia-governor-race-in-2026",
              "GOVPARTYGA-26-R": "will-the-republicans-win-the-georgia-governor-race-in-2026"}}
```

Polymarket tickers are market slugs (from `erisk markets show <slug> --venue polymarket`).

## Rules

- Impacts are signed yearly operating-profit effects once in force (+ helps, − hurts). A one-off amount (a
  settlement, a fine, a refund) sets `"one_off": true` in `impact` and is shown as "once", not "a year".
- `impact.formula` is the calculation path a reader can follow: every number in it, with its source in
  `impact.sources`. The report shows it under "How this number is built".
- Keep a market only if its rules match the policy; quote the gist in `rules_summary`.
- No entry without a market. Channels with no market are left out of the file.
