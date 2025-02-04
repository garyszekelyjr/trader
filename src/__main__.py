from pprint import pprint

from sqlalchemy.orm import Session

from . import models, ENGINE
from .requester import Requester


requester = Requester()

with Session(ENGINE) as session:
    ticker = session.query(models.Ticker).first()

    if ticker:
        response = requester.quotes([ticker.ticker])

        pprint(response.json())
