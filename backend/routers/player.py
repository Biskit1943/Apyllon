from fastapi import (
    APIRouter,
    Depends,
)

from backend.player import player_
from backend_database import *
from backend_database.song_utils import get_song_by_title
from config import get_type, SongTypes

router = APIRouter()


@router.get('/state', response_model=PlayerState)
async def get_player_state(_: Users = Depends(get_current_active_user)):
    try:
        state = player_.get_state()
    except:
        raise
    return PlayerState(**state)


@router.put('/play', response_model=PlayerState)
async def play(_: Users = Depends(get_current_active_user)):
    try:
        state = player_.play()
    except:
        raise
    return PlayerState(**state)


@router.put('/playsong', response_model=PlayerState)
async def play(song: SongIn, _: Users = Depends(get_current_active_user), db: Session = Depends(get_db)):
    try:
        path = song.song_path
        type_ = get_type(song.type, int)

        if song and (type_ == SongTypes.YOUTUBE.value or type_ == SongTypes.FILE.value):
            state = player_.play(path)
        elif song and type_ == SongTypes.DATABASE.value:
            song = get_song_by_title(path, db)
            # TODO: not working
            state = player_.play(song)
        else:
            state = player_.get_state()
    except:
        raise
    return PlayerState(**state)


@router.put('/pause', response_model=PlayerState)
async def pause(_: Users = Depends(get_current_active_user)):
    try:
        state = player_.pause()
    except:
        raise
    return PlayerState(**state)


@router.put('/stop', response_model=PlayerState)
async def stop(_: Users = Depends(get_current_active_user)):
    try:
        state = player_.stop()
    except:
        raise
    return PlayerState(**state)


@router.put('/next', response_model=PlayerState)
async def next(_: Users = Depends(get_current_active_user)):
    try:
        state = player_.next()
    except:
        raise
    return PlayerState(**state)


@router.put('/previous', response_model=PlayerState)
async def prev(_: Users = Depends(get_current_active_user)):
    try:
        state = player_.prev()
    except:
        raise
    return PlayerState(**state)


@router.put('/shuffle', response_model=PlayerState)
async def shuffle(_: Users = Depends(get_current_active_user)):
    try:
        state = player_.shuffle()
    except:
        raise
    return PlayerState(**state)


@router.put('/loop', response_model=PlayerState)
async def shuffle(_: Users = Depends(get_current_active_user)):
    try:
        state = player_.loop()
    except:
        raise
    return PlayerState(**state)
