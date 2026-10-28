# How the numbers are computed and shown

## Prices
- Probability = midpoint of the best yes bid and yes ask. The last trade can be days old in thin markets.
- Spread over 0.25: the midpoint is meaningless; the last trade is used if the market has traded
  (`quote: last_trade`), otherwise there is no price.
- Thin: under 10,000 contracts (Kalshi, each pays $1) or $10,000 traded (Polymarket). Shown everywhere.
- Ladders ("above $X") are made non-increasing in X with pool-adjacent-violators.
- Races (mutually exclusive outcomes) are normalized to sum to 1; placeholder outcomes with no quote and no
  volume count as 0.
- Prices fetched today are reused for the rest of the day (`snapshot --refresh` refetches).

## Per market
| Type | Probability shown | Impact shown |
|---|---|---|
| direct | market price that the policy happens | `impact`: yearly profit change once in force |
| race | each candidate's price to win, plus the *estimated* chance the policy follows under each | `impact` if the policy happens |

Share of profit = impact / denominator. No expected value is shown: the question is how big the swing is and
what the market says about its odds.

## Chance, election swing, headlines
- **Chance**: direct = market price; race = sum over candidates of (price to win × book `p`).
- **Election swing**: race = |book `p` of the market leader − the runner-up's|; direct = `election.swing` when a
  Nov 3 contest also decides the policy, else 0.
- **Meaningful**: |impact| ≥ 1% of the base, market volume ≥ 10,000, chance ≥ 5%.
- **Election headline**: the biggest meaningful result with a swing ≥ 0.10. **Policy headline**: the biggest
  meaningful result with a smaller swing. Either can be "none".
- Book chances are historical rates over a full term, used for about two years: read them as upper bounds.

## Red Team flags (automatic)
A race candidate with p > 0 and no source (the engine counts that chance as 0); a thin market; an impact range wider than 3×; a meaningful result
whose impact is an estimate; an attorney-general (`sue`) swing above the 0.03–0.11 the research supports; a
meaningful `appoint` result (research: about −0.15 pp of allowed return). The agent adds its own doubts in `notes.weak_links`.

## Provenance
Every report prints when prices were fetched and which policy book was used (built here or downloaded, last
edit date, fingerprint), so two people's results for the same company can be compared.

## Two venues
The main venue (`market.source`) enters the table. The other venue's price for the same outcome is printed
beside it. If the main venue has no price, the other venue's price is used and the row says so.
