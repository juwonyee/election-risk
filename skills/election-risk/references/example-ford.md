# Worked example: Ford (F), one direct link and two race links

Full files (structure.md, markets.json, summary.md, report.html, card.svg):
[`examples/F/`](https://github.com/juwonyee/election-risk/tree/main/examples/F) on GitHub.

1. **Exposure** (`$profit-structure`, written before opening any market list). Base: FY2025 adjusted EBIT
   $6.78B (GAAP operating income was negative because of special items; say which you use). Movable lines,
   biggest first: tariffs on imported vehicles and parts (net ~$2B in 2025, `tariffs-trade`, federal), USMCA
   rules for the Mexico and Canada plants (`tariffs-trade`, federal), emissions-credit purchases (~$700M,
   `clean-cars-ev`, federal + California). Locked in: CAFE penalty set to $0, EV credits repealed, UAW
   contract to 2028.
2. **Markets.** `erisk markets pull`, then read `elections.md` and `policy.md`. `policy.md` has
   `kalshi:KXUSMCA-26` (US gives notice to leave USMCA, by date). `elections.md` has House control
   (`CONTROLH-2026`) and the California governor race (`KXGOVCA-26`).
3. **Book rows.** `erisk book find --tag tariffs-trade` returns the House-control rows: Democrats pledge a law
   overturning the tariffs (`federal: partisan`, 0.05); Republicans keep repeal off the floor
   (`block: majority`, 0). `erisk book find --tag clean-cars-ev --state CA`: Becerra is "open to revising"
   the 2035 gas-car rule (`vague`, 0.05); Hilton has no row (0).
4. **Links.**
   - Direct: USMCA notice before 2027 (the rung matching the impact's timing). Impact: ~352k Mexican-built
     vehicles a year × ~$25k × the 25% Section 232 rate on the half not yet tariffed, plus parts: −$2.0B
     (range −$1.1B to −$3.5B), `estimated`, every input sourced.
   - Race: House control → tariff repeal, +$1.0B if it happens, p 0.05 / 0.
   - Race: California governor → gas-car rule relaxed, +$100M, p 0.05 / 0.
5. **Run.** `erisk validate`, `erisk snapshot`, `erisk compute` for `F`.
6. **Result.** Election risk LOW, policy risk HIGH. Policy: "Kalshi puts 8% on: the US gives notice to leave
   USMCA before 2027. For Ford: −$2.00B a year (−29.5% of profit)." Election: nothing passes the bar; the
   biggest is +$1.00B if Congress repeals the tariffs, but only 5% even if Democrats win. Who wins Nov 3 barely
   changes Ford's odds. That is a finding, not a failure.
7. **Red Team.** The USMCA impact is an estimate built on an import-value assumption, and a notice can be a
   negotiating move later withdrawn (Kalshi's other USMCA market prices the same notice at 17%, thin).
