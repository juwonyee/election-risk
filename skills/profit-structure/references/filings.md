# Company filings: base numbers and exposure

Read this at step 1. Find the sources yourself; public pages only, no paywalled databases or transcripts.
Every number: amount, unit, period, `verified` (read from a filing or official page) or `estimated` (derived,
with the arithmetic in a note), and a URL.

## Contents
- Steps
- Where to find annual numbers, by listing country
- Where exposure splits usually are
- When a source can't be reached

## Steps

1. **Denominator.** Latest full fiscal year operating income. Use adjusted EBITDA or pre-tax income when
   operating income is near zero or not reported, and say which.
   - US and SEC-registered foreign filers (10-K, 20-F, 40-F): `erisk filings edgar <TICKER>`.
     Extra XBRL tags: `--tags FuelCosts`.
   - Everyone else: the annual report in the home filing system or on the company's IR page (table below).
2. **Currency.** Keep the reported amount and currency. Convert to US dollars at one stated rate (date and
   source: Federal Reserve H.10, ECB reference rates, or the home central bank), recorded in `denominator.fx`.
3. **Exposure splits.** Look for what each channel needs (table below).
4. **Mark gaps.** If a split isn't disclosed, say "not disclosed" and, if you estimate it, show the arithmetic
   and mark it `estimated`.

## Where to find annual numbers, by listing country

A starting point, not a limit. Prefer the official filing; cite the exact document.

| Listed in | Official source | Notes |
|---|---|---|
| United States | SEC EDGAR: 10-K, 10-Q, 8-K | `erisk filings edgar <TICKER>` for headline numbers |
| Foreign, also SEC-registered | SEC EDGAR: 20-F, 40-F, 6-K | Many large non-US companies (TSMC, Toyota, Sony, Novo Nordisk...). Often IFRS, home currency. The same command works |
| South Korea | DART (dart.fss.or.kr) | Business report (사업보고서) |
| Japan | EDINET (disclosure2.edinet-fsa.go.jp); TDnet for earnings | Annual securities report (有価証券報告書) |
| European Union | ESEF annual reports (filings.xbrl.org), national registers | |
| United Kingdom | FCA National Storage Mechanism, Companies House | |
| Canada | SEDAR+ (sedarplus.ca) | |
| Taiwan | MOPS (mops.twse.com.tw) | |
| Hong Kong, mainland China | HKEXnews, CNINFO | |
| India | BSE and NSE filings | |
| Australia | ASX announcements | |
| Anywhere | Investor-relations page: annual report, earnings release, investor-day slides | When no filing system has it |

## Where exposure splits usually are

| Split | Look in |
|---|---|
| Segment revenue and operating profit | Segment note in the annual report (US: ASC 280 note in the 10-K) |
| Stores, plants, offices by state or country | "Properties" section (10-K Item 2), store-count tables, company location pages |
| Employees by state | Company location or "facts by state" pages (often rendered by JavaScript: open them in a browser), state economic-development releases, union filings |
| Sales by country | Geographic revenue note; US share for non-US companies |
| Imports by country | 10-K risk factors and supply-chain sections, earnings-call remarks on the company's IR site, US customs-based trade data only for products, not firms |
| Regulated utility base | Rate-case filings at the state commission, the subsidiary's own 10-K (equity, rate base, allowed ROE) |
| Tax credits | Income-tax note (credits used, deferred tax assets), "government incentives" sections |
| Wage mix | Company pay announcements, BLS occupational wages by state as a cross-check (mark derived numbers `estimated`) |

## When a source can't be reached

- SEC asks every request to carry a contact email. Before the first SEC call, if `EDGAR_USER_AGENT` is not
  set, let the user choose once: their real email (suggest the one you know, if any) or the placeholder
  `you@example.com`. For a real email, set `EDGAR_USER_AGENT="election-risk <email>"` for this run only; never
  write it into a file. If the user doesn't answer or you can't ask, the engine uses the placeholder.
- If SEC still returns 403, read the numbers from the company's IR annual report instead, and tell the user
  at the end that a real email would let SEC data be added.
- DART and EDINET APIs need free keys; their websites don't. Use the website if no key is set, and mention the
  key would speed it up.
