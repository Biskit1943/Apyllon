from datetime import timedelta

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
)
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm

from backend_database import *
from config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


@router.post("/token", tags=['authentication'], response_model=Token)
async def route_login_access_token(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", tags=['users'], response_model=User)
async def register(
        *,
        db: Session = Depends(get_db),
        user_in: UserIn,
        _: Users = Depends(get_current_active_superuser)
):
    user = get_user(db, user_in.username)
    if user:
        raise HTTPException(status_code=409, detail="User already exist")

    new_user = create_user(db, user_in=user_in)
    return User(**new_user.to_dict())


@router.get("/users/me", tags=['users', 'me'], response_model=User)
async def read_users_me(current_user: Users = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items/", tags=['users', 'me'])
async def read_own_items(current_user: Users = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


@router.put("/users/me", tags=['users', 'me'], response_model=User)
async def update_user_me(
        *,
        db: Session = Depends(get_db),
        password: str = Body(None),
        username: str = Body(None),
        current_user: Users = Depends(get_current_active_user),
):
    current_user_data = jsonable_encoder(current_user)
    user_in = UserIn(**current_user_data)
    if password is not None:
        user_in.password = password
    if username is not None:
        user_in.username = username
    user = await update_user(db, user=current_user, user_in=user_in)
    return user
