from sqlalchemy.orm import Session
from sqlalchemy.schema import Sequence

from .models import Playlists


def get_next_playlist_id(db: Session) -> int:
    return db.execute(Sequence('playlists_id_seq'))


async def create(db: Session) -> Playlists:
    return
