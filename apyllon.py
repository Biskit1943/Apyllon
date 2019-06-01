import logging
from logging.config import dictConfig

from logger import logging_config

logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from backend.routers import (
    player,
    users,
    playlist,
)
import backend_database as bd
from backend.player import player_


@app.on_event("startup")
async def startup():
    db = bd.Session()
    pw = await bd.create_first_user(db)
    if pw:
        # Note: This print only works on 20 character passwords
        print(f'''
################################################################################
#                    Copy this Password and login as admin.                    #
#                  After that immediately change the password!                 #
#                                                                              #
#                             {pw}                             #
#                                                                              #
################################################################################''')
    # # TODO:  This is just done for mocking
    # player_.add_youtube('https://www.youtube.com/watch?v=PXbU_UI-lAg', db=db)
    # player_.add_youtube('https://www.youtube.com/watch?v=LBZ-3Ugj1AQ', db=db)
    player_.add_youtube('https://www.youtube.com/watch?v=U5u9glfqDsc', db=db)
    db.close()


@app.on_event("shutdown")
async def shutdown():
    pass


@app.middleware("http")
async def db_session_middleware(
        request: Request,
        call_next
):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = bd.Session()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


app.include_router(users.router)
app.include_router(
    player.router,
    prefix="/player",
    tags=["player"],
)
app.include_router(
    playlist.router,
    prefix="/player/playlist",
    tags=["playlist"],
)
