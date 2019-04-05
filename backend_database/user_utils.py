from typing import Union

import jwt
from fastapi import Depends, Security, HTTPException
from jwt import PyJWTError
from starlette.status import HTTP_403_FORBIDDEN

from config import (
    oauth2_scheme,
    ALGORITHM,
    SECRET_KEY,
)
from . import (
    session,
    Users,
)
from .fastapi_models import User, TokenPayload


def get_user(identifier: Union[int, str]) -> Users:
    if type(identifier) is int:
        u = session.query(Users).filter(Users.id_ == identifier).first()
        return u
    elif type(identifier) is str:
        u = session.query(Users).filter(Users.username == identifier).first()
        return u


async def get_current_user(token: str = Security(oauth2_scheme)) -> Users:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = get_user(identifier=token_data.username)
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user
