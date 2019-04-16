from typing import Union

import jwt
from fastapi import Depends, Security, HTTPException
from fastapi.encoders import jsonable_encoder
from jwt import PyJWTError
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN

from config import (
    OAUTH2_SCHEME,
    ALGORITHM,
    SECRET_KEY,
)
from . import (
    get_db,
    Users,
    UserIn,
    AdminIn,
    TokenPayload,
    get_password_hash,
    verify_password,
)

__all__ = [
    'authenticate_user',
    'create_first_user',
    'create_user',
    'get_current_active_superuser',
    'get_current_active_user',
    'get_current_user',
    'get_user',
    'update_user',
]


def get_user(db: Session, identifier: Union[int, str]) -> Users:
    if type(identifier) is int:
        u = db.query(Users).filter(Users.id_ == identifier).first()
        return u
    elif type(identifier) is str:
        u = db.query(Users).filter(Users.username == identifier).first()
        return u


def create_user(db: Session, *, user_in: Union[UserIn, AdminIn]) -> Users:
    if type(user_in) is UserIn:
        user = Users(username=user_in.username, password=get_password_hash(user_in.password))
    else:
        user = Users(username=user_in.username, password=get_password_hash(user_in.password), admin=user_in.admin)
    db.add(user)
    db.commit()
    return user


async def get_current_user(db: Session = Depends(get_db), token: str = Security(OAUTH2_SCHEME)) -> Users:
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


async def create_first_user(db: Session) -> Union[None, str]:
    user = db.query(Users).first()
    if user:
        return None

    import string
    import secrets
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for _ in range(20))
    create_user(db, user_in=AdminIn(username='admin', password=password, admin=True))
    return password


async def update_user(db: Session, *, user: Users, user_in: UserIn):
    user_data = jsonable_encoder(user)
    for field in user_data:
        if field in user_in.fields:
            value_in = getattr(user_in, field)
            if value_in is not None:
                setattr(user, field, value_in)
    if user_in.password:
        password_hash = get_password_hash(user_in.password)
        user.password = password_hash
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
