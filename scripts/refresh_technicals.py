#!/usr/bin/env python3
"""NOVASTRA technicals refresh — RSI(14) for the full universe in ONE process.

Reads the fixed ticker list from data/universe.json, batches 40 tickers per
finance_ohlcv_histories call via the `external-tool` CLI, computes Wilder RSI(14)
from 6-month daily closes, and writes data/technicals.json.

Run from the repo root:  python3 scripts/refresh_technicals.py
Requires api_credentials ["external-tools"]. Do NOT iterate per-ticker tool calls.
"""
import json, subprocess, urllib.request, datetime, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNIVERSE = os.path.join(ROOT, "data", "universe.json")
OUT = os.path.join(ROOT, "data", "technicals.json")
START = (datetime.date.today() - datetime.timedelta(days=200)).isoformat()
END = datetime.date.today().isoformat()


def rsi(closes, period=14):
    if len(closes) < period + 1:
        return None
    ag = al = 0.0
    for i in range(1, period + 1):
        d = closes[i] - closes[i - 1]
        if d >= 0: ag += d
        else: al -= d
    ag /= period; al /= period
    for i in range(period + 1, len(closes)):
        d = closes[i] - closes[i - 1]
        ag = (ag * (period - 1) + max(d, 0)) / period
        al = (al * (period - 1) + max(-d, 0)) / period
    if al == 0:
        return 100.0
    return round(100 - 100 / (1 + ag / al), 1)


tickers = json.load(open(UNIVERSE))["tickers"]
print(f"{len(tickers)} tickers", flush=True)
out, B = {}, 40
nb = (len(tickers) + B - 1) // B
for i in range(0, len(tickers), B):
    batch = tickers[i:i + B]
    args = {"source_id": "finance", "tool_name": "finance_ohlcv_histories", "arguments": {
        "ticker_symbols": batch, "query": "daily close",
        "start_date_yyyy_mm_dd": START, "end_date_yyyy_mm_dd": END,
        "time_interval": "1day", "fields": ["close"]}}
    try:
        p = subprocess.run(["external-tool", "call", json.dumps(args)], capture_output=True, text=True, timeout=240)
        resp = json.loads(p.stdout)
    except Exception as e:
        print(f"batch {i//B+1} call FAIL {e}", flush=True); continue
    for cf in resp.get("csv_files", []):
        url, name = cf.get("url"), cf.get("filename", "")
        tk = name.split("_price_history")[0] if "_price_history" in name else None
        if not url or not tk:
            continue
        try:
            txt = urllib.request.urlopen(url, timeout=40).read().decode("utf-8", "ignore")
            lines = [l for l in txt.splitlines() if l.strip()]
            hdr = lines[0].split(","); ci = next((j for j, h in enumerate(hdr) if h.strip().lower() == "close"), None)
            if ci is None:
                continue
            closes = []
            for l in lines[1:]:
                parts = l.split(",")
                if len(parts) > ci:
                    v = parts[ci].replace('"', '').replace(",", "").strip()
                    try: closes.append(float(v))
                    except: pass
            r = rsi(closes)
            if r is not None:
                out[tk] = {"rsi": r, "asOf": END, "source": "Perplexity finance_ohlcv_histories (daily close)"}
        except Exception:
            continue
    print(f"batch {i//B+1}/{nb}: total {len(out)}", flush=True)

doc = {"refreshedAt": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
       "source": "Perplexity finance DB", "period": 14, "rsi": out}
json.dump(doc, open(OUT, "w"), ensure_ascii=False, indent=1)
print(f"WROTE {OUT} with {len(out)} RSI cross-checks", flush=True)
