import yfinance as yf

import tickers


HISTORY = "history.csv"


def download(period: str = "1mo", interval: str = "1d") -> None:
    df = yf.download(
        [symbol for symbol, _ in tickers.TICKERS[:500]],
        period=period,
        interval=interval,
    )

    if df is None:
        return

    df.to_csv(HISTORY)
