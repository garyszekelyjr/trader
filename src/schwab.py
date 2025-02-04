import base64
import json

from datetime import datetime

import jwt
import requests

from . import CLIENT_ID, REDIRECT_URI, SECRET, TOKENS


def authenticate(code: str) -> bool:
    response = requests.post(
        "https://api.schwabapi.com/v1/oauth/token",
        headers={
            "Authorization": f"Basic {base64.b64encode(f"{CLIENT_ID}:{SECRET}".encode()).decode()}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
    )

    if response.status_code == 200:
        with TOKENS.open("w") as f:
            json.dump(response.json(), f)

    return response.status_code == 200


def refresh():
    with TOKENS.open("r") as f:
        tokens = json.load(f)

    response = requests.post(
        "https://api.schwabapi.com/v1/oauth/token",
        headers={
            "Authorization": f"Basic {base64.b64encode(f'{CLIENT_ID}:{SECRET}'.encode()).decode()}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "refresh_token",
            "refresh_token": tokens["refresh_token"],
        },
    )

    if response.status_code == 200:
        with TOKENS.open("w") as f:
            json.dump(response.json(), f)

    return response.status_code == 200


def access_token_expired() -> bool:
    THIRTY_MINUTES = 1800
    with TOKENS.open("r") as f:
        tokens = json.load(f)
        payload = jwt.decode(
            tokens["id_token"],
            algorithms=["HS256"],
            options={"verify_signature": False},
        )
        return datetime.now().timestamp() >= (payload["iat"] + THIRTY_MINUTES)


def refresh_token_expired() -> bool:
    SEVEN_DAYS = 604800
    with TOKENS.open("r") as f:
        tokens = json.load(f)
        payload = jwt.decode(
            tokens["id_token"],
            algorithms=["HS256"],
            options={"verify_signature": False},
        )
        return datetime.now().timestamp() >= (payload["iat"] + SEVEN_DAYS)
