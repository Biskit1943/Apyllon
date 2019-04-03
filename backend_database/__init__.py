import sqlalchemy

from passlib.context import CryptContext
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///app.sqlite"
engine = sqlalchemy.create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# import Models
from .models import (
    FilePaths,
    Playlists,
    Songs,
    Users,
)

# from backend_database import *
__all__ = [
    'session',
    'FilePaths',
    'Playlists',
    'Songs',
    'Users',
]

# create tables if not existing
Base.metadata.create_all(engine)
