from pydantic import BaseModel


class User(BaseModel):
    username: str


class UserIn(User):
    password: str


class UserInDB(User):
    id: int
    admin: bool
