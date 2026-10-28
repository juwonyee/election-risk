---
name: election-risk
description: Works like a sell-side risk desk on one listed company - starts from how it makes its profit, links each government-movable line to the Nov 3, 2026 US election contests and policy markets on Kalshi and Polymarket that decide it, and states how much yearly profit changes if each resolves, next to the market's odds and how much the election moves them, with sources, a local web report and a share card. Use when the user asks what an election, a candidate, a ballot measure or a policy fight could mean for a company or ticker, US-listed or not, even if they don't mention prediction markets. Not investment advice.
license: MIT
metadata:
  author: juwonyee
  version: "2.0.2"
---

# Election risk for a company

The answer, per link: **"If this resolves, profit changes by $X a year (Y%). The market says Z%; who wins
moves that chance by S."** A risk with a price can be measured. Channels with no market are left out.

`erisk` below means `python3 <skill-dir>/scripts/erisk.py` (`${CLAUDE_SKILL_DIR}` in Claude Code). Run it from
the user's working directory; everything goes to `./election-risk-out/`. Python 3.10+, standard library only.

**You** research, choose and source every number and write `markets.json`. **The engine** fetches prices and
does all the math. Never compute or edit a number the engine printed; fix `markets.json` and re-run.

## The desk

| Role | Skill | Output |
|---|---|---|
| Exposure analyst | `$profit-structure` | `election-risk-out/<TICKER>/structure.md` |
| Policy analyst | `$candidate-positions` | `election-risk-out/_book/` (the policy book) |
| Market analyst | `$prediction-markets` | `election-risk-out/_markets/elections.md`, `policy.md` |
| Risk Officer | this skill | `markets.json` → `summary.md`, `report.html`, `card.svg` |
| Red Team | this skill, last step | flags in the summary and report |

If another skill is not installed, follow the same steps with the `erisk` commands below.

## Rules that hold for every answer

- Never say buy, sell, hold, short or "hedge with this contract", and never size a position or count
  contracts. You may say a risk "has a market price" and so "can be measured"; stop there.
- Same method for every party and candidate. No editorializing.
- Every amount and policy claim has a public URL and is `verified` (filing, official page, market price) or
  `estimated` (your arithmetic, shown). Race chances come from the policy book, never from your own guess.
- Show volume; never lead with a thin market when a liquid one prices the same thing.
- End with: *Analyst draft for human review. Scenario estimates, not investment advice or a recommendation to
  trade any security or contract.*
- **When a source can't be reached** (HTTP 451, a missing key, a timeout), keep going; never get around a
  block. List what is missing at the end.

## Workflow

```
- [ ] 0. Policy book ready?   erisk book info
- [ ] 1. Exposure: structure.md                  ($profit-structure)
- [ ] 2. Markets: erisk markets pull              ($prediction-markets)
- [ ] 3. Links: lines -> book rows + market lists -> markets.json
- [ ] 4. erisk validate -> fix -> repeat until ok
- [ ] 5. erisk snapshot, erisk compute            (summary.md, card.svg, report.html)
- [ ] 6. Red Team, then answer in the format below
```

**0. Policy book.** If `erisk book info` shows no book, ask the user once, before anything else:
- **Build it here** with `$candidate-positions`: the user's own research, sourced; it takes a while (about
  200 contests; parallel subagents help) and is reused for every company afterwards. For one company you can
  build only the contests in that company's states and issues first.
- **Download the maintainers' book** (`erisk book download --accept-risk`): ready in a minute, but built by
  someone else and possibly out of date. Run it only after telling the user that and getting a yes.

**1. Exposure.** Write `structure.md` per `$profit-structure` **before** opening any market list or the book:
base, where profit comes from, and what a government can move, with an issue tag per line.

**2. Markets.** `erisk markets pull` writes the full lists. Read `elections.md` (contests) and `policy.md`
(direct policy markets) in full; do not search for markets.

**3. Links (at most 8, biggest first).** For each movable line:
- Find the book rows: `erisk book find --tag <tag> --state <ST>` (federal rows come with every state); add
  `--text <word>` (e.g. `nuclear`) when the line's issue has no exact tag.
- **Race link**: a contest in `elections.md` whose winner decides the line. `p_policy` per candidate =
  the book row's `p` for that policy, with its `route` and `source`; no row, 0. A `block: veto` row's `p` is
  already the chance the blocked policy still happens: use it as is. Never change a book `p`; if you think the
  book is wrong, say so in `notes.weak_links`. One race can carry several policies: one entry per policy.
- **Ballot measures are direct links**: the market prices passage, so its price is the chance; the book row
  only says what the measure does. Never multiply a measure's price by the book's `p`.
- **Direct link**: a market in `policy.md` whose Yes is the policy; its price is the chance, even when the
  book's `p` differs. If a Nov 3 contest also decides it, add `election: {contest, swing}` (the book file and
  the difference between the two sides' `p`). For date ladders, use the rung that matches the impact's timing
  and say which in `rules_summary`.
- Read each market's rules (`erisk markets show EVENT --venue ...`) and keep it only if they match.
- Size the impact on yearly operating profit with a formula in plain numbers, a low-high range and sources:
  [references/research-method.md](references/research-method.md), [references/policy.md](references/policy.md).
- Write `election-risk-out/<TICKER>/markets.json` per
  [references/markets-schema.md](references/markets-schema.md).

**4–5.** `erisk validate --company <TICKER>` until `"ok": true`; then `erisk snapshot --company <TICKER>` and
`erisk compute --company <TICKER>` (add `--no-open` if asked).

**6. Red Team.** Read the engine's flags in `summary.md` and add your own to `notes.weak_links`: the 2-3
estimates that drive the result, any book row you doubt, any market whose rules only partly match. Re-run
compute if you changed anything.

## Answer format

1. **Desk board**: the analyst table, the Risk Officer line and both verdicts with their reasons, exactly as
   `summary.md` prints them.
2. The table from `summary.md`.
3. **Locked in regardless**, then **Red Team** (weakest links and flags), with an offer to change them.
4. The report path and the card path exactly as `compute` printed them (the report has a "Save card as PNG"
   button; if it printed "Card: none", say no market reaches the company), the policy book line (source, date,
   fingerprint), sources, then the disclaimer.
5. **Not included**, if any source was unreachable.

If no market reaches the company, say so plainly and list the lines you checked.

## More

- Worked example (Ford: one direct and two race links; election risk Low, policy risk High): [references/example-ford.md](references/example-ford.md)
- How the numbers are computed and shown: [references/methodology.md](references/methodology.md)
