from typing import List

import requests
import yfinance as yf


def tickers() -> List[List[str]]:
    """
    FIELDS

    ticker
    cik
    """

    URL = "https://www.sec.gov/include/ticker.txt"
    HEADERS = {"User-Agent": "Gary Szekely gary.szekely.jr@gmail.com"}

    response = requests.get(URL, headers=HEADERS)

    return [line.split("\t") for line in response.text.split("\n")]


def history(period: str = "1mo", interval: str = "1d") -> None:
    TICKERS = tickers()

    df = yf.download(
        [symbol for symbol, _ in TICKERS[:500]],
        period=period,
        interval=interval,
    )

    if df is None:
        return

    df.to_csv("history.csv")
