# NOVASTRA twice-daily data refresh — runbook

Goal: regenerate `data/macro.json`, `data/news.json`, `data/catalysts.json` with the FRESHEST
authentic Indian-market data + AI interpretation, then push to this repo (branch `main`).
The live terminal reads these files within ~5 minutes — no republish needed.

See `REFRESH_SCHEMA.md` for the EXACT field schema. Follow it precisely (key names matter).

## Hard rules (non-negotiable)
- Every number MUST come from a real, citable source with a working `sourceUrl` + `asOf` date.
- If a value can't be found from an authentic source, set it to `null` and `freshness:"DNA"`.
  NEVER invent, estimate, or carry a number forward without saying so.
- `bias` (bullish/bearish/neutral) and `rationale`/`interpretation` are YOUR interpretation of
  sourced facts — they may explain, but must not assert numbers absent from a sourced field.
- Set `refreshedAt` to the current UTC time (ISO 8601) in every file so the live app treats it as fresh.

## Procedure
1. `git clone https://github.com/shajibluesky/novastra-mirv-data.git` (use github credentials), cd in.
2. Gather data:
   - Use the `finance` connector for live India quotes/indices where helpful.
   - Use web search for macro prints (RBI repo, CPI, WPI, GDP, IIP, FII/DII flows, USD/INR, Brent,
     India 10Y G-sec, fiscal deficit, GST collections, IMD monsoon) and the last ~7 days of
     market/sector/stock news + catalysts. Prefer ET, Business Standard, Moneycontrol, LiveMint,
     Reuters India, PIB, RBI, MoSPI.
3. Write the three files into `data/` matching REFRESH_SCHEMA.md (macro: ~14 indicators;
   news: 20-30 items mixing market/sector/stock; catalysts: market[], sectors[], stocks[]).
4. Validate: `python3 -m json.tool data/macro.json`, same for news/catalysts. Fix until all parse.
5. Commit + push:
   `git -c user.email=bot@novastra.local -c user.name="NOVASTRA data bot" commit -am "Refresh <UTC date-time>"`
   `git push origin main`
6. Notify only if something materially changed (new buy/avoid catalyst, rating-relevant macro shift).
