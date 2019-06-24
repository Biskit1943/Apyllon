from datetime import (
    timedelta,
    datetime,
)

import jwt

from config import (
    ALGORITHM,
    SECRET_KEY,
    TOKEN_SUBJECT,
    PWD_CONTEXT,
)

__all__ = [
    'create_access_token',
    'get_password_hash',
    'verify_password',
]


def verify_password(plain_password: str, hashed_password: str):
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": TOKEN_SUBJECT})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
