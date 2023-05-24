from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from .config import settings


def get_engine():
    user, password, host, port, db = settings
    url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    if not database_exists(url):
        create_database(url)
    return create_engine(url, pool_size=50, echo=False)


def get_session():
    engine = get_engine()
    return sessionmaker(bind=engine)(), engine
