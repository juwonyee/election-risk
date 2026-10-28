# Q2 — How likely is a bill or a governor's proposal to become law?

Researched 2026-10-24. Every number below is quoted from or computed directly from the cited source. Where I computed something myself it is marked **(computed)**. Where a source could only be seen through a search snippet or a secondary write-up, it says so.

## 1. Findings table

### (a) State bill passage rates (introduced → enacted)

| Source | Measure | Number | n / years | URL |
|---|---|---|---|---|
| FiscalNote 2025 State Sessions Recap (via Governing, 2025-09-11, FiscalNote authors) | Share of introduced state bills enacted, all states | **28%**; >135,500 bills introduced (87,500 in 2024; ~132,600 in 2023). Colorado 73.5%, Virginia 60.7%, Georgia 60.1%, Texas 35.5%, New York 12% | 2025 sessions, 50 states | https://www.governing.com/politics/in-2025-states-continued-to-be-more-active-than-congress (FiscalNote page itself returned 403: https://fiscalnote.com/2025-state-sessions-recap) |
| FiscalNote 2025 recap, **by party control**, as cited by Yankee Institute (secondary) | Average passage rate by control | **Republican trifecta 36.4%; Democratic trifecta 19.8%; split government 18.6%** | 2025; n states per group and weighting not stated | https://yankeeinstitute.org/?p=35922 |
| FiscalNote 2024 State Sessions Recap (search snippet only; page 403) | Average enactment rate | **26%**; >21,000 enacted; Colorado 74% high, New Jersey 0.5% low; Congress 1.1% | 2024 | https://fiscalnote.com/reports/2024-state-sessions-recap |
| Quorum, 2024 State Legislative Trends Report (PDF) | Bills enacted vs introduced, mid-2024 | 14,088 enacted of 76,756 introduced (147,660 incl. carryovers) → **18.4% / 9.5% (computed)**. Arkansas 98.37% (181/184), Colorado 73.91%, Utah 62%; Minnesota 0.37% (41/10,947), Illinois 0.50%, New York 0.96% | Through ~June 2024; 10 states still in session | https://www.quorum.us/wp-content/uploads/2024/08/2024-State-Legislative-Trends-Report-Digital-Edition.pdf |
| Quorum, "State legislatures vs Congress" | Decade average enactment rate | **States 25.84%; Congress ~5.5%**. Top states: CO 67.81%, GA 66.06%, DE 64.62%, UT 63.16%, AR 62.52% | "Last decade"; exact years and n not stated | https://quorum.us/data-driven-insights/state-legislatures-versus-congress-which-is-more-productive |
| Governing (CQ StateTrack data) | Enactment rate | "About a quarter"; Minnesota 5% to Maine 86% | 2013–14 | https://www.governing.com/archive/gov-state-labs.html (search snippet) |
| Eidelman, Kornilova & Argyle (FiscalNote), arXiv 1806.05284 | Floor action (passed origin chamber or got a floor vote) vs enactment | **41%** of bills get floor action (avg across states); "over 30%" enacted. Under 15% reach the floor in NJ and MA; 75% in CO and AR | ~1M bills, 50 states + DC, ~10 sessions per state (pre-2018) | https://arxiv.org/pdf/1806.05284 |
| Shor, *Describing the Data — Legislatures* (online book) | Passage by chamber control | Unified-party legislatures: "only about a quarter pass"; split legislatures: failure rate "near 90%" | ">50,000 bills"; years not stated in excerpt | https://bookdown.org/boris_shor214/Shor-Book/describing-the-data---legislatures.html |

### (b) Governors' legislative agenda success

