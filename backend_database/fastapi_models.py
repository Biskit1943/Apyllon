from pydantic import BaseModel


class User(BaseModel):
    username: str


class UserIn(User):
    password: str


class UserInDB(User):
    id: int
    admin: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    username: str = None
