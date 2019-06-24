import logging

logger = logging.getLogger(__name__)

from typing import Union
from sqlalchemy.orm import Session
from pytube import YouTube

from config import get_type, SongTypes
from .models import Songs


def create(
        *,
        filepath: str,
        type_: Union[str, int],
        artist: str = None,
        title: str = None,
        album: str = None,
        genre: str = None,
        length: int,
        db: Session = None,
) -> Songs:
    t = get_type(type_, int)
    song = db.query(Songs).filter(Songs.filepath == filepath).first()
    if song:
        return song
    song = Songs(
        type_=t,
        filepath=filepath,
        artist=artist,
        title=title,
        album=album,
        genre=genre,
        length=length
    )
    if db:
        db.add(song)
        db.commit()
        logger.info('Successfully created Song')
    return song


def get_song(filepath: str, t: int, db: Session):
    type_ = get_type(t, int)
    song = db.query(Songs).filter(Songs.filepath == filepath).filter(Songs.type_ == type_).first()
    if not song:
        if t is SongTypes.YOUTUBE.value:
            yt = YouTube(filepath)
            title = yt.title
            if not title:
                logger.info('Failed to get title from Video URL')
            song = create(type_=SongTypes.YOUTUBE.value, filepath=filepath, title=title, length=int(yt.length), db=db)
        else:
            return None

    return song


def get_song_by_title(title: str, db: Session):
    song = db.query(Songs).filter(Songs.title == title).first()
    if song:
        return song
    raise FileNotFoundError('Song not Found')


def get_youtube_url(filepath: str):
    yt = YouTube(filepath)
    yt_song = yt.streams.filter(only_audio=True).first()
    return yt_song.url
