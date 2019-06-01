from enum import Enum
from typing import Union

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from passlib.hash import md5_crypt

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = 'HS256'
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl='/token')
PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')
PATH_CONTEXT = md5_crypt
SECRET_KEY = 'mein_sekret'
TOKEN_SUBJECT = 'access'
MUSIC_LIB = '/home/max/Music'


class SongTypes(Enum):
    FILE = 1
    YOUTUBE = 2
    DATABASE = 3


TYPES = {SongTypes.FILE.value: 'File', SongTypes.YOUTUBE.value: 'YouTube'}


def get_type(t: Union[str, int], type_=None) -> Union[str, int]:
    if type(t) is str:
        if type_ == str:
            return t
        for k, v in TYPES.items():
            if v == t:
                return k
        else:
            raise StopIteration('Not found')
    elif type(t) is int:
        if type_ == int:
            return t
        v = TYPES.get(t)
        if not v:
            raise StopIteration('Not found')
        return v
