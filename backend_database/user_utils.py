from typing import Union

import jwt
from fastapi import Depends, Security, HTTPException
from jwt import PyJWTError
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN

from config import (
    oauth2_scheme,
    ALGORITHM,
    SECRET_KEY,
)
from . import (
    get_db,
    Users,
)
from .fastapi_models import (
    UserIn,
    TokenPayload,
)
from .security import (
    get_password_hash,
    verify_password,
)


def get_user(db: Session, identifier: Union[int, str]) -> Users:
    if type(identifier) is int:
        u = db.query(Users).filter(Users.id_ == identifier).first()
        return u
    elif type(identifier) is str:
        u = db.query(Users).filter(Users.username == identifier).first()
        return u


def create_user(db: Session, *, user_in: UserIn) -> Users:
    user = Users(username=user_in.username, password=get_password_hash(user_in.password))
    db.add(user)
    db.commit()
    return user


async def get_current_user(db: Session = Depends(get_db), token: str = Security(oauth2_scheme)) -> Users:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = get_user(db, identifier=token_data.username)
    return user


async def get_current_active_user(current_user: Users = Depends(get_current_user)) -> Users:
    return current_user


async def get_current_active_superuser(current_user: Users = Depends(get_current_user)) -> Users:
    if not current_user.admin:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="You have not the correct access rights"
        )
    return current_user


def authenticate_user(db: Session, username: str, password: str) -> Union[bool, Users]:
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
