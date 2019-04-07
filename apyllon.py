from fastapi import FastAPI

app = FastAPI()

from backend import routes
from backend_database import *
from backend_database.security import get_password_hash


@app.on_event("startup")
async def startup():
    from sqlalchemy import exists
    db = Session()
    if not db.query(exists().where(Users.username == 'max')).scalar():
        user = Users(username='max')
        user.password = get_password_hash('pw')
        user.admin = True
        filepath = FilePaths(filename='test.mp3', directory='/root')
        song = Songs(filepath=filepath, artist='artist',
                     title='title', album='album', genre='genre', length=42)
        playlist = Playlists(name='p1', user=user, songs=[song])
        db.add_all([user, filepath, song, playlist])
        db.commit()

    for model in [Users, FilePaths, Songs, Playlists]:
        print(db.query(model).all())
    db.close()


@app.on_event("shutdown")
async def shutdown():
    pass
