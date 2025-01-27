import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
RELOAD = os.getenv("RELOAD")
WORKERS = os.getenv("WORKERS")

VERSION = os.getenv("VERSION")

DATABASE_URL = os.getenv("DATABASE_URL")
