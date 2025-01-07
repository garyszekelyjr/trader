import pprint

import pandas as pd

import formulas


history = pd.read_csv("history.csv", header=[0, 1], low_memory=False)

if isinstance(history.columns, pd.MultiIndex):
    fields = history.columns.levels[0]
    tickers = history.columns.levels[1]

    rows = {}
    for ticker in tickers:
        try:
            rsi = formulas.rsi(history["Close", ticker])

            if rsi == 100:
                continue

            rows[ticker] = rsi
        except Exception:
            pass

    pprint.pprint(rows["AAPL"])
