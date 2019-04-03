from fastapi import FastAPI

from backend_database import *

app = FastAPI()


@app.on_event("startup")
async def startup():
    user = Users(username='max', password='pw')
    filepath = FilePaths(filename='test.mp3', directory='/root')
    song = Songs(filepath=filepath, artist='artist',
                 title='title', album='album', genre='genre', length=42)
    playlist = Playlists(name='p1', user=user, songs=[song])
    session.add_all([user, filepath, song, playlist])
    session.commit()

    for model in [Users, FilePaths, Songs, Playlists]:
        print(session.query(model).all())


@app.on_event("shutdown")
async def shutdown():
    pass
