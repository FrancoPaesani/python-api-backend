import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT") or "")
RELOAD = os.getenv("RELOAD")
WORKERS = int(os.getenv("WORKERS") or 1)

VERSION = os.getenv("VERSION")

DATABASE_URL = os.getenv("DATABASE_URL")
