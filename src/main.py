import math

import pandas as pd

import formulas


history = pd.read_csv("history.csv", header=[0, 1], low_memory=False)

stocks = {}
if isinstance(history.columns, pd.MultiIndex):
    fields = history.columns.levels[0]
    tickers = history.columns.levels[1]
    for ticker in tickers:
        try:
            closes = history["Close", ticker]
            if isinstance(closes, pd.Series):
                ma = formulas.ma(closes)
                rsi = formulas.rsi(closes)

                if math.isnan(ma) or math.isnan(rsi):
                    continue

                stocks[ticker] = {"ma": ma, "rsi": rsi}
        except Exception:
            pass

df = pd.DataFrame(stocks).T

print(df.sort_values("rsi", ascending=False).head())
print(df.sort_values("rsi", ascending=False).tail())
