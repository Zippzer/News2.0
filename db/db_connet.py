import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from service import token_env


POSTGRES_USER = token_env.POSTGRES_USER
POSTGRES_PASSWORD = token_env.POSTGRES_PASSWORD
POSTGRES_HOST = token_env.POSTGRES_HOST
POSTGRES_DB = token_env.POSTGRES_DB
POSTGRES_PORT = token_env.POSTGRES_PORT


DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
