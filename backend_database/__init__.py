import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request

DATABASE_URL = "sqlite:///app.sqlite"
engine = sqlalchemy.create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db(request: Request) -> Session:
    return request.state.db


# import Models
from .models import (
    FilePaths,
    Playlists,
    Songs,
    Users,
)

# from backend_database import *
__all__ = [
    'get_db',
    'Session',
    'FilePaths',
    'Playlists',
    'Songs',
    'Users',
]

# create tables if not existing
Base.metadata.create_all(engine)
