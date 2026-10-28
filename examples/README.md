# Examples

Each folder is what the skills write to `election-risk-out/<TICKER>/`, from end-to-end runs on 2026-10-27
with the policy book built that day:

- `structure.md`: the profit structure (`$profit-structure`)
- `markets.json`: the links the agent chose, with every number's source
- `summary.md`, `report.html`, `card.svg`, `results/all.json`: what the engine computed, with the prices it used
  and when they were fetched

The raw price snapshots are not included (venue terms), so recomputing fetches today's prices:

```bash
mkdir -p election-risk-out && cp -r examples/F election-risk-out/
python3 engine/erisk.py snapshot --company F
python3 engine/erisk.py compute --company F
```

`SO` (Southern Company) is the small fixture the tests use. Its prices are synthetic, not market data, and it
predates the policy book.
