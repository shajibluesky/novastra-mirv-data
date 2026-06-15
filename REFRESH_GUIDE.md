# NOVASTRA twice-daily data refresh — runbook

Goal: regenerate `data/macro.json`, `data/news.json`, `data/catalysts.json`, `data/flows.json`
with the FRESHEST authentic Indian-market data + AI interpretation, then push to this repo
(branch `main`). The live terminal reads these within ~5 minutes — no republish needed.

See `REFRESH_SCHEMA.md` for the macro/news/catalysts schema. Follow key names exactly.

## Hard rules (non-negotiable)
- Every number MUST come from a real, citable source with a working `sourceUrl` + `asOf` date.
- If a value can't be sourced, set it `null` + `freshness:"DNA"`. NEVER invent or carry forward.
- `bias`/`rationale`/`interpretation`/`marketState` are interpretation of sourced facts only.
- Set `refreshedAt` to the current UTC time (ISO 8601) in EVERY file.

## Files to refresh
1. **data/macro.json** — ~14 indicators (RBI repo, CPI, WPI, GDP actual+forecast, IIP, FII/DII
   flows, USD/INR, Brent, India 10Y G-sec, fiscal deficit, GST, monsoon). PLUS a top-level
   `marketState` object: { state: "Bullish"|"Bearish"|"Transition", tilt, confidence, asOf,
   headline, boosting:[{factor,detail}], lagging:[{factor,detail}], narration, method }.
   Derive marketState by weighing the sourced indicators + flows + index trend. Interpretation only.
2. **data/news.json** — 20-30 real published items (last ~7 days), each impact-tagged (bias, scope,
   sector, tickers[], rationale).
3. **data/catalysts.json** — market[], sectors[], stocks[] (pump/dump/watch), all sourced.
4. **data/flows.json** — APPEND today's NSE/NSDL provisional FII & DII net cash figures to the
   existing `series` (do NOT rebuild history; keep prior days). Schema:
   { refreshedAt, unit, source, sourceUrl, notes, series:[{date,fii,dii,source,sourceUrl}] }.
   Sort ascending by date. Skip weekends/holidays. Authentic source: NSE FII/DII report or
   Moneycontrol FII-DII activity (NSE+BSE+MSEI combined provisional). Omit any day you can't verify.

## Procedure
1. `git clone https://github.com/shajibluesky/novastra-mirv-data.git` (github credentials), cd in.
2. Gather data: finance connector for India quotes; web search for macro prints, news, catalysts,
   and the latest FII/DII day. Prefer ET, Business Standard, Moneycontrol, LiveMint, Reuters India,
   PIB, RBI, MoSPI, NSE.
3. Update the four files in `data/` (append to flows.json; regenerate the other three). Recompute marketState.
4. Validate each parses: `python3 -m json.tool data/<file>.json`. Fix until all pass.
5. Commit + push:
   `git -c user.email=bot@novastra.local -c user.name="NOVASTRA data bot" commit -am "Refresh <UTC datetime>"`
   `git push origin main`
6. Notify only if the Market State flips or a major new buy/avoid catalyst appears. Else end silently.

## data/technicals.json (RSI cross-check)
Recompute RSI(14) for the whole universe from the finance connector OHLCV (6-month daily closes)
and write `{ refreshedAt, source, period:14, rsi: { "TICKER.NS": {rsi, asOf, source} } }`.
This is the SECOND source the live app compares its Yahoo RSI against. Only sourced closes; if a
ticker lacks enough history, omit it (the app shows single-source rather than a fabricated value).
