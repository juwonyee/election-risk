# Prediction markets: find, read, price

Read this at step 3. No API keys needed. Markets are information: never help open an account or get around a
venue's regional restrictions.

## Contents
- Find
- Read the rules before using a market
- Report prices
- Venue specifics
- When a venue can't be reached

## Find

```bash
erisk markets search ohio governor --prices                # all words must match; both venues
erisk markets search "minimum wage" --any nyc "new york"   # a phrase plus any of several words
erisk markets search "data center" --venue polymarket --prices
```

The first search of the day builds a local index of open events per venue (a few minutes); later searches are
instant. Search a few phrasings: titles are terse ("Who will be inaugurated as Ohio's governor?").

**Relevance order (optional).** If `OPENROUTER_API_KEY` is set, results come back ordered by how well each
market prices the topic (Jev, a yes/no model, via OpenRouter; each hit gets a `relevance` from 0 to 1 and the
output has a `rerank` block with the cost, usually well under a cent). Say what the market should price with
`--about`, e.g. `erisk markets search deport --about "number of US deportations"`, which sinks look-alikes
such as Deportivo football matches to the bottom. Put only the topic in `--about`, never a user's or
company's numbers. Relevance only sorts: still read the rules of every market you use. Without the key, or
with `--no-rerank`, results keep keyword order; if the call fails, `gaps` says so and the search still works.

## Read the rules before using a market

```bash
erisk markets show GOVPARTYGA-26 --venue kalshi
erisk markets show georgia-governor-winner-2026 --venue polymarket
```

A market counts only if its resolution text matches the channel. Check: what exactly resolves Yes, the
deadline, and who decides. Similar titles often differ (for example "any state enacts a moratorium" vs
"at least 3 states adopt binding moratoria"). If two venues differ by more than 10 points, read both rule
texts before using either.

## Report prices

- Price = bid/ask midpoint. Give the venue, the volume and the date. Kalshi volume is contracts (each pays $1);
  Polymarket volume is dollars.
- When both venues price it, show both ("Kalshi 68%, Polymarket 72%").

## Venue specifics

### Kalshi
- Public API, no key: `https://api.elections.kalshi.com/trade-api/v2/events/<EVENT>?with_nested_markets=true`.
- An **event** (e.g. `GOVPARTYOH-26`) holds **markets** (e.g. `GOVPARTYOH-26-D`). Use market tickers in
  `markets.json`.
- Governor races: `GOVPARTY{ST}-26`. Some 2026 races carry other year suffixes (`GOVPARTYNH-28`,
  `GOVPARTYKS-27` were 2026 races): check the rules, not the ticker.
- State ballot measures: `KXSTATEBALLOTMEASURE-{ST}` (one market per measure), California
  `KXCABALLOTMEASURES-26NOV03`. Local laws: `KXLOCALLAW-*`. Minimum wage: e.g. `KXNYCMINWAGE-27JAN01`.
- Ladder events ("above $X") list one market per strike; the engine makes them non-increasing.

### Polymarket
- Gamma API: `https://gamma-api.polymarket.com/events?slug=<slug>`. Use **market slugs** in `markets.json`.
- Races often list placeholder outcomes ("Option A", "Other") with no quote; they count as 0.
- Offset paging stops near 2,500 events, so the search index adds politics and economy tags; very small events
  can be missed.
- Joint markets ("Senate winner x oil below $85") give conditional odds; most only restate the larger market
  (e.g. ACA credits x House winner). Use them only when both legs carry real uncertainty.

### Liquidity in practice
Federal control and big governor races trade millions; many state measures, commission seats and tariff
ladders trade in the hundreds or low thousands. A thin market is still information, labelled as such.

## When a venue can't be reached

Polymarket returns HTTP 451 in some countries. Don't try to get around it: finish with Kalshi, then tell the
user Polymarket was unreachable from their network and that you can add its prices if they can reach it.
Do the same for timeouts or other errors on either venue.
