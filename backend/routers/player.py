from fastapi import (
    APIRouter,
    Depends,
)

from backend.player import player_
from backend_database import *

router = APIRouter()


@router.get('/state', response_model=PlayerState)
async def get_player_state(db: Session = Depends(get_db)):
    return


@router.put('/play', response_model=PlayerState)
async def play(db: Session = Depends(get_db), _: Users = Depends(get_current_active_user)):
    try:
        player_.play()
    except:
        raise
    return PlayerState(**{'loop': False, 'state': 'play', 'shuffle': False})


@router.put('/pause', response_model=PlayerState)
async def pause(db: Session = Depends(get_db), _: Users = Depends(get_current_active_user)):
    try:
        player_.pause()
    except:
        raise
    return PlayerState(**{'loop': False, 'state': 'pause', 'shuffle': False})

