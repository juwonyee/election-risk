# The policy book: one file per contest

The book lives in `election-risk-out/_book/` in the user's working directory, one Markdown file per contest,
named `<ST>-<office>.md` (e.g. `CA-governor.md`, `US-house-control.md`, `NY-attorney-general.md`). The same
contest on Kalshi and Polymarket is one file that lists both market ids. `erisk book status` reads the
`Markets:` line to know what is covered, and `erisk book find` reads the tables, so keep both exact.

## Template

```markdown
# California Governor
Markets: kalshi:GOVPARTYCA-26, polymarket:california-governor-election-2026
Researched: 2026-10-27 · Becerra 0.96, Hilton 0.04 · volume 12,400,000
Office power: appoints the Public Utilities Commission (5 seats, staggered 6-year terms); signs or vetoes
bills; executive orders; directs state agencies (CARB, Insurance is elected separately).
Legislature: Democratic supermajority in both chambers (no Nov 3 market changes that). If Becerra wins:
trifecta, strong majority. If Hilton wins: divided, other-party legislature with veto-proof majority.

## Xavier Becerra (D)
| Tag | Position | Route | p | Source |
|---|---|---|---|---|
| utilities | Freeze PG&E and SCE base rates for two years | make: same party, strong | 0.35 | https://... (2026-09-14) |
| clean-cars-ev | No stated position | none | 0 | |

## Steve Hilton (R)
| Tag | Position | Route | p | Source |
|---|---|---|---|---|
| utilities | Replace PUC majority with "affordability" appointees | appoint | 0.30 | https://... (2026-08-02) |

Locked in: AB 1167 rate cap already law through 2027.
```

## Columns

- **Tag**: one of `utilities`, `data-centers`, `energy-oil-gas`, `clean-cars-ev`, `gaming-betting`,
  `health-medicaid-aca`, `insurance`, `labor-min-wage`, `gig-workers`, `tech-antitrust-privacy`,
  `kids-online`, `crypto`, `film-tax-credits`, `corporate-sales-property-tax`, `tariffs-trade`,
  `defense-procurement`, `housing`, `cannabis`, `transport-ai-vehicles`, `wildfire-liability`, or
  `other: <what>`. Exact words, so company analysts can search by tag.
- **Position**: one concrete line in plain words. Quote, don't paraphrase upward: "would review" is not
  "will cut".
- **Route**: how the winner would get it done, in the probability table's words:
  `make: alone`, `make: same party, strong`, `make: same party, narrow`, `make: other party`,
  `voters: initiative`, `voters: referral`, `federal: partisan`, `federal: bipartisan`,
  `federal: reconciliation`, `block: veto`, `block: majority`, `block: sign`, `appoint`, `sue`, `vague`,
  `none`, `court`. For `block:` rows, p is the chance the blocked policy still happens.
- **p**: from [probability-table.md](probability-table.md) for that route. Never tuned per case.
- **Source**: a public URL and date for every row with p > 0. **No URL, p = 0.** Prefer the campaign site,
  official statements, debate transcripts, Ballotpedia, and AP, Reuters, major regional papers or public
  media. Avoid partisan outlets.

## Rules

- Cover the two leading candidates (or the two parties for chamber control and for party markets).
- Only business-relevant positions: anything that could move a listed company's costs, revenue, taxes,
  regulation, licences or lawsuits. Skip social issues unless they have a direct business channel. 3–10 rows
  per candidate is typical; fewer is fine.
- Same method for every party. No editorializing, no inference from party labels.
- For House and Senate control, the "candidates" are the parties: list what each majority would actually
  push or stop (agenda, appropriations, oversight, confirmations, reconciliation) with routes from table B.
- Ballot measures: one file per state's measures; each measure is a row under `## Yes` with route
  `voters: initiative` or `voters: referral` and a link to the measure text. The market price already prices
  passage, so the row's job is to say what the measure does.
