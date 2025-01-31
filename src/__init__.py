import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from .models import Base


load_dotenv()

CLIENT_ID = os.getenv("SCHWAB_CLIENT_ID", "")

SECRET = os.getenv("SCHWAB_CLIENT_SECRET", "")

REDIRECT_URI = "https://127.0.0.1"

ENGINE = create_engine("sqlite:///db.sqlite")

Base.metadata.create_all(ENGINE)
