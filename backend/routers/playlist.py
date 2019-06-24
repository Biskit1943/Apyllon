from fastapi import (
    APIRouter,
    Depends,
    HTTPException)

from backend.player import player_
from backend_database import *
from backend_database.playlist_utils import ls as list_playlists
from backend_database.song_utils import get_song

router = APIRouter()


@router.get('/', response_model=PlaylistIndexed)
async def get_playlist(current_user: Users = Depends(get_current_active_user)):
    queue = player_.queue
    if not queue:
        return PlaylistIndexed(**{'songs': []})

    return PlaylistIndexed(**queue.to_playlist(current_user))


@router.get('/list', response_model=PlaylistsOut)
async def get_playlists(current_user: Users = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return PlaylistsOut(**list_playlists(current_user, db))


@router.put('/add', response_model=PlaylistIndexed)
async def add_to_playlist(
        song: SongIn,
        current_user: Users = Depends(get_current_active_user),
        db: Session = Depends(get_db),
):
    song = get_song(song.song_path, song.type, db)
    if not song:
        raise HTTPException(status_code=404, detail="Failed to find Song")

    player_.add_song(song)

    return PlaylistIndexed(**player_.queue.to_playlist(current_user))


@router.put('/save', response_model=PlaylistIndexed)
async def save_playlist(
        playlist_in: Playlist,
        current_user: Users = Depends(get_current_active_user),
        db: Session = Depends(get_db),
):
    queue = player_.queue
    if not queue:
        return PlaylistIndexed(**{'songs': []})

    return PlaylistIndexed(**queue.to_playlist(current_user=current_user, name=playlist_in.title, db=db))
