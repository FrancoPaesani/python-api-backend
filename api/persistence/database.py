from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import DATABASE_URL

engine = create_engine(DATABASE_URL, future=True, echo=True)
session = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
