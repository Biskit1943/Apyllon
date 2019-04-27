import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request

DATABASE_URL = "sqlite:///app.sqlite"
engine = sqlalchemy.create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
Base = declarative_base()


def get_db(request: Request) -> Session:
    return request.state.db


# import modules
from backend_database.fastapi_models import *
from backend_database.security import *
from backend_database.models import *
from backend_database.user_utils import *

'''
from backend_database import *
or
from . import ...

This makes the other modules available to each other without having to import
them from each module. This also makes everything importable from the top level
module (backend_database)

e.g.:
from .modules import Users
vs.
from . import Users
'''
__all__ = [
    'Admin',
    'AdminIn',
    'authenticate_user',
    'Base',
    'create_access_token',
    'create_first_user',
    'create_user',
    'get_current_active_superuser',
    'get_current_active_user',
    'get_current_user',
    'get_db',
    'get_password_hash',
    'get_user',
    'PlayerState',
    'Playlist',
    'PlaylistOut',
    'PlaylistsOut',
    'PlaylistIndexed',
    'Playlists',
    'Session',
    'Song',
    'SongIn',
    'SongIndexed',
    'SongMeta',
    'Songs',
    'Token',
    'TokenPayload',
    'update_user',
    'User',
    'UserIn',
    'UserInDB',
    'Users',
    'verify_password',
]

# create tables if not existing
Base.metadata.create_all(engine)
