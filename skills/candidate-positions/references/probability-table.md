# Probability table: if this candidate wins, how likely is the policy?

Read this before giving any `p`. Every cell comes from published statistics or research; the full notes,
numbers and links are in the repository under `research/probability-table/` (Q1 pledges, Q2 legislation,
Q3 vetoes, Q4 appointments, Q5 attorneys general and executive orders, Q6 ballot measures and federal).

**Use the table as written. Do not tune a cell for one case.** Your judgment goes into choosing the route
(make, block, appoint, sue) and the legislature situation; the number then comes from the table. If two rows
fit, use the lower.

All research covers a full term (about 4 years). We use the numbers for "within about 2 years" unchanged and
call them an **upper bound**. No raise for headline pledges: research finds prominent pledges are not kept
more often (Q1).

## A. Make: the winner enacts a new policy

| Route | p | Range | Basis |
|---|---|---|---|
| Alone (executive order, agency action, appointment-free) | **0.45** | 0.35–0.55 | Pledges fully kept by a US president's party over a term: 47% (Royed et al. 2019, n=1,078); status-quo-changing pledges 43%; governors' emergency orders upheld in court 86% (Q1, Q5) |
| Needs a legislature of the winner's party, strong majority | **0.35** | 0.30–0.40 | Governors' policy proposals enacted ~38% when their party holds ~79% of seats (Kousser & Phillips, n=1,088) (Q2) |
| Needs a legislature of the winner's party, narrow majority | **0.25** | 0.20–0.30 | Interpolated from the same regression (Q2) |
| Needs a legislature of the other party | **0.15** | 0.10–0.20 | Governors' proposals enacted ~16% when their party holds 14% of seats; a divided-government governor kept 33% of pledges (Q1, Q2) |
| Voters: citizen initiative | **0.45** | 0.42–0.51 | Initiatives passed 42% (1904–2021, n=2,653), 51% in the 2010s (Q6) |
| Voters: legislative referral | **0.70** | 0.60–0.75 | Legislatively referred amendments passed 68% in 2024 (n=73) (Q6) |

## B. Federal (the President is a Republican with a veto until January 2029)

| Case | p | Basis |
|---|---|---|
| Partisan bill from a Democratic chamber, President opposed | **0.05** | Majority-party agenda items passed over minority opposition 4% (Curry & Lee); 93% of bills with a formal veto threat did not become law (2001–2017) (Q3, Q6) |
| Bipartisan bill the President supports | **0.40** | 4 of 6 flagship bills of a 2007 opposite-party Congress were signed; 45% of bills reaching a 60-vote cloture vote became law (117th Congress) (Q6) |
| Republican agenda through budget reconciliation, Republicans keep both chambers | **0.35** | No direct study; borrows A "same party, strong majority" (judgment) |
| Reconciliation when only the House flips | **≈0** | No such law since 1987 (Q6) |

## C. Block: the winner vetoes or signs

Policy p = P(legislature passes it) × P(the winner signs it).

| Item | p | Basis |
|---|---|---|
| Winner pledged to veto: chance the policy still happens | **0.07** | Governors' vetoes overridden 5.2% (2010–2020, 578 of 11,173); 93% of formally threatened bills did not become law (Q3) |
| ...but the other party holds a veto-proof majority | that state's recent override record (0.4–1.0) | Kentucky 2025 overrode almost all; North Carolina 2017–18 overrode 23 of 28 (Q3) |
| Winner pledged to sign: P(legislature passes), ordinary bill | **0.25** | 25–28% of introduced state bills become law; use the state's own rate when known (Q2) |
| ...bill with leadership backing or already passed one chamber | **0.40** | No direct statistic; between 0.25 and ~0.70 for a bill that passed one chamber in the same session (judgment) |
| Winner is a chamber majority that keeps the bill off the floor | **0** (judgment) | A majority controls its own floor; use `block: majority`. `block: veto` is only for an executive with a veto |

## D. Appoint: utility commissions and other boards

| Item | p or size | Basis |
|---|---|---|
| New governor appoints a commission majority within 2 years | **0.30** (0 in the ~11 states that elect commissioners) | Commissioner turnover ~19–21% a year (Q4) |
| Effect of that majority on allowed return on equity | **about −0.15 percentage points** (not statistically significant) | 13–20 bp difference by Democratic share of commissioners (Dunkle Werner & Jarvis, 3,390 rate cases) (Q4) |
| Federal regulator confirmations with an opposite-party Senate | 70% → 49% | 1999–2016 nominees: same-party Senate 69.5%, opposite 49.3% (Q4) |

Size appointment-route impacts with the D effect, not with a guessed rate cut.

## E. Sue: attorneys general

| Item | p | Basis |
|---|---|---|
| Once filed, the company pays (settlement or loss) | **0.95** | ~80% of single-state suits settle, multistate suits all settled, AGs won 31 of 32 contested (Q5) |
| ...resolved within 2 years | **0.70** | 28% of suits run past 2 years (Q5) |
| Difference made by the AG's party (suits against companies) | **0.03–0.11** | Multistate suits against companies are mostly bipartisan; partisan splits are in suits against the federal government (Nolette) (Q5) |
| Pledged suit actually filed | use A "alone" 0.45 | No study found (Q5) |

## F. Cells with no evidence (judgment)

| Item | p | Why |
|---|---|---|
| Vague position ("open to", "would look at") | **0.05** | No study found |
| No stated position | **0** | Never infer a position from party |
| Outcome decided by a court | difference between candidates **0** | A candidate changes only whether a suit is filed (use E) |

## Election swing

For each policy, the **election swing** is the difference between the two leading candidates' `p`. A swing
of 0.10 or more makes the contest a candidate for the election headline.
