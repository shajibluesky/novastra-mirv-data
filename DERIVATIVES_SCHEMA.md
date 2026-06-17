# derivatives.json — schema (NIFTY & Sensex F&O + Options positioning)

End-of-day index derivatives snapshot. Refreshed once daily post-close by the agent.
Authenticity is non-negotiable: every numeric field carries a real source + sourceUrl + asOf
+ freshness. If a value cannot be sourced -> value: null, freshness: "DNA". NEVER invent.
`bias`, `note`, and all `*Verdict` objects are INTERPRETATION of the sourced facts only.

## Top level
```json
{
  "refreshedAt": "<current UTC ISO, e.g. 2026-06-16T14:00:00Z>",
  "asOf": "<trading day, e.g. 2026-06-16>",
  "expiry": "<current weekly/monthly expiry the data refers to, e.g. 2026-06-25>",
  "indices": { "NIFTY": <IndexBlock>, "SENSEX": <IndexBlock> }
}
```

## Metric object (used for every numeric field)
```json
{ "value": <number|string|null>, "unit": "<e.g. points, %, contracts, ratio>",
  "change": <number|null>, "source": "<name>", "sourceUrl": "<working url>",
  "asOf": "<date>", "freshness": "LIVE|SNAPSHOT|DNA",
  "bias": "Bullish|Bearish|Neutral", "note": "<1-line plain-English interpretation>" }
```

## IndexBlock (NIFTY full; SENSEX same shape, DNA where data unavailable)
```json
{
  "spot":            <Metric>,                         // index close
  "futuresBasis":    <Metric>,                          // futures - spot (premium=bullish / discount=bearish)
  "futuresOi":       <Metric>,                          // total futures OI; change = day % ; note = buildup type
  "buildup":         "Long buildup|Short buildup|Short covering|Long unwinding|Neutral",
  "fiiIndexFutures": <Metric>,                          // value = net long contracts (+long/-short); note = long/short split + ratio
  "pcr":             <Metric>,                          // OI-based Put-Call Ratio
  "maxPain":         <Metric>,                          // max pain strike
  "support":         <Metric>,                          // highest Put OI strike
  "resistance":      <Metric>,                          // highest Call OI strike
  "indiaVix":        <Metric>,                          // only on NIFTY block (market-wide); SENSEX may reuse/null

  "fnoVerdict":      { "verdict": "Bullish|Bearish|Neutral", "confidence": "High|Medium|Low",
                       "rationale": "<2-3 lines weighing FII futures + OI buildup + basis>" },
  "optionsVerdict":  { "verdict": "...", "confidence": "...",
                       "rationale": "<2-3 lines weighing PCR + VIX + OI strikes + max pain>" },
  "combinedVerdict": { "verdict": "...", "confidence": "...",
                       "rationale": "<overall positioning read for this index>" }
}
```

## Approved F&O sources (extends SOURCES.md)
nseindia.com (official participant-wise OI & FII derivatives stats), moneycontrol.com,
groww.in, trendlyne.com, 5paisa.com, upstox.com, economictimes.indiatimes.com.
India VIX: nseindia.com or Yahoo (^INDIAVIX). Prefer NSE official for FII stats.

## Notes
- NIFTY is the primary, most-liquid index derivative — populate fully.
- SENSEX/BSE F&O is thinner; populate what is authentically available, else DNA. Do not fabricate.
- If NSE blocks direct fetch, use Moneycontrol/Groww/Trendlyne snapshot but keep canonical URL.

## Cron-compatible sourcing (IMPORTANT — background runs CANNOT render JavaScript)
Live option-chain pages (StockMojo, Sensibull, NiftyTrader live) are JavaScript-rendered and
CANNOT be read by the background daily refresh (no browser). To fill Max Pain / Support / Resistance
for BOTH NIFTY and SENSEX without a browser, parse the **daily static F&O-cues / trade-setup articles**
(plain HTML, published every trading morning/evening) which state the numbers in text:
- Upstox "Trade setup" / "Expiry alert" articles (upstox.com/news/...) — state "Max call OI: X", "Max put OI: Y", "Max pain: Z" for NIFTY and SENSEX.
- Moneycontrol "Trade setup: Top 15 things to know" and ET Markets "Top F&O cues" — same fields in text.
Use the highest Call OI strike as resistance and highest Put OI strike as support; record the article URL + date.
- **India VIX is market-wide** (one NSE value): apply the same India VIX to BOTH the NIFTY and SENSEX blocks (note it is market-wide), do not mark SENSEX VIX as DNA.
- **SENSEX fiiIndexFutures is genuinely unavailable**: NSE publishes FII derivative statistics index-agnostically (not split for SENSEX), so this field is legitimately DNA — never fabricate it.
- Totals (Total Call OI / Total Put OI / PCR) for SENSEX are available statically from upstox.com/fno-discovery/open-interest-analysis/sensex-oi/.
- Only when a number is in NONE of these static sources, set it null + freshness "DNA".
