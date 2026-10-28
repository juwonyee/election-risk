# DraftKings (DKNG): profit structure
Written 2026-10-27 (rewritten from the 2026-10-22 analyst draft; research not redone). Base: FY2025 Adjusted EBITDA $620.0M (verified, https://www.sec.gov/Archives/edgar/data/1883685/000188368526000013/dkng-20251231.htm). GAAP operating income was -$15.8M (near zero), so the company's own steering measure, Adjusted EBITDA, is the base.

FY2026 guidance (Q2 2026 release, Aug 7, 2026): revenue $6.5-6.9B, Adjusted EBITDA $700-900M; management says the core business is ~$1B, the gap being spend on Predictions (https://www.sec.gov/Archives/edgar/data/1883685/000188368526000027/q226-prx8kexx991.htm). Guidance assumes state tax rates stay where they are.

## Where operating profit comes from
| # | Line | $ / yr | Source | Status |
|---|---|---|---|---|
| R1 | Sportsbook revenue (online + retail; 27 US jurisdictions + Ontario); handle $53.6B, net revenue margin 7.1% | +$3,827M | 10-K revenue note (URL above) | verified |
| R2 | iGaming revenue (MI, NJ, PA, WV, CT, Ontario) | +$1,805M | 10-K revenue note | verified |
| R3 | Other: DFS, Jackpocket lottery courier, Predictions, $25.6M interest on deposits | +$423M | 10-K revenue note | verified |
| C1 | Cost of revenue (gaming taxes, payment processing, market access, platform) | -$3,557M | 10-K income statement | verified |
| C2 | Sales and marketing | -$1,380M | 10-K | verified |
| C3 | Product and technology | -$460M | 10-K | verified |
| C4 | General and administrative | -$674M | 10-K | verified |
| | GAAP operating income | -$15.8M | 10-K | verified |
| A1 | Add-backs: D&A $275M, stock comp $339M, other ~$21M | +$636M | 10-K Adj. EBITDA reconciliation | verified |
| | **Adjusted EBITDA (base)** | **$620.0M** | 10-K | verified |

Revenue by state is not disclosed. Estimated split (state 2025 market revenue x DraftKings' national share: OSB $3.83B / $16.89B ≈ 23%, iGaming $1.80B / $10.73B ≈ 17%; AGA via https://www.covers.com/industry/aga-sports-betting-igaming-revenue-surged-over-20-percent-in-2025-may-12-2026, LSR via https://www.legalsportsreport.com/239399/sports-betting-pace-for-2025/), all estimated:

| State | DK revenue est. | Current tax (approx.) | 1 pp tax change ≈ EBITDA / yr |
|---|---|---|---|
| New York OSB | ~$625M | 51% | ~$6M |
| Pennsylvania iGaming + OSB | ~$795M | 54% iGaming / 36% OSB | ~$8M |
| Michigan iGaming + OSB | ~$670M | 20-28% iGaming / 8.4% OSB | ~$7M |
| New Jersey iGaming + OSB | ~$810M | 19.75% (raised 2025) | ~$8M |
| Illinois OSB | ~$355M | graduated to 40% + per-wager fee since Jul 2025 | ~$4M (+ per-wager) |
| Ohio OSB | ~$250M | 20% | ~$2.5M |
| Other OSB states (MA, MD, AZ, NC, VA, CO, TN, KS, IA, KY, LA, CT, NH, MO, ...) | ~$1.9B | 10-51% | ~$19M in total |

Rule of thumb: +1 pp on DraftKings' whole ~$5.6B gaming revenue ≈ -$56M/yr Adjusted EBITDA (≈ 9% of base), estimated.

## Policy lines inside those
| # | Line | $ / yr | Source | Status |
|---|---|---|---|---|
| P1 | State gaming taxes (inside C1) | ≈ -$1,600M (range -$1,400M to -$1,900M) | not disclosed; 10-K says gaming taxes rose $473.4M in 2025; ~25-30% x ~$5.6B gaming revenue | estimated |
| P2 | Federal wagering excise tax, 0.25% of OSB handle (inside C1) | ≈ -$134M | rate from 10-K risk factors; 0.25% x $53.6B | estimated |
| P3 | Predictions (CFTC-regulated event contracts) investment in 2026 | ≈ -$100M to -$300M | core ~$1B vs guidance $700-900M (Q2 2026 release) | estimated |
| P4 | Advertising / promotion rules (inside C2 and net revenue margin) | not disclosed | 10-K | not sized |
| P5 | DFS and lottery courier (inside R3) | not disclosed; each likely < $100M EBITDA | 10-K | estimated |
| P6 | New-state upside (iGaming in NY, IL, OH, MD, MA, IN; OSB in CA, TX, GA, FL, MN, SC, AL) | one large state at maturity ~$75-200M EBITDA; NY iGaming ~$100-150M | ~$3B NY market at PA-like per-adult spend x ~17-20% share, after tax and marketing | estimated |

## What a government can move
| Line | Lever | Who decides | Level (federal / state: which states / local) | Issue tag |
|---|---|---|---|---|
| P1 State gaming taxes (-$1.6B; 1 pp in one big state ≈ $2.5-8M; a typical 5-10 pp hike in one big state ≈ -$25M to -$80M) | Tax rate, per-wager fees, promo deductibility | Governor + legislature (budget bills) | State: NY, PA, NJ, MI, IL, OH, MA, MD, AZ, CO, ... | `gaming-betting` |
| P6 New iGaming / OSB legalization (upside, ~$75-200M per large state at maturity) | Legalization statute; constitutional amendment / ballot in some states; tribal compacts | Legislature, governor, voters | State: NY, IL, OH, MD, MA, IN (iGaming); CA, TX, GA, FL, MN, SC, AL (OSB) | `gaming-betting` |
| P3 Predictions (-$100M to -$300M 2026 spend; competitor threat from Kalshi/Polymarket to Sportsbook) | CEA amendments; CFTC rules on sports event contracts; state cease-and-desist | Congress + President; CFTC; courts; state gaming regulators / AGs | Federal + state | `other: prediction markets / CFTC` (closest book tag `gaming-betting`) |
| P2 Federal wagering excise tax (-$134M) | Repeal or change of 0.25% excise | Congress + President | Federal | `gaming-betting` |
| P4 Advertising, promo and bet-limit rules (SAFE Bet Act-type bills; state rules) | Ad limits, affordability checks, deposit limits | Congress; state gaming commissions + legislatures | Federal + state | `gaming-betting` |
| P5 DFS legality/tax; lottery courier bans (e.g. Texas 2025) | Statute, AG opinion, lottery rule | State AGs, legislatures, lottery commissions | State | `gaming-betting` |
| Sweepstakes-casino bans (competitor; small upside) | Ban statute | Legislature + governor; AGs | State | `gaming-betting` |

Base $620M Adjusted EBITDA; the movable lines touch essentially all of it (state taxes alone ≈ 2.6x the base), but a single election outcome reaches tens of $M, not hundreds.

## Locked in
- Federal gambling-loss deduction capped at 90% from 2026 (P.L. 119-21, 2025 reconciliation law); works through bettor demand, not sized.
- 2025 state tax hikes already enacted: NJ to 19.75%, IL per-wager fee (Jul 2025), MD to 20%, LA to 21.5% (an unsourced Jefferies estimate puts their 2026 pressure at ~$80M; not verified here).
- NJ and VA governors elected 2025 (in office through 2029-30); NC governor not up until 2028.
- Ontario is provincial; no Nov 3 contest reaches it.

Changes from the 2026-10-22 draft: added issue tags; moved the Jefferies ~$80M figure from a sized line to an unsourced note (no URL); moved the 90% loss-deduction cap to Locked in (it is enacted law, not a movable line before 2029).
