from fastapi import (
    APIRouter,
    Depends,
)

from backend.player import player_
from backend_database import *
import json

router = APIRouter()


@router.get('/state', response_model=PlayerState)
async def get_player_state(_: Users = Depends(get_current_active_user)):
    try:
        state = player_.get_state()
    except:
        raise
    return state


@router.put('/play', response_model=PlayerState)
async def play(_: Users = Depends(get_current_active_user)):
    try:
        state = player_.play()
    except:
        raise
    return state


@router.put('/pause', response_model=PlayerState)
async def pause(_: Users = Depends(get_current_active_user)):
    try:
        state = player_.pause()
    except:
        raise
    return state


@router.put('/stop', response_model=PlayerState)
async def stop(_: Users = Depends(get_current_active_user)):
    try:
        state = player_.stop()
    except:
        raise
    return state


@router.put('/next', response_model=PlayerState)
async def next(_: Users = Depends(get_current_active_user)):
    try:
        state = player_.next()
    except:
        raise
    return state


@router.put('/previous', response_model=PlayerState)
async def prev(_: Users = Depends(get_current_active_user)):
    try:
        state = player_.prev()
    except:
        raise
    return state


@router.put('/shuffle', response_model=PlayerState)
async def shuffle(_: Users = Depends(get_current_active_user)):
    try:
        state = player_.shuffle()
    except:
        raise
    return state


@router.put('/loop', response_model=PlayerState)
async def shuffle(_: Users = Depends(get_current_active_user)):
    try:
        state = player_.loop()
    except:
        raise
    return state
