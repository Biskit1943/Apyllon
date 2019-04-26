from sqlalchemy.orm import Session

from .models import Songs


def create(
        *,
        filepath: str,
        artist: str = None,
        title: str = None,
        album: str = None,
        genre: str = None,
        length: int,
        db: Session = None
) -> Songs:
    song = Songs(
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
    return song
