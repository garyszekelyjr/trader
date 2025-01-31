import os

import tqdm
import requests

from dotenv import load_dotenv
from sqlalchemy.orm import Session

from .. import models, ENGINE


load_dotenv()

NAME = os.getenv("NAME")
EMAIL = os.getenv("EMAIL")

with Session(ENGINE) as session:
    session.query(models.Ticker).delete()

    response = requests.get(
        "https://www.sec.gov/files/company_tickers.json",
        headers={"User-Agent": f"{NAME} {EMAIL}"},
    )

    tickers = response.json().values()

    tickers = [models.Ticker(**ticker) for ticker in tqdm.tqdm(tickers)]

    session.add_all(tickers)
    session.commit()
