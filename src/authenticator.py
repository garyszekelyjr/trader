import json
import ssl
import time
import urllib.parse as urlparse
import webbrowser

from threading import Thread

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlencode

from . import CLIENT_ID, REDIRECT_URI, PEM_PASSWORD, TOKENS, schwab


class Authenticator:
    authenticated = False

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            url = urlparse.urlparse(self.path)
            params = urlparse.parse_qs(url.query)
            code = params.get("code", None)

            if code:
                Authenticator.authenticated = schwab.authenticate(code.pop())
                self.send_response(200 if Authenticator.authenticated else 401)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
            else:
                url = "https://api.schwabapi.com/v1/oauth/authorize"
                params = {
                    "client_id": CLIENT_ID,
                    "redirect_uri": REDIRECT_URI,
                }
                self.send_response(302)
                self.send_header("Location", f"{url}?{urlencode(params)}")
                self.end_headers()

    def __init__(self):
        self.server = HTTPServer(("127.0.0.1", 443), Authenticator.Handler)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain("cert.pem", "key.pem", PEM_PASSWORD)
        self.server.socket = context.wrap_socket(self.server.socket, server_side=True)

    def login(self) -> str:
        if not TOKENS.exists():
            print("Tokens Not Found. Authenticating...")
            self.__authenticate__()
        elif schwab.refresh_token_expired():
            print("Refresh Token Expired. Reauthenticating...")
            self.__authenticate__()
        elif schwab.access_token_expired():
            print("Access Token Expired. Refreshing...")
            self.authenticated = schwab.refresh()
        else:
            self.authenticated = True

        return self.__access_token__()

    def __authenticate__(self):
        server = Thread(target=self.server.serve_forever)
        server.start()

        webbrowser.open(REDIRECT_URI)
        while not self.authenticated:
            time.sleep(1)

        self.server.shutdown()
        server.join()

    def __access_token__(self) -> str:
        if self.authenticated:
            with TOKENS.open("r") as f:
                tokens = json.load(f)
                return tokens["access_token"]

        return ""
