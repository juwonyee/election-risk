---
name: prediction-markets
description: Lists and prices every open Kalshi and Polymarket market for the Nov 3, 2026 US elections and for US policy events (bills, tariffs, regulators, ballot measures, court rulings), with midpoint prices, volume and rules text, from public APIs with no key. Use when the user asks for the odds of an election or policy outcome, wants to see which markets exist on a topic, or before an election-risk or candidate-positions task that needs the market list.
license: MIT
metadata:
  author: juwonyee
  version: "2.0.0"
---

# Prediction markets

Markets are information. Never say buy, sell or hedge, never size a position, and never help open an account
or get around a venue's regional restrictions.

`erisk` below means `python3 <skill-dir>/scripts/erisk.py` (`${CLAUDE_SKILL_DIR}` in Claude Code). Run it from
the user's working directory; output goes to `./election-risk-out/`. Python 3.10+, standard library only.

## The full list (read it, don't search it)

```bash
erisk markets pull            # about 4 minutes the first time each day; then cached
```

Writes two plain lists, one line per event (`venue:event | title | volume | close date | top outcomes`):
- `election-risk-out/_markets/elections.md`: contests decided by the Nov 3 vote (winners, chamber control,
  ballot measures). Margin, turnout and vote-share side markets are dropped. About 15k tokens: read it whole.
- `election-risk-out/_markets/house-districts.md`: single House districts (they act through House control).
- `election-risk-out/_markets/policy.md`: markets whose Yes is a policy (bill, tariff, regulator, moratorium,
  court ruling, government deal).

Each list is small enough to read whole. Read the relevant one in full instead of guessing search words: the
titles are terse and the same thing is often priced under a name you would not search for. The filter is
keyword-based, so a few off-topic lines get in; skip them.

## One market in detail

```bash
erisk markets show GOVPARTYGA-26 --venue kalshi                       # prices + rules text
erisk markets show georgia-governor-winner-2026 --venue polymarket
erisk markets search "data center" --prices                           # keyword search, both venues
```

**Read the rules before using a market.** It counts only if its resolution text matches the question: what
exactly resolves Yes, by when, and who decides. Similar titles often differ. Details, venue quirks and how
prices are computed: [references/markets.md](references/markets.md).

## Answer format

| Market (what resolves Yes) | Venue | Price | Volume | Closes |
|---|---|---|---|---|

Price = bid/ask midpoint, "thin" under 10,000 contracts (Kalshi) or $10,000 traded (Polymarket). Give both
venues when both list it. Say when the prices were pulled. If a venue could not be reached (Polymarket returns
HTTP 451 in some countries), say so and finish with the other.
