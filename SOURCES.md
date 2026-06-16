# NOVASTRA — Approved Data Sources & Refresh Rules

Authoritative source allowlist for the twice-daily refresh. Use ONLY these domains for
macro indicators, news items, catalysts, and FII/DII flows. This keeps the feed authentic
and repeatable, and avoids weak/low-quality sources.

## Approved news / data domains (in priority order)

**Tier 1 — primary / official (prefer for macro & flows):**
- rbi.org.in (RBI — repo rate, monetary policy)
- mospi.gov.in (MoSPI — CPI, IIP, GDP)
- pib.gov.in (Press Information Bureau — official releases)
- nseindia.com (NSE — FII/DII provisional cash, index data)
- nsdl.co.in / cdslindia.com (FPI flows)
- eaindustry.nic.in (WPI — Office of Economic Adviser)
- dea.gov.in / cga.nic.in (fiscal deficit, GST)
- mausam.imd.gov.in (IMD — monsoon)

**Tier 2 — established financial press (prefer for news & catalysts):**
- economictimes.indiatimes.com
- business-standard.com
- moneycontrol.com
- livemint.com
- financialexpress.com
- thehindubusinessline.com
- reuters.com (India coverage)

**Notes on access:** Reuters / ET may occasionally block direct fetch. If a fetch is
blocked, use the headline + summary from the search result snippet and still record the
canonical article URL as sourceUrl — never fabricate the body or numbers.

## Item-count rules (news.json)
- Target 20–30 real published items from the last ~7 days.
- If fewer than 20 authentic items are found, publish only what is real and note the
  shortfall in the file's `note` field. NEVER pad with weak sources or invented items.
- Each item MUST have: title, source, sourceUrl (working), publishedAt, summary, scope,
  sector, tickers[], bias, rationale, freshness.

## Non-negotiable authenticity
- Every numeric/factual field carries a real source + working sourceUrl + asOf date.
- If a value cannot be sourced: value = null and freshness = "DNA". Never invent.
- bias / rationale / marketState / narration are interpretation of sourced facts ONLY.
- Set `refreshedAt` to current UTC ISO in every file.

## Technicals (RSI) — use the batch script, not per-ticker tool calls
- Ticker universe is fixed in `data/universe.json` (584 tickers).
- Run `python3 scripts/refresh_technicals.py` (api_credentials ["external-tools"]).
  It batches 40 tickers per `finance_ohlcv_histories` call in ONE process and writes
  `data/technicals.json`. Do NOT iterate finance_ohlcv_histories via individual tool calls.
