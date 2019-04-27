from fastapi import (
    APIRouter,
    Depends,
)

from backend.player import player_
from backend_database import *

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
