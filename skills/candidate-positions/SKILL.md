---
name: candidate-positions
description: Builds a sourced policy book of what each Nov 3, 2026 US election winner would do that can move company profits (governors, attorneys general, utility commissions, legislatures, ballot measures, House and Senate control), with the chance each policy follows from a research-based probability table. Use when the user asks what a candidate or party would do on an issue, which races matter for an industry, or before an election-risk analysis that needs candidate positions.
license: MIT
metadata:
  author: juwonyee
  version: "2.0.0"
---

# Candidate positions (the policy book)

For each Nov 3 contest that has a prediction market, the book records what the two leading candidates would
do on business issues, how they would get it done, the chance it happens if they win, and a source.
The book is built on the user's own machine and reused for every company. It is never shipped in the repo.

`erisk` below means `python3 <skill-dir>/scripts/erisk.py` (`${CLAUDE_SKILL_DIR}` in Claude Code). Run it from
the user's working directory; the book goes to `./election-risk-out/_book/`. Python 3.10+, standard library.

## Rules

- **Every position needs a public URL. No URL, p = 0.** Never infer a position from party.
- **p comes from [references/probability-table.md](references/probability-table.md).** Your judgment picks
  the route; the table gives the number. Never tune a cell for one case.
- Same method for every party and candidate. No editorializing.
- Never say buy, sell or hedge. Never get around a geo-block or paywall; note what is missing.

## Workflow

```
- [ ] 1. Market list: erisk markets pull   (or use $prediction-markets)
- [ ] 2. erisk book status  -> what is covered, what is left (biggest markets first)
- [ ] 3. Research contests, one file each   (references/book-format.md)
- [ ] 4. erisk book status again; repeat 3 until done or the user stops
```

**2. Status.** `erisk book status` lists every contest in `_markets/elections.md` and marks which are covered
by a book file. Single US Senate seats and House districts are left out: their policy effect runs through
chamber control (`US-senate-control.md`, `US-house-control.md`), and in testing no single seat moved a large
company. The list is keyword-filtered, so skip any line that is not a contest a winner governs from.

**3. Research.** For each contest on the to-do list, write `election-risk-out/_book/<ST>-<office>.md` in the
format of [references/book-format.md](references/book-format.md): office powers, legislature after Nov 3 if
each candidate wins, then each candidate's business-relevant positions with tag, route, p and source.
- If your agent can run subagents in parallel, split the to-do list into chunks of about 10 contests and give
  each subagent one chunk and this skill. Otherwise go one contest at a time.
- The book can be built over several sessions: `status` always shows what is left.
- A full book is large (about 200 contests). If the user only needs some contests now, do those first.

**If the user asks to answer about one contest only** ("what would the next Arizona AG do on data
centers?"), research that one contest into the book and answer from the file.

## Using a downloaded book

`erisk book download --accept-risk` fetches the book the maintainers built, from the repository's release.
Only run it when the user has said yes after you told them, in your own words: it was built by someone else on
the date shown, it may be wrong or out of date, and they should check the sources of any row they rely on.
A downloaded book has the same format; re-research any contest to overwrite it. `erisk book info` shows where
the current book came from, its date and fingerprint; reports print the same line.

## Answer format (when asked about candidates directly)

Per contest: one line on who leads in the market, then a small table per candidate (issue, position, how,
chance if they win, source). End with: *Positions from public sources as of <date>. Chances are upper bounds
from historical rates, not forecasts.*
