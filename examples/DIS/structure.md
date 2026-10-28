# Walt Disney (DIS): profit structure
Written 2026-10-27 (rewritten from the 2026-10-22 analyst draft; research not redone). Base: FY2025 (year to Sep 27, 2025) total segment operating income $17,551M (verified, https://www.sec.gov/Archives/edgar/data/1744489/000174448925000155/dis-20250927.htm). Disney steers by segment OI; GAAP pre-tax income was $12,003M after corporate costs, restructuring, interest and amortization.

Sources:
- [10-K] FY2025 10-K: https://www.sec.gov/Archives/edgar/data/1744489/000174448925000155/dis-20250927.htm
- [ER] Q3 FY2026 earnings release (Aug 5, 2026): https://www.sec.gov/Archives/edgar/data/1744489/000174448926000056/fy2026_q3xerxex991.htm
- [10-Q] Q3 FY2026 10-Q: https://www.sec.gov/Archives/edgar/data/1744489/000174448926000057/dis-20260627.htm

Run-rate: 9 months FY2026 segment OI $14,758M vs $14,071M (+5%) [ER].

## Where operating profit comes from
| # | Line | $ / yr | Source | Status |
|---|---|---|---|---|
| 1 | Entertainment: Linear Networks, Domestic (ABC network, 8 owned ABC stations, Disney/Freeform/FX/NatGeo channels) | OI $2,378M (rev $8,309M) | [10-K] segment note | verified |
| 2 | Entertainment: Linear Networks, International + A+E equity income | OI $132M + $445M | [10-K] | verified |
| 3 | Entertainment: Direct-to-Consumer (Disney+, Hulu) | OI $1,327M (rev $24,614M) | [10-K] | verified |
| 4 | Entertainment: Content Sales/Licensing (theatrical, home entertainment) | OI $392M | [10-K] | verified |
| 5 | Sports: ESPN Domestic | OI $2,801M (rev $16,085M) | [10-K] | verified |
| 6 | Sports: ESPN International, Star India, equity | OI $81M | [10-K] | verified |
| 7 | Experiences: Domestic Parks & Experiences (WDW Florida, Disneyland California, Disney Cruise Line, DVC, Aulani) | OI $6,375M (rev $25,191M) | [10-K] | verified (total) |
| 7a | - Walt Disney World, Florida | ~$3,000-3,500M | not disclosed; about half of domestic P&E by resort size | estimated |
| 7b | - Disneyland Resort, Anaheim, California | ~$1,500-2,000M | not disclosed | estimated |
| 7c | - Disney Cruise Line | ~$1,000M | not disclosed | estimated |
| 8 | Experiences: International Parks (Paris, Hong Kong 48%, Shanghai 43%, Tokyo royalties) | OI $1,442M | [10-K] | verified |
| 9 | Experiences: Consumer Products (licensing + merchandise) | OI $2,178M | [10-K] | verified |
| 10 | Corporate and unallocated shared expenses (below segment OI) | -$1,646M | [10-K] | verified |
| 11 | Interest expense, net (below OI) | -$1,305M | [10-K] | verified |

Segment check: Entertainment 4,674 + Sports 2,882 + Experiences 9,995 = 17,551.

## Policy lines inside those
| # | Line | $ / yr | Source | Status |
|---|---|---|---|---|
| P1 | Production tax incentives (cost offset inside lines 1-4; CA, GA, NY, NM, UK and others) | ~$700M a year offset; $1.8B receivable; state split not disclosed | [10-K] Note 7 | verified (total) |
| P2 | Experiences operating labor (mostly FL and CA park staff; ~172,000 US employees) | -$8,948M | [10-K] | verified (total) |
| P3 | Experiences infrastructure incl. property taxes, utilities, fuel | -$3,511M; property-tax share not disclosed | [10-K] | verified (total) |
| P4 | Tariff cost on imported consumer products (toys, apparel) | ~$100M order of size (Q3 FY26 booked a ~$100M refund of tariffs paid earlier in FY26) | [ER] | estimated |
| P5 | Broadcast licences and the national ownership cap (ABC stations, network) | inside line 1 ($2,378M) | [10-K] | verified (line) |
| P6 | Federal income-tax preferences (FDII, now FDDEI under P.L. 119-21), below OI | ~$260M benefit (2.2 pts x $12,003M pre-tax) | [10-K] tax note | estimated |

## What a government can move
| Line | Lever | Who decides | Level (federal / state: which states / local) | Issue tag |
|---|---|---|---|---|
| 7a Walt Disney World, Florida (~$3.0-3.5B) | Land use and development rights (CFTOD board); special-district and property-tax law; constitutional amendments | FL governor (appoints CFTOD board, FL Senate confirms), FL legislature, FL voters, Orange/Osceola counties | state: FL; local | `corporate-sales-property-tax` |
| P2 Experiences labor (-$8.9B) | Minimum wage floors (FL constitutional schedule reaches $15 on Sep 30, 2026; CA state; Anaheim resort-district measure; federal floor) | FL voters/legislature, CA legislature + governor + voters, Anaheim council/voters, Congress | state: FL, CA; local: Anaheim; federal | `labor-min-wage` |
| 7b Disneyland Resort, California (~$1.5-2.0B) | Zoning (Disneyland Forward), state labor and tax law | Anaheim city council and local ballot; CA legislature + governor; CA voters | state: CA; local | `labor-min-wage` / `corporate-sales-property-tax` |
| 1 / P5 Domestic Linear Networks ($2.4B) | Broadcast licences, 39% national ownership cap, network rules | FCC (commissioners named by President, confirmed by Senate); cap set by Congress | federal | `other: broadcast-fcc` |
| P1 Production incentives (~$700M offset) | State film credits ($750M/yr California program; Georgia; New York; New Mexico) | CA, GA, NY, NM legislatures + governors | state: CA, GA, NY, NM | `film-tax-credits` |
| 5 ESPN Domestic ($2.8B) | Antitrust review of sports-rights deals and carriage; sports-betting legality (ESPN BET partner revenue) | DOJ/FTC (President); state legislatures and voters | federal; state: all | `tech-antitrust-privacy` / `gaming-betting` |
| 3 Direct-to-Consumer ($1.3B) | Kids' online safety, privacy, app-store rules | Congress, FTC, state legislatures + AGs (CA and others) | federal; state | `kids-online` |
| 9 / P4 Consumer Products ($2.2B; tariff cost ~$100M) | Import tariffs on toys and apparel (Sec. 301/232) | President, USTR, Commerce; Congress | federal | `tariffs-trade` |
| 4 Content Sales ($0.4B) | Proposed tariff on foreign-made films | President / Commerce | federal | `tariffs-trade` |
| 7 Inbound international visitors | Visa and travel policy | President / State Dept | federal | `other: travel-visa` |
| P3 Property tax and utilities | Property-tax rates and homestead/non-homestead caps; utility rates | FL legislature, FL voters, counties; FL PSC | state: FL; local | `corporate-sales-property-tax` / `utilities` |
| P6 Federal tax (below OI) | Corporate rate, FDDEI | Congress + President | federal | `other: federal-corporate-tax` |

## Locked in
- P.L. 119-21 (2025 reconciliation law): 21% federal rate and FDDEI changes stay through 2028 (President's veto); below operating income.
- Florida minimum wage schedule (2020 Amendment 2) reached $15 on Sep 30, 2026; already in the cost base.
- Section 301/232 tariffs in force since 2026-07-24; Congress has no disapproval route.
- CFTOD (Florida) replaced Reedy Creek in 2023; Disney and the district settled litigation in 2024 with a 15-year development agreement.

Base $17,551M segment OI. Movable lines touch about $11-12B of segment OI (Florida and California parks, linear networks, ESPN, production credits), plus an $8.9B labor cost line.
