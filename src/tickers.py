import requests

"""
FIELDS

ticker
cik
"""

URL = "https://www.sec.gov/include/ticker.txt"
HEADERS = {"User-Agent": "Gary Szekely gary.szekely.jr@gmail.com"}

response = requests.get(URL, headers=HEADERS)

TICKERS = [line.split("\t") for line in response.text.split("\n")]
