from typing import List

from pydantic import BaseModel

__all__ = [
    'Admin',
    'AdminIn',
    'PlayerState',
    'Playlist',
    'Song',
    'SongIndexed',
    'SongMeta',
    'Token',
    'TokenPayload',
    'User',
    'UserIn',
    'UserInDB',
]


class User(BaseModel):
    username: str


class Admin(User):
    admin: bool


class AdminIn(Admin):
    password: str


class UserIn(User):
    password: str


class UserInDB(User):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    username: str = None


class SongMeta(BaseModel):
    album: str = None
    artist: str = None
    genre: str = None
    title: str = None


class Song(BaseModel):
    filename: str
    length: int
    meta: SongMeta
    path: str


class SongIndexed(Song):
    index: int


class PlayerState(BaseModel):
    loop: bool
    state: str
    next: Song = None
    current: Song = None
    previous: Song = None
    shuffle: bool


class Playlist(BaseModel):
    songs: List[SongIndexed]
