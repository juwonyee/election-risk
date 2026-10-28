# Ford Motor (F): profit structure
Written 2026-10-27 (rewritten from the 2026-10-22 analyst draft; research not redone). Base: FY2025 company adjusted EBIT $6,780M (verified, https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm)

Ford steers by adjusted EBIT; GAAP operating income was -$9,169M (verified, XBRL `OperatingIncomeLoss`) because of $17.4B of special items (Model e impairment, EV program cancellations, BlueOval SK JV disposition). 2026 guidance after Q2 2026: adjusted EBIT $10-11B (verified, https://s205.q4cdn.com/882619693/files/doc_financials/2026/q2/Ford-Motor-Company-Q2-2026-Press-Release.pdf); context only, not the base. FY2025 revenue $187.3B; US $122.6B (65%), Canada $14.5B, UK $12.3B, Mexico $2.5B, other $35.4B (verified, 10-K geographic note).

Sources: S10K = https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm ; SQ2 = https://s205.q4cdn.com/882619693/files/doc_financials/2026/q2/Ford-Motor-Company-Q2-2026-Press-Release.pdf

## Where operating profit comes from
| # | Line | $ / yr | Source | Status |
|---|---|---|---|---|
| 1 | Ford Pro (commercial, government, rental; Super Duty, Transit; services) EBIT | +$6,843M (rev $66,286M) | S10K | verified |
| 2 | Ford Blue (ICE + hybrid retail; F-150, Bronco, Explorer, Lincoln) EBIT | +$3,024M (rev $101,019M) | S10K | verified |
| 3 | Ford Model e (EVs, software) EBIT | -$4,806M (rev $6,670M) | S10K | verified |
| 4 | Ford Credit EBT (auto finance; ~$110B receivables) | +$2,557M | S10K | verified |
| 5 | Corporate Other | -$838M | S10K | verified |
| = | Company adjusted EBIT | **$6,780M** | S10K | verified |

## Policy lines inside those
| # | Line | $ / yr | Source | Status |
|---|---|---|---|---|
| 6 | Tariffs on imported vehicles, parts, steel/aluminum (Sec. 232 autos/parts and metals; IEEPA tariffs until struck down 2026-02-20) | 2025: gross ~-$3,000M, net ~-$2,000M; 2026 net guided "better than -$1,000M" after offset expansion; $974M refund receivable end-2025; $1.3B reimbursement booked Q1 2026 | S10K; SQ2 | verified (2025), estimated (2026) |
| 7 | Regulatory compliance credit purchases (EPA GHG, CARB/ZEV states, Canada, EU CO2) | ~-$700M expense 2025; $1.6B outstanding purchase obligations, cancellable if the requirement disappears | S10K | verified |
| 8 | CAFE civil penalties | $0 (2025 law set light-duty penalty to $0) | S10K | verified |
| 9 | Consumer EV tax credits (30D/45W) | eliminated by P.L. 119-21 (2025); effect sits inside the Model e loss | S10K risk factors | verified (status); size not disclosed |
| 10 | 45X battery production credit | +$53M (2025), +$105M (2024), reduction to cost of sales; FEOC limits added 2025 | S10K | verified |
| 11 | US hourly labor (UAW, ~56,300 US hourly employees; contract to Apr 2028) | ~-$8,000 to -9,000M wage+benefit cost (56,300 x ~$150k loaded) | S10K headcount | estimated |
| 12 | USMCA trade with Canada/Mexico (plants in Ontario and Mexico; Canada revenue $14.5B) | inside line 6; split not disclosed | S10K | not disclosed |
| 13 | Government fleet sales (federal, state, local; inside Ford Pro) | not disclosed | S10K | not disclosed |
| 14 | State/local plant incentives (TN BlueOval City, KY battery plants, MI Marshall) | capital grants, not a yearly EBIT line; not disclosed | S10K | not disclosed |
| 15 | Income tax (adjusted ETR 20%; federal + CA, NJ, KY, MI, WI, IL, MD) | below EBIT; not in base | S10K | verified (rate) |
| 16 | Ford Credit funding cost / consumer-lending regulation (CFPB, state lending law) | inside line 4; not sized | S10K | not disclosed |
| 17 | Vehicle safety regulation / recalls (NHTSA) and warranty | warranty is large; not separately disclosed in the EBIT bridge | S10K | not disclosed |

## What a government can move
| Line | Lever | Who decides | Level (federal / state: which states / local) | Issue tag |
|---|---|---|---|---|
| 6 Tariffs (~-$1,000 to -2,000M net) | Sec. 232 auto/parts and metals tariffs and the offset/relief program; any new tariff authority | President / Commerce; Congress by law; courts | Federal | `tariffs-trade` |
| 12 USMCA | 2026 USMCA joint review, content rules, Canada/Mexico tariffs | President / USTR; Congress | Federal (+ Canada, Mexico) | `tariffs-trade` |
| 11 Labor (~-$8-9B cost) | NLRB rules and appointments, federal labor law; state right-to-work (UAW pay is far above any minimum wage, so minimum wage is not material) | Congress / President; state legislatures and governors (MI, KY, OH, MO, IL, TN) | Federal + state | `other: labor-law` |
| 7 Compliance credits (~-$700M) | EPA GHG vehicle standards (EPA proposed ending them in 2025); California waiver / Advanced Clean Cars II and states that follow CARB | EPA (President); Congress (CRA); CARB, CA governor/legislature, other states' governors/legislatures | Federal + state: CA and CARB-following states | `clean-cars-ev` |
| 9 EV purchase credits | Federal 30D/45W (repealed); state EV rebates (CA, CO, NJ, NY, etc.) | Congress + President; state legislatures/governors | Federal + state | `clean-cars-ev` |
| 10 45X (+$53M) | Credit size, FEOC rules (Marshall, MI LFP plant on a CATL license) | Congress; Treasury | Federal | `clean-cars-ev` |
| 8 CAFE penalties ($0) | Penalty rate, CAFE stringency (NHTSA) | Congress; NHTSA (President) | Federal (locked in for now) | `clean-cars-ev` |
| 13 Government fleet (not disclosed) | Federal procurement (GSA), state/local fleet budgets and EV-fleet mandates | Congress / agencies; governors / legislatures | Federal + state + local | `other: government-fleet-procurement` |
| 14 State incentives (not disclosed) | Plant grants, property-tax abatements | Governors / legislatures / economic-development boards (MI, TN, KY) | State: MI, TN, KY | `corporate-sales-property-tax` |
| 15 Taxes (below EBIT) | Corporate rate, state income/franchise tax | Congress; state legislatures | Federal + state | `corporate-sales-property-tax` |
| 16 Ford Credit (not sized) | Consumer-lending rules (CFPB), state usury/lending law | CFPB (President); Congress; state legislatures / AGs | Federal + state | `other: consumer-lending` |
| 17 Safety/recalls (not sized) | NHTSA rules and enforcement, incl. driver-assist/automation rules | NHTSA (President) | Federal | `transport-ai-vehicles` |
| Dealer franchise laws (not sized) | Laws protecting the franchised-dealer model vs direct-sale rivals | State legislatures | State | `other: dealer-franchise` |

Not movable by a US government decision in the near term: Ford Blue/Pro pricing and volume (market), Novelis aluminum supply disruption (~-$2B in 2025), Europe results (EU/UK governments), FX.

## Locked in
- CAFE light-duty civil penalty set to $0 by the 2025 reconciliation law (P.L. 119-21): ~$0 cost; no election before 2029 can restore it without the President's signature.
- Federal consumer EV credits 30D/45W repealed by P.L. 119-21: the demand loss sits inside Model e's -$4,806M; not separately sized.
- 45X battery credit with FEOC limits (P.L. 119-21): +$53M in 2025.
- UAW contract through April 2028: US hourly wage path fixed regardless of the election.
- IEEPA tariffs struck down 2026-02-20: refunds ($974M receivable end-2025) flow regardless.

Base: FY2025 adjusted EBIT $6,780M. Movable lines with a size: tariffs (~$1-2B net cost) and compliance credits (~$0.7B), together ~15-40% of the base; labor (~$8-9B cost) is large but its policy levers are not sized.
