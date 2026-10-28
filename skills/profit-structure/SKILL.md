---
name: profit-structure
description: Writes an equity analyst's first page on a listed company - where its operating profit comes from, line by line with dollar sizes and filing sources, and which lines a government decision can move (tax, tariff, subsidy, rate approval, licence, wage law, procurement) and who decides each (Congress, President, agency, governor, legislature, commission, attorney general, voters). Use when the user asks what drives a company's profit, how exposed it is to policy or regulation, or before an election-risk analysis.
license: MIT
metadata:
  author: juwonyee
  version: "2.0.3"
---

# Profit structure

Start from how the company makes money, not from the news or the markets. Rough is fine; this is an
analyst's first page, not an audit. Do not invent numbers: a line you cannot size says "not disclosed".

`erisk` below means `python3 <skill-dir>/scripts/erisk.py` (`${CLAUDE_SKILL_DIR}` in Claude Code). Run it from
the user's working directory. Output: `./election-risk-out/<TICKER>/structure.md`.

## Workflow

```
- [ ] 1. Base: latest annual operating income (or adjusted EBIT / EBITDA when that is what the company
         steers by; say which), with the filing URL
- [ ] 2. Where operating profit comes from: segments, products, geographies, big cost lines
- [ ] 3. Policy lines inside them: taxes, credits, subsidies, tariffs, regulated rates, licences, wage laws,
         procurement, compliance costs
- [ ] 4. Which lines a government can move, the lever, who decides, and at what level
- [ ] 5. Write structure.md (format below)
```

**Sources.** The latest 10-K (or 20-F/40-F, or the annual report for non-US companies) and the latest earnings
release. For US filers, `erisk filings edgar <TICKER>` gives headline numbers; read the segment note and risk
factors for the rest. How to find and read the numbers: [references/filings.md](references/filings.md).

Split by whatever matters for this company: US states where they are material (staff, stores, rate base,
sales), customer type (government, Medicaid, Medicare), countries of import. Every line: $ per year, source
URL, `verified` (from a filing) or `estimated` (your arithmetic, shown).

Do not look at prediction markets or candidate positions while writing this. A structure written with the
markets open drifts toward whatever has a market.

## structure.md format

```markdown
# <Company> (<TICKER>): profit structure
Written <date>. Base: <FY> <measure> $<amount> (<status>, <url>)

## Where operating profit comes from
| # | Line | $ / yr | Source | Status |

## Policy lines inside those
| # | Line | $ / yr | Source | Status |

## What a government can move
| Line | Lever | Who decides | Level (federal / state: which states / local) | Issue tag |

## Locked in
Things already law that no election changes, with size.
```

**Issue tag** uses the policy book's words (`utilities`, `data-centers`, `energy-oil-gas`, `clean-cars-ev`,
`gaming-betting`, `health-medicaid-aca`, `insurance`, `labor-min-wage`, `gig-workers`,
`tech-antitrust-privacy`, `kids-online`, `crypto`, `film-tax-credits`, `corporate-sales-property-tax`,
`tariffs-trade`, `defense-procurement`, `housing`, `cannabis`, `transport-ai-vehicles`,
`wildfire-liability`, `other: <what>`), so `$candidate-positions` and `$election-risk` can look lines up.

## Answer format

The "What a government can move" table, biggest lines first, then one line: the base and the share of profit
the movable lines touch. Offer the full file path.
