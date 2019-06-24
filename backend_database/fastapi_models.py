from typing import List, Union

from pydantic import BaseModel

__all__ = [
    'Admin',
    'AdminIn',
    'PlayerState',
    'Playlist',
    'PlaylistOut',
    'PlaylistsOut',
    'PlaylistIndexed',
    'Song',
    'SongIn',
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


class SongIn(BaseModel):
    song_path: str
    type: int


class Song(BaseModel):
    length: int
    meta: SongMeta


class SongIndexed(Song):
    index: int


class PlayerState(BaseModel):
    loop: bool = None
    state: str = None
    next: Song = None
    current: Song = None
    previous: Song = None
    shuffle: bool = None
    queue_or_song: Union[str, Song] = None


class Playlist(BaseModel):
    title: str = None


class PlaylistIndexed(Playlist):
    songs: List[SongIndexed]


class PlaylistOut(Playlist):
    songs: List[Song]


class PlaylistsOut(BaseModel):
    playlists: List[PlaylistOut]
