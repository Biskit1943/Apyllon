from datetime import timedelta

from fastapi import (
    Depends,
    HTTPException,
)
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request
from starlette.responses import Response

from apyllon import app
from backend_database import (
    get_db,
    Session,
)
from backend_database.fastapi_models import (
    User,
    UserIn,
    Token,
)
from backend_database.models import Users
from backend_database.security import (
    create_access_token,
)
from backend_database.user_utils import (
    authenticate_user,
    create_user,
    get_user,
    get_current_active_superuser,
    get_current_active_user,
)
from config import ACCESS_TOKEN_EXPIRE_MINUTES


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = Session()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.post("/token", response_model=Token)
async def route_login_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register", response_model=User)
async def register(*, db: Session = Depends(get_db), user_in: UserIn,
                   current_user: Users = Depends(get_current_active_superuser)):
    user = get_user(db, user_in.username)
    if user:
        raise HTTPException(status_code=409, detail="User already exist")

    new_user = create_user(db, user_in=user_in)
    return User(**new_user.to_json())


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: Users = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: Users = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
