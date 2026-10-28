# Coinbase (COIN): profit structure
Written 2026-10-27 (rewritten from the 2026-10-22 analyst draft; research not redone). Base: FY2025 operating income $1,435.4M (verified, https://www.sec.gov/Archives/edgar/data/1679788/000167978826000015/0001679788-26-000015-index.htm)

Revenue FY2025 $7,181.3M; 84% US (10-K MD&A); no state split disclosed.
Caveat: H1 2026 operating **loss** of $134.9M (Q2 2026: -$113.5M); H1 2026 adjusted EBITDA $511.1M (10-Q Q2 2026,
https://www.sec.gov/Archives/edgar/data/1679788/000167978826000088/coin-20260630.htm). FY2025 is kept as the base
because it is the latest full year; shares of a 2026 run-rate would be far larger.

K = FY2025 10-K above; Q = Q2 2026 10-Q above.

## Where operating profit comes from
| # | Line | $ / yr | Source | Status |
|---|---|---|---|---|
| R1 | Consumer transaction revenue (spot crypto fees/spread; since 2025-26 also equities, futures, perps, prediction markets) | $3,322.8M | K | verified |
| R2 | Institutional transaction revenue (prime, Deribit derivatives) | $479.7M | K | verified |
| R3 | Other transaction revenue | $252.9M | K | verified |
| R4 | Stablecoin revenue (share of interest on USDC reserves, Circle arrangement) | $1,348.8M | K | verified |
| R5 | Blockchain rewards (staking), gross | $677.4M | K | verified |
| R6 | Interest and finance fee income (customer cash, lending) | $247.0M | K | verified |
| R7 | Other subscription and services (Coinbase One, custody, etc.) | $554.8M | K | verified |
| R8 | Corporate interest and other income | $297.9M | K | verified |
| C1 | Transaction expense (blockchain rewards fees 427.5, rebates 221.5, payment processing 194.6, reversals 132.7) | -$1,020.2M | K | verified |
| C2 | Technology and development (employee 1,052.6; hosting 322.1) | -$1,670.6M | K | verified |
| C3 | Sales and marketing (incl. USDC rewards paid to users 441.3) | -$1,058.6M | K | verified |
| C4 | General and administrative (employee 664.8; professional services 292.6; customer support 224.2) | -$1,619.6M | K | verified |
| C5 | Losses on crypto held for operations | -$20.7M | K | verified |
| C6 | Other operating expense (mainly 2025 data-theft incident 345.2, one-off) | -$356.1M | K | verified |
| = | Operating income | $1,435.4M | K | verified (7,181.3 - 1,020.2 - 1,670.6 - 1,058.6 - 1,619.6 - 20.7 - 356.1 = 1,435.5, rounding) |

## Policy lines inside those
| # | Line | $ / yr | Source | Status |
|---|---|---|---|---|
| P1 | Prediction-market fees (via Kalshi, inside R1) | ~$100M+ annualized (Q2 2026) | https://quartr.com/events/coinbase-global-inc-coin-q2-2026_3erzI00Q ; Q (mentions prediction-market exchange fees, no number) | estimated (press summary of Q2 letter) |
| P2 | Interest-rate-sensitive revenue (R4 + R6 + R8) | $1,893.7M | K (10-K sensitivity: +/-150bp = +/-$540M) | verified (sum of verified lines) |
| P3 | USDC rewards paid to users (inside C3) | -$441.3M | K | verified |
| P4 | Staking revenue exposed to state securities actions (inside R5) | not disclosed (state split) | K risk factors | — |
| P5 | Compliance / licensing cost (inside C4) | not disclosed | K | — |
| P6 | Income tax (below OI; ETR 17.2%) | $261.7M | K | verified |

## What a government can move
| Line | Lever | Who decides | Level (federal / state: which states / local) | Issue tag |
|---|---|---|---|---|
| R1 consumer trading ($3,322.8M) | Crypto market-structure law (which tokens trade, SEC vs CFTC), SEC/CFTC rules, crypto tax reporting / de minimis | Congress (CLARITY Act, Senate pending), President (signs; appoints SEC/CFTC chairs), SEC, CFTC | federal | `crypto` |
| P2 interest-sensitive revenue ($1,893.7M) | Short-term interest rates | Federal Reserve FOMC; President nominates Fed chair/governors, Senate confirms | federal | `other: monetary policy (Fed rates)` |
| R4 + P3 stablecoin yield/rewards ($1,348.8M revenue; -$441.3M cost) | Rules on stablecoin rewards/yield and issuer economics (CLARITY sec. 404 compromise, May 2026); Treasury/OCC GENIUS Act rules | Congress + President; Treasury, OCC | federal | `crypto` |
| R5 staking ($677.4M gross) | Staking treated as a securities offering | State securities regulators (new-customer staking paused in CA, NJ, SC, WI, MD); SEC; Congress | state: CA, NJ, SC, WI, MD; federal | `crypto` |
| R2 institutional / derivatives ($479.7M) | Derivatives and market-structure rules | CFTC, SEC, Congress; foreign regulators (Deribit offshore) | federal (+ foreign) | `crypto` |
| P1 prediction markets (~$100M+) | Whether event contracts (esp. sports) are state-regulated gambling or CFTC-only | State gaming boards, AGs, legislatures, governors (NV, CT, IL, MI, NJ, MD and others; Coinbase sued CT/IL/MI Dec 2025); federal courts; CFTC; Congress | state: NV, CT, IL, MI, NJ, MD, others; federal | `gaming-betting` |
| C4 / C6 licensing and enforcement (not disclosed) | Money-transmitter licences, BitLicense, AG and privacy enforcement | NYDFS, CA DFPI, state AGs | state: NY, CA, others | `crypto` |
| P6 tax ($261.7M, below OI) | Corporate rate, crypto tax rules | Congress; states | federal / state | `corporate-sales-property-tax` |

## Locked in
- GENIUS Act (stablecoin law, July 2025): stablecoin issuer framework is law; the Treasury/OCC rules under it are in progress.
- R&D expensing restored by P.L. 119-21 (July 2025): below OI, through at least 2028.
- 2025 data-theft incident cost ($345.2M) is one-off and already booked.

Base $1,435.4M FY2025 operating income; the movable lines touch essentially all revenue (R1 + R2 + R5 + P2 = ~$6.4B of $7.2B revenue; P2 includes R4).
