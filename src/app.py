import base64
import json

from urllib.parse import urlencode

import requests

from flask import Flask, Response, redirect, request, render_template

from . import CLIENT_ID, REDIRECT_URI, SECRET


app = Flask(__name__)


def authenticate(code: str):
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

    match response.status_code:
        case 200:
            with open("tokens.json", "w") as f:
                json.dump(response.json(), f)

            return Response(status=200)
        case _:
            return Response(status=500)


def refresh():
    with open("tokens.json", "r") as f:
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

    with open("tokens.json", "w") as f:
        json.dump(response.json(), f)


@app.route("/login")
def login():
    url = "https://api.schwabapi.com/v1/oauth/authorize"
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
    }
    return redirect(f"{url}?{urlencode(params)}")


@app.route("/")
def index():
    code = request.args.get("code")

    if code:
        authenticate(code)

    return render_template("index.html")
