import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///app.sqlite"
engine = sqlalchemy.create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

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
