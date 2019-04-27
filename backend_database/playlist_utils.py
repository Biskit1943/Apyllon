import logging

logger = logging.getLogger(__name__)

from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.schema import Sequence

from .models import Playlists, Users, Songs


def get_next_playlist_id(db: Session) -> int:
    return db.execute(Sequence('playlists_id_seq'))


def create(user: Users, name: str, songs: List[Songs] = [], db: Session = None) -> Playlists:
    p = Playlists(
        user=user,
        name=name,
        songs=songs
    )
    if db:
        db.add(p)
        db.commit()
        logger.info('Successfully created Playlist')

    return p


def append(playlist: Playlists, *, song: Songs = None, songs: List[Songs] = None, db: Session = None) -> Playlists:
    playlist.add(song=song, songs=songs)
    if db:
        db.add(playlist)
        db.commit()
        logger.info('Updated Playlist')

    return playlist


def get(id_: int, db: Session):
    return db.query(Playlists).filter(Playlists.id_ == id_).first()


def ls(user: Users, db: Session):
    playlists = [p.to_dict() for p in db.query(Playlists).filter(Playlists.user_id == user.id_).all()]
    return {
        'playlists': playlists,
    }
