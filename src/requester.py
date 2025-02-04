from typing import List

import requests

from .authenticator import Authenticator


URLS = {
    "marketdata": "https://api.schwabapi.com/marketdata/v1",
}


class Requester:
    authenticator = Authenticator()

    def __init__(self):
        self.access_token = self.authenticator.login()

    def __request__(self, url: str) -> requests.Response:
        return requests.get(
            url, headers={"Authorization": f"Bearer {self.access_token}"}
        )

    def quotes(self, symbols: List[str]) -> requests.Response:
        return self.__request__(
            f"{URLS['marketdata']}/quotes?symbols={','.join(symbols)}"
        )
