# NOVASTRA data-channel schema (macro.json / news.json / catalysts.json)

These three files are the **baked, scheduled-refresh layer**. The Express backend reads them
(remote GitHub raw first, local bundle fallback) and MERGES live keyless feeds at request time.

GOLDEN RULES (non-negotiable):
- Every numeric/factual field MUST carry a real `source` name + `sourceUrl` + `asOf` date.
- If a value cannot be found from an authentic source, set the value to `null` and `freshness:"DNA"`.
  NEVER invent, estimate, or carry forward a number without saying so.
- `bias` is interpretation, allowed values: "bullish" | "bearish" | "neutral".
- `interpretation`/`rationale` is analyst narration — it may explain, but must not assert numbers
  that aren't in a sourced field.
- ISO dates (YYYY-MM-DD) for `asOf`; ISO timestamp for `refreshedAt`.

## macro.json
```json
{
  "refreshedAt": "2026-06-15T12:00:00Z",
  "asOf": "2026-06-15",
  "indicators": [
    {
      "id": "repo_rate",
      "label": "RBI Repo Rate",
      "category": "Monetary policy",          // Monetary policy | Inflation | Growth | External | Flows | Fiscal | Liquidity
      "value": "5.25%",                         // string with unit, or null
      "prev": "5.50%",                          // previous print, or null
      "asOf": "2026-06-06",
      "source": "Reserve Bank of India — MPC statement",
      "sourceUrl": "https://www.rbi.org.in/...",
      "bias": "bullish",                        // impact on equities broadly
      "scope": "market",                        // market | sector
      "affects": ["NBFC", "Realty", "Auto"],   // sectors most sensitive
      "interpretation": "A pause after cuts keeps rate-sensitives supported; further cuts would re-rate NBFCs/realty.",
      "freshness": "SNAPSHOT"                   // SNAPSHOT (baked) | DNA
    }
  ]
}
```
Required indicators to attempt (mark DNA if not found): RBI repo rate, CPI inflation (latest YoY),
WPI inflation, FY GDP growth (latest + estimate), IIP, FII net flows (YTD or latest), DII net flows,
USD/INR (note: also live), Brent (also live), India 10Y G-sec yield, fiscal deficit % of GDP / target,
monsoon/IMD outlook (qualitative), GST collections (latest month).

## news.json
```json
{
  "refreshedAt": "2026-06-15T12:00:00Z",
  "items": [
    {
      "title": "….",
      "source": "Economic Times",
      "sourceUrl": "https://...",
      "publishedAt": "2026-06-15",
      "summary": "1-2 line factual summary",
      "scope": "stock",                         // market | sector | stock
      "sector": "IT Services",                  // or null
      "tickers": ["LTIM", "INFY"],             // NSE symbols without .NS, or []
      "bias": "bearish",
      "rationale": "Why this could move the name(s).",
      "freshness": "SNAPSHOT"
    }
  ]
}
```
Aim for 18-30 items: a mix of market-wide, sector, and single-stock catalysts from the last ~7 days.
Only real, published articles with working source URLs. No paraphrased rumors.

## catalysts.json
```json
{
  "refreshedAt": "2026-06-15T12:00:00Z",
  "market": [
    { "title": "...", "detail": "...", "bias": "bullish", "source": "...", "sourceUrl": "...", "asOf": "2026-06-15" }
  ],
  "sectors": [
    { "sector": "Defence", "bias": "bullish",
      "catalysts": [ { "title": "...", "detail": "...", "source": "...", "sourceUrl": "...", "asOf": "..." } ] }
  ],
  "stocks": [
    { "ticker": "LTIM", "company": "LTIMindtree", "signal": "pump",   // pump | dump | watch
      "catalyst": "...", "detail": "...", "source": "...", "sourceUrl": "...", "asOf": "..." }
  ]
}
```
