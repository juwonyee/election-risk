# election-risk

**An election risk desk for your coding agent.**

Name a company. Your agent works like a sell-side risk desk: it maps how the company makes its profit, finds
every Kalshi and Polymarket market for the Nov 3, 2026 US elections and US policy that can move it, and tells
you, with sources:

> If this resolves, profit changes by **$X a year (Y%)**. The market says **Z%**, and who wins moves that
> chance by **S**.

Then it opens a local web report and writes a share card. Works in Claude Code, Codex, Cursor, Gemini and any
agent that reads [Agent Skills](https://agentskills.io).

<p align="center"><img src="examples/F/card.svg" width="720" alt="Ford: if the US gives notice to leave USMCA before 2027, about −$2.0B a year (−29.5% of adjusted EBIT); Kalshi 8%"></p>

## What it found (Oct 27, 2026)

Eight household names, run end to end by the skills. Every row links to the full report, the profit
structure behind it and every source.

| Company | Headline | Market | Profit, per year |
|---|---|---|---|
| [Ford](examples/F/summary.md) | US gives notice to leave USMCA before 2027 | Kalshi 8% | **−$2.0B** (−29.5%) |
| [GM](examples/GM/summary.md) | Same USMCA notice | Kalshi 8% | **−$1.7B** (−13.3%) |
| [Coinbase](examples/COIN/summary.md) | Clarity Act (crypto market structure) becomes law before 2028 | Kalshi 21% | **+$370M** (+25.8%) |
| [DraftKings](examples/DKNG/summary.md) | Congress bans sports contracts on prediction markets in 2026 | Polymarket 18% | **+$150M** (+24.2%) |
| [Disney](examples/DIS/summary.md) | Federal film and TV production tax credit becomes law | Kalshi 26% | **+$400M** (+2.3%) |
| [Starbucks](examples/SBUX/summary.md) | New York City enacts a $30 minimum wage by 2030 | Kalshi 8% | **−$60M** (−2.0%) |
| [PG&E](examples/PCG/summary.md) | Becerra wins (96%) → 30% chance of a rate freeze, vs 0% under Hilton | Kalshi | **−$600M** (−12.6%) |
| [Uber](examples/UBER/summary.md) | California AG suit ends in a Lyft-sized settlement: 70%, and who wins moves it by at most 11 points | Kalshi | **−$170M** (−3.1%) |

**The surprise: who wins on Nov 3 moves these odds less than the headlines suggest.** Six of the eight biggest
risks are priced directly by policy markets (USMCA, the Clarity Act, a film credit) and barely depend on the
vote. Where the election does matter, the Red Team keeps it honest: research finds a new utility commission
moves allowed returns by about 0.15 points, and attorneys general of both parties sue companies, so the
PG&E and Uber results carry those flags in their reports.

> **Not investment advice.** Analyst drafts for human review. No recommendation to buy, sell or hold any
> security or to trade any contract. Markets are shown as information only.

## The desk

Four skills, each usable on its own; `election-risk` calls the other three by name.

| Role | Skill | Ask it |
|---|---|---|
| Exposure analyst | **profit-structure** | "Which of Ford's profit lines can a government move?" |
| Policy analyst | **candidate-positions** | "What would California's next governor do on electricity rates?" |
| Market analyst | **prediction-markets** | "What are the odds on a data-center moratorium?" |
| Risk Officer + Red Team | **election-risk** | "What does Nov 3 mean for Uber?" |

```
company ─► profit-structure      where profit comes from, what a government can move    structure.md
        ─► prediction-markets    every open Nov 3 and policy market, as two plain lists    _markets/
        ─► candidate-positions   what each winner would do, how, chance it happens         _book/
        ─► election-risk         links → engine → headlines, report, card, Red Team flags  <TICKER>/
```

## Install

**Ask your agent** (recommended):

```text
Install election-risk from https://github.com/juwonyee/election-risk
```

Or install it yourself, one of:

```bash
# Claude Code
claude plugin marketplace add juwonyee/election-risk
claude plugin install election-risk@election-risk

# Codex
codex plugin marketplace add juwonyee/election-risk
codex plugin add election-risk@election-risk

# Gemini
gemini extensions install https://github.com/juwonyee/election-risk

# Cursor
git clone --depth 1 https://github.com/juwonyee/election-risk ~/.cursor/plugins/local/election-risk

# Any other agent, via the skills CLI
npx skills add juwonyee/election-risk
```

Install the plugin or the skills, not both (you would see every skill twice). Needs Python 3.10+; no packages,
no API keys.

## First run: the policy book

Race results need to know what each candidate would actually do. That lives in a **policy book**: one file
per Nov 3 contest, every position with a source link, and the chance it happens if they win, from a
[research-based probability table](skills/candidate-positions/references/probability-table.md)
(veto override rates, governors' proposal success, ballot measure pass rates and more).

The book is not in this repo, on purpose: candidate positions in a public repo could be edited by anyone.
On the first run your agent asks you to pick:

- **Build it yourself**: your agent researches every contest with sources (it takes a while; agents with
  parallel subagents are faster) and reuses it for every company afterwards.
- **Download ours**: ready in a minute, built by us on the date shown, possibly out of date. Your agent tells
  you that and asks before running `erisk book download --accept-risk`.

Every report prints which book it used (built or downloaded, date, fingerprint) and when prices were fetched.

## How the numbers work

- **The agent researches, the engine calculates.** Every number in the table comes from a small Python engine
  (standard library only), not from the model's arithmetic.
- **Two kinds of market.** *Direct*: the market resolving Yes is the policy. *Race*: the market prices who
  wins, times the book's chance the policy follows each winner.
- **Two headlines.** The *election headline* is the biggest result where who wins moves the chance by 0.10 or
  more. The *policy headline* is the biggest result the market prices directly. "Meaningful" means at least
  1% of profit, volume at least 10,000 and a chance of at least 5%.
- **Every impact shows how it was built**: the formula with each number and its source, and a low-high range.
- **Red Team.** A position with no source link counts as 0. The report flags those, thin markets, wide ranges
  and estimated impacts.
- **Only priced risks.** Channels with no market are left out. Unreachable sources are listed, never worked
  around.

## What it won't do

Recommend trades, size positions, help open market accounts, or work around a venue's regional restrictions.
It names no small businesses (franchised chains are discussed as "a typical store").

## Run the engine yourself

```bash
python3 engine/erisk.py markets pull                         # every open Nov 3 + policy market
python3 engine/erisk.py book status                          # policy book coverage
python3 engine/erisk.py book find --tag utilities --state CA
python3 engine/erisk.py markets show GOVPARTYGA-26 --venue kalshi
ERISK_OUT=examples python3 engine/erisk.py compute --company SO --no-open   # test fixture, synthetic prices
```

## Develop

See [AGENTS.md](AGENTS.md). Edit `engine/`, then `python3 scripts/sync_engine.py`; check with
`python3 scripts/validate_skills.py` and `python3 -m unittest discover tests`.

## License

MIT.
