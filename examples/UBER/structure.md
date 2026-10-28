# Uber Technologies (UBER): profit structure
Written 2026-10-27 (rewritten from the 2026-10-22 analyst draft; research not redone). Base: FY2025 GAAP income from operations $5,565M (verified, https://www.sec.gov/Archives/edgar/data/1543151/000154315126000015/uber-20251231.htm)

Recent run-rate: Q2 2026 GAAP income from operations $1,890M (Q2 2025: $1,450M) (verified, https://www.sec.gov/Archives/edgar/data/0001543151/000154315126000027/uberq226earningspressrelea.htm).
Below operating income, not in the base: interest +743, interest expense −440, other −68, tax benefit +4,346 (includes a one-off $5.0B Netherlands valuation-allowance release).

## Where operating profit comes from
| # | Line | $ / yr | Source | Status |
|---|---|---|---|---|
| 1 | Mobility segment adj. EBITDA (revenue $29,670M) | +$7,899M | 10-K FY2025 note 13 (URL above) | verified |
| 2 | Delivery segment adj. EBITDA (revenue $17,248M) | +$3,572M | 10-K note 13 | verified |
| 3 | Freight segment adj. EBITDA (revenue $5,099M) | −$33M | 10-K note 13 | verified |
| 4 | Corporate G&A and Platform R&D | −$2,708M | 10-K note 13 | verified |
| 5 | Stock-based compensation | −$1,826M | 10-K note 13 | verified |
| 6 | Depreciation and amortization | −$719M | 10-K note 13 | verified |
| 7 | Legal, non-income tax, regulatory reserve changes and settlements | −$564M | 10-K note 13 | verified |
| 8 | Other (impairments, deal costs, lease, restructuring) | −$56M | 10-K note 13 | verified |
| | **Income from operations** | **$5,565M** | 10-K | verified |
| S1 | Revenue, United States | $23,771M (46% of total) | 10-K geographic information | verified |
| S2 | Revenue, United Kingdom | $10,609M (20%) | 10-K geographic information | verified |
| S3 | US share of Mobility + Delivery segment EBITDA | ~$5.0B (≈45% of $11.47B) | assumes segment EBITDA splits like revenue; not disclosed | estimated |
| S4 | US Mobility segment EBITDA | ~$3.6–4.0B | ~45–50% of $7,899M | estimated |
| S5 | US Delivery segment EBITDA | ~$1.4–1.6B | ~40–45% of $3,572M | estimated |
| S6 | California share of US Mobility | ~15–20% (~$0.6–0.8B EBITDA) | not disclosed; largest US state by population, LA/SF top metros; low confidence | estimated |
| S7 | New York City share of US Mobility | ~10–15% (~$0.4–0.6B EBITDA) | not disclosed; top-5 metro; low confidence | estimated |

## Policy lines inside those
| # | Line | $ / yr | Source | Status |
|---|---|---|---|---|
| P1 | Mobility insurance expense (auto liability, UM/UIM) | total not disclosed; **+$851M increase in 2025**; insurance reserves $12.5B at 12/31/25 (short $3,387M + long $9,076M); US&CAN costlier than other regions | 10-K MD&A | verified (increase, reserves) |
| P2 | Mobility driver payments and incentives (platform-participant direct costs) | $8,683M; +$1.6B increase in 2025 | 10-K | verified |
| P3 | Driver classification and pay floors (CA Prop 22 floor 120% of state minimum wage; NYC TLC per-mile/minute rate; WA, MN pay laws; MA 2024 driver-union ballot law; CA 2025 driver-union law) | inside P2; not separately disclosed | 10-K risk factors | verified (laws), not disclosed ($) |
| P4 | Courier pay floors (NYC DCWP, Seattle PayUp) | inside Delivery costs; not disclosed | 10-K risk factors | not disclosed |
| P5 | Per-trip taxes and surcharges (Chicago up to $3/trip, SF surcharge, NYC congestion fee on FHV trips), airport fees | mostly passed to riders; not disclosed | 10-K risk factors | not disclosed |
| P6 | Legal and regulatory reserves (state AG suits, FTC Uber One case, state unemployment-tax audits such as NJ) | line 7, −$564M | 10-K note 13 | verified |

## What a government can move
| Line | Lever | Who decides | Level (federal / state: which states / local) | Issue tag |
|---|---|---|---|---|
| US Mobility EBITDA (S4, P2) | Driver classification (employee vs contractor). A big-state reclassification raises driver cost 20–30% of driver pay; one CA- or NY-sized shock ≈ $0.2–0.5B (estimated) | State legislatures, AGs, courts, ballot measures; federal DOL contractor rule (President/agency), NLRB, Congress (PRO Act) | federal and state: CA, NY, MA, NJ, IL, WA, MN | `gig-workers` |
| US Mobility EBITDA (P3) | Driver minimum-pay floors and sectoral bargaining. A 10% floor increase in one large market ≈ $0.05–0.2B (estimated) | City councils / TLC (mayor appoints), state legislatures, governors, ballot measures | state: CA, NY, MA, WA, MN, IL; local: NYC, Seattle, Chicago | `gig-workers` |
| Mobility insurance cost (P1) | Tort rules (attorney fees, medical-lien damages), required coverage limits (UM/UIM), insurance rate approval. ≈ $0.05–0.3B per large state (estimated) | State legislatures, ballot measures, insurance commissioners (elected in some states), governors | state: CA, NV, NY, FL, TX, GA, IL | `insurance` |
| Line 7 legal/regulatory reserves (P6) | Enforcement: AG suits, FTC, state unemployment-tax audits. Reserve swings ≈ $0.1–0.5B a year (estimated) | State AGs (elected), FTC (President appoints), state labor agencies | federal and state: CA, NY, NJ, MA, IL | `other: state AG and FTC enforcement` |
| US Delivery EBITDA (S5, P4) | Courier minimum pay, delivery-fee caps. Increments ≈ $0.02–0.1B (estimated) | Mayor/city council, city agencies | local: NYC, Seattle, Chicago | `gig-workers` |
| Mobility/Delivery demand (P5) | Per-trip taxes, surcharges, congestion pricing, airport fees. ≈ $0.01–0.1B (estimated) | City councils, local ballots, state legislatures, MTA/state; federal DOT on congestion pricing | local: NYC, Chicago, SF; state: NY, IL | `other: rideshare trip taxes` |
| Merchant and floor-linked costs | State/city minimum wage (feeds the Prop 22 floor and merchant costs). ≈ $0.01–0.1B per state (estimated) | State legislatures, ballot measures, city councils | state: CA and others with indexed floors | `labor-min-wage` |
| Future Mobility (no profit today) | Autonomous-vehicle rules (driverless permits, AV bills). $0 in the FY2025 base | State legislatures, DMV/CPUC, governors; NHTSA/Congress | federal and state: CA, TX, AZ, NY | `transport-ai-vehicles` |
| Freight (−$33M) | Tariffs and trade volumes. Small; segment near breakeven | President, Congress | federal | `tariffs-trade` |
| Taxes (below operating income) | Corporate tax, CAMT, digital services taxes abroad | Congress/President; foreign governments | federal; non-US | `corporate-sales-property-tax` |
| UK/EMEA (S2) | VAT on platform fares, worker status, EU Platform Work Directive. Large (UK 20% of revenue) but not a US Nov 3 decision | UK government, EU and member states | non-US | `other: non-US regulation` |

## Locked in
- California SB 623 (signed 2026-06-25): medical-lien damage limits plus rideshare safety rules; Uber's and the Consumer Attorneys' competing November initiatives were withdrawn (https://news.bloomberglaw.com/litigation/uber-avoids-california-ballot-war-as-governor-signs-lawyers-deal).
- California Prop 22 (2020) upheld by the CA Supreme Court; drivers remain contractors with an earnings floor.
- Massachusetts AG case settled June 2024 (drivers stay contractors, with a pay floor); MA 2024 driver-union ballot question passed.
- NYC TLC minimum pay (since 2019) and FHV licence cap remain.
- Federal tax changes enacted in 2025 (P.L. 119-21) through 2028.
- Nevada contingency-fee initiative was blocked by the NV Supreme Court in Jan 2025 (https://www.fox5vegas.com/2025/01/28/nevada-supreme-court-shuts-down-ubers-ballot-effort-cap-attorney-fees/); whether a revised version is on the 2026 ballot is not confirmed.

Gaps: Uber discloses no state- or city-level revenue or profit (all state splits are estimates); total insurance expense is not disclosed.

Movable lines touch roughly the US Mobility + Delivery EBITDA (~$5.0B, estimated) and the −$564M reserve line, against a $5,565M base.
