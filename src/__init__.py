import os

from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine

from .models import Base


load_dotenv()

CLIENT_ID = os.getenv("SCHWAB_CLIENT_ID", "")

SECRET = os.getenv("SCHWAB_CLIENT_SECRET", "")

PEM_PASSWORD = os.getenv("PEM_PASSWORD", "")

REDIRECT_URI = "https://127.0.0.1"

ENGINE = create_engine("sqlite:///db.sqlite")

TOKENS = Path("tokens.json")

Base.metadata.create_all(ENGINE)