| Source | Measure | Number | n / years | URL |
|---|---|---|---|---|
| Kousser & Phillips 2012, *The Power of American Governors*, Ch. 4 (author copy on Phillips's Columbia site) | Outcome of State of the State proposals | **41% passed (close to the ask), 18% compromise, 41% failed** → 59% "at least some of what they want" | 1,088 proposals, 28 states, 2001 and 2006 sessions | https://www.columbia.edu/~jhp2121/publications/ThePowerOfAmericanGovernors.pdf |
| Same | Mean governor "batting average" (compromise = 0.5) | **52%** (52.1% in Table 9.2). Range: ~90% (GA Barnes 2001, Perdue 2006) down to 16% (NY Pataki 2001), 21% (MA Romney 2006) | same | same |
| Same | Budget vs policy items | Pass or compromise: **budget 66%, policy 54%**. Compromise: budget 27%, policy 12%. Full pass about the same for both. **Implied full pass: policy ~42%, budget ~39% (computed)** | same | same |
| Same | By year | Pass or compromise: 55% (2001), 63% (2006); difference not significant | same | same |
| Same | By issue | Political reform (constitutional, fiscal, electoral rules): **27% pass + 6% compromise**. Every other category: majority at least partly successful | same | same |
| Same, regression (policy proposals) | Effect of the governor's party seat share | Predicted chance of a **full pass on a policy proposal: 16% with Romney's legislature (<14% copartisan seats) vs 38% with Wise's (79% copartisan)**. Mean copartisan seat share was 52%. Using a divided-government dummy instead "has no meaningful effect on our results." | same | same |
| Same, regression (budget items) | Session length | Full-pass chance on a budget item: 32% at mean session length; 38% for New Hampshire-length; 17% for New York-length | same | same |
| Same (case examples) | Divided-government cases | Keating (OK, lame duck, Democratic legislature) passed 22% of proposals. Lynch (NH, Democrat facing 65% Republican seats, first term, 69% approval) passed two-thirds | single cases | same |
| Rosenthal 1990 (via K&P p.110) | Self-reported success | 9 of 10 governors between **75–95%**. K&P say this is inflated (staff self-reports) | 10 governors, late 1980s | cited in K&P (above) |
| Fording, Woods & Prince 2002 (via K&P p.110) | Mean batting average | **73%**. Counts compromises as full passes and drops proposals with no information | 37 governors, 1999 | cited in K&P (above) |
| Ferguson 2003, SPPQ 3(2):158–182 | Determinants of success | Formal powers matter little; legislature type, party, personal factors and the economy matter; success "wanes over time." **No descriptive success rate reported** (K&P fn. 7: Ferguson does "not report descriptive statistics") | 50 governors, 1993–94 | https://www.cambridge.org/core/journals/state-politics-and-policy-quarterly/article/abs/chief-executive-success-in-the-legislative-arena/622A9C6F607CD2B2586B39AF8C0A2EC8 (abstract only) |
| Bernick & Wiggins 1991 | Gubernatorial legislative success | **Not found** (book chapter; no accessible numbers) | — | — |
| Governing, "Are governors' annual speeches all talk?" | Same-sex marriage 2013 | 3 of 3 governors who asked got it; 1 of 3 asking for a minimum-wage raise; 4 of 30 backing Medicaid expansion failed | 2013 anecdotes | https://governing.com/archive/gov-are-governors-annual-speeches-all-talk.html |

### (c) Bills that already passed one chamber, or have leadership or majority backing

| Source | Measure | Number | n / years | URL |
|---|---|---|---|---|
| Eidelman et al. 2018 (above) | Floor action 41% vs enacted >30% | Suggests **roughly 70–75% of bills that reach floor action / pass the origin chamber are enacted (computed, rough)**. The two figures use different averaging, so this is only a ballpark | ~1M bills | https://arxiv.org/pdf/1806.05284 |
| Craig 2023, SPPQ 23(4) "Governing Through Gridlock" | Bills that passed the origin chamber | 1,746 of 3,739 sampled bills passed their first chamber (46.7%, computed). Enactment rate among those: **not reported in text**. No link between divided government and enactment of district bills | 13 states, 1881–1997 | https://www.cambridge.org/core/journals/state-politics-and-policy-quarterly/article/governing-through-gridlock-bill-composition-under-divided-government/C5155AC64AC73C2385B0F02AC4B03366 |
| Bucchianeri, Volden & Wiseman, APSR 2025, state LES | Majority-party legislators | Majority-party members' effectiveness scores are **58% higher** than minority members', all else equal. Raw stage-by-stage pass rates are not in the article text (they are in the Dataverse data) | ~1.8M bills, 97 chambers, 1987–2018 | https://ideas.repec.org/a/cup/apsrev/v119y2025i1p21-39_3.html |
| Nevada Independent | Pass rate by sponsor party | Democratic (majority) sponsors 63% vs Republican 18% | NV 2021 session only | https://thenevadaindependent.com/article/analysis-which-legislators-had-the-most-and-fewest-bills-passed-in-the-2021-session |
| Gui, Ouyang & Chen 2025 (APSA preprint) | Reintroduction in US House | 27.8% of failed bills (17,084 of 61,557) are reintroduced next Congress. Enactment odds of reintroduced bills: **not reported** | 2003–2023 | https://doi.org/10.33774/apsa-2025-f67st-v2 |
| — | Enactment chance for a state bill that **passed one chamber in an earlier session** | **Not found** | — | — |
| — | Pass rate of leadership-priority bills (e.g., HB1/SB1) | **Not found** | — | — |

### (d) US Congress

| Source | Measure | Number | n / years | URL |
|---|---|---|---|---|
| Wiseman (Center for Effective Lawmaking) via FactCheck.org | Public bills enacted / introduced | **House 3.7%, Senate 4.1%** | 1973–2018 | https://www.factcheck.org/2019/04/a-misleading-claim-about-lawmakers-effectiveness |
| Brookings Vital Statistics on Congress, Tables 6-1, 6-2, 6-4 | Public bills enacted / bills + joint resolutions introduced (both chambers) | **115th 442/11,416 = 3.9%; 116th 344/14,342 = 2.4%; 117th 362/15,234 = 2.4% (computed)** | 1947–2022 | https://www.brookings.edu/wp-content/uploads/2024/11/Chpt-6.pdf |
| Gui, Ouyang & Chen 2025 | Enactment rate | 116th 2.36%; 117th 2.05% | — | (above) |
| FiscalNote via Governing | Federal enactment rate | 2% (2025) | 2025 | (above) |
| Rudalevige 2002 (via K&P Table 9.2) | Average success of presidential proposals | **45.4%** | Truman–Clinton | K&P PDF above |
| Edwards & Barrett 2000 (via K&P Table 9.2) | Share of presidential initiatives that became law | **41.2%** | Eisenhower–Clinton | K&P PDF above |
| Saiegh 2010 (via K&P Table 9.2), for comparison | Passage of executive initiatives in lower house | Latin American presidents 57.6%; European parliamentary PMs 79.6%; mixed systems 76.0% | 8 / 9 / 5 systems | K&P PDF above |
| Brookings Vital Stats Table 8-1 (CQ presidential success = share of roll calls where the president's stated position won) | **Unified government** years (1993–94, 2003–06, 2009–10, 2017–18, 2021–22) | **Mean 87.5%**, range 72.6–98.7 **(computed)** | 12 years | https://www.brookings.edu/wp-content/uploads/2024/11/8-1-Full.pdf |
| Same | **Divided government** years (1989–92, 1995–2000, 2002, 2007–08, 2011–16, 2019–20; 2001 left out because of the mid-year Senate switch) | **Mean 54.1%**, range 36.2–87.8; 52.4% without 2002 **(computed)** | 21 years | same |
| CQ Roll Call 2024 vote study | Biden House success | 100% (2021–22, Democratic House) → **18.5% (2023), 31.9% (2024: 23 of 72)**. Over the nine most recent opposite-party House years, Trump, Obama and Biden averaged **18.5%** in the House. Senate non-nomination votes: 48.1% (2023), 69.6% (2024: 16/23) | 2021–2024 | https://rollcall.com/2025/02/24/president-support-congress-vote-studies/ |

## 2. Numbers most usable for the probability table

1. **Base rate, generic state bill:** about **25–28%** of introduced bills become law (FiscalNote 28% in 2025, 26% in 2024; Quorum decade average 25.84%). The range across states runs from under 1% (MN, NJ, NY, IL) to over 70% (CO, AR). **Use the state's own rate, not the national mean.**
2. **State bill by party control (2025, single year, secondary citation):** Republican trifecta **36.4%**, Democratic trifecta **19.8%**, split **18.6%**. Shor's figures point the same way: unified about 25% pass, split about 10%.
3. **Governor's headline proposal enacted in the next session (Kousser & Phillips, n=1,088):** full pass **41%**; at least partial **59%**; batting average **52%**. Policy items: **54%** at least partial. Budget items: **66%**. Political reform items: **27%** full pass.
4. **Governor's proposal, same-party vs opposite-party legislature:** chance of a full pass on a **policy** proposal runs from **~16%** (governor's party holds about 14% of seats) to **~38%** (about 79% of seats). This comes from a regression on seat share, not a raw split. There is **no published raw unified-vs-divided success rate for governors**. A reasonable reading is "opposite party ≈ 15–20% full pass; strong same-party majority ≈ 35–40% full pass; add about 12 points for compromises."
5. **Bill that already passed one chamber:** no published rate for prior-session passage. The closest proxy: about 41% of state bills reach floor action against 30%+ enacted, which implies **~70%+ of bills that clear a chamber become law within the same session (rough, computed)**. **Congress / president:** about 2–4% of introduced bills are enacted. Presidential proposals become law about **41–45%** of the time. CQ success averages **87.5% under unified government vs 54.1% under divided**. In the House, it falls to **~18.5%** when the opposite party controls it.

## 3. Caveats

- **Definitions differ.** Vendors (FiscalNote, Quorum, Plural) count "introduced" in different ways: with or without resolutions, with or without carryover bills, and at different dates within the year. Quorum's 2024 rate is 18.4% or 9.5% depending on whether carryovers are counted. States with bill-filing limits (CO, AR, which also had a fiscal-only session in 2024) have high rates by construction.
- **The trifecta split** (36.4/19.8/18.6) comes from one year, reached me only through a think-tank write-up of a FiscalNote page I could not open (403), and is confounded by state rules: many Republican trifectas are low-volume, bill-capped states. Treat it as directional.
- **Kousser & Phillips** covers 2001 and 2006 only, 28 states, and only proposals named in State of the State speeches. Governors pre-screen their speeches toward items that can pass (selection effect). "Failure" includes proposals with no trace found. The 16% → 38% figures are model predictions for a *full pass on policy items*, holding other factors at typical values.
- **Older success rates (73%, 75–95%)** are inflated by self-reporting or by counting compromises as wins (according to K&P).
- **CQ presidential success** measures roll-call wins on votes where the president took a position, not enactment of the agenda. It counts watered-down wins and leaves out items that never reached a vote. My unified and divided means are simple averages of yearly combined scores. Columns in the Brookings PDF were partly garbled in extraction; I used only year values that reconcile with the table's own per-president averages.
- **Time horizon.** All rates are per session or per Congress. A two-year window covers 1–2 state sessions, or one Congress. Nothing found gives a cumulative multi-session rate.
- **Not found:** Bernick & Wiggins figures; any published enactment rate for bills that passed a chamber in a *previous* session; pass rates for leadership-priority bills; Ferguson 2003 descriptive rates (the paper reports none); Rudalevige and Edwards & Barrett splits by divided government. Ferguson 2003 and Dilger, Krause & Moffett 1995 were read only as abstracts or citations (paywalled). The Kousser & Phillips book was read from the authors' own posted copy.
