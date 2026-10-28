# Research method: what the elections put in play for one company

Read this at step 3. Goal: for each government-movable line in `structure.md`, the chain from a Nov 3 contest
or a policy market to yearly operating profit, with a source on every link.

## One chain per channel

1. **Race or measure.** Governor, legislature, ballot measure, mayor, utility commission, Congress. Note who is
   on each side.
2. **Policy.** What each side or the measure would actually do: platform pages, bill text, measure text.
3. **Can it happen?** For a race, copy each candidate's `p` from the policy book row (`erisk book find`);
   no row, 0. For a direct market, the price is the chance.
4. **Size of the policy.** From official or independent analyses (`policy.md`). Give a range when sources
   disagree.
5. **Company exposure.** From filings and the company's own pages (`filings.md`): staff by state, stores,
   sales mix, segment profit, rate base.
6. **Dollars.** A formula with numbers, e.g.
   `associates 33,718 x 0.92 hourly x 0.55 below $20 x $2.00 x 1,700 h = $58M a year`.
   Use operating profit, not revenue, unless you say otherwise.

Then attach the market that prices it, from `elections.md` or `policy.md`. No market, no row.

## Where channels usually are

| Company type | Look first at |
|---|---|
| Retail, restaurants, logistics | State and city minimum wages, scheduling laws, SNAP and benefit timing, sales and grocery taxes |
| Utilities | State utility commission seats and orders (rate cases, capacity approvals), data-center rules, governor races |
| Gaming, cannabis | Legalization measures and bills, governor races, tax rates |
| Health insurers, pharmacy, PBMs | Medicaid and Medicare Advantage rules, PBM bills, state drug-pricing laws |
| Homebuilders, real estate | Property-tax measures, rent rules, zoning, immigration enforcement (labor) |
| Energy, data centers, chips | Moratoria, siting and clean-energy rules, tax credits, grid-market exits |
| Non-US companies | US tariffs on their country or sector, US tax credits for their US plants, US sales by state |

`policy.md` holds the current political context (what is locked in, veto math).

## Locked in vs in play

**Locked in** = already law, or not reversible by the coming election (for example a reconciliation law the
President would veto any repeal of). Report it separately with its size. It is not a market row.

## Checklist before writing markets.json

- Each impact has a formula, a range, `verified`/`estimated`, and URLs.
- Each market's rules match the channel (read them with `markets show`).
- Both parties' outcomes are treated with the same method.
- The 2-3 estimates that drive the result are listed in `notes.weak_links`.
