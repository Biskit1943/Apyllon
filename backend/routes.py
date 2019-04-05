from datetime import timedelta

from fastapi import (
    Depends,
    HTTPException,
)
from fastapi.security import OAuth2PasswordRequestForm

from apyllon import app
from backend_database.fastapi_models import (
    User,
    Token,
)
from backend_database.security import (
    authenticate_user,
    create_access_token,
)
from backend_database.user_utils import get_current_active_user
from config import ACCESS_TOKEN_EXPIRE_MINUTES


@app.post("/token", response_model=Token)
async def route_login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
