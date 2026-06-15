# NOVASTRA CAPITAL MIRV — Public Data Channel

Public market-information JSON consumed by the NOVASTRA CAPITAL MIRV — Indian Equity Terminal.

- `data/macro.json` — India macro indicators (RBI repo, CPI, WPI, GDP, IIP, FII/DII flows, USD/INR, Brent, 10Y G-sec, fiscal deficit, GST, monsoon)
- `data/news.json` — sourced, impact-tagged market/sector/stock news
- `data/catalysts.json` — market → sector → stock catalysts (pump/dump/watch)

Every field carries `source`, `sourceUrl`, `asOf`, and a `freshness`/`bias` tag. Refreshed twice daily.
**Public market data only** — no proprietary scoring, models, or app code. Research base case, not investment advice.
