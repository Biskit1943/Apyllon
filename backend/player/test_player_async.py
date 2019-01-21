from player import Player
import time

class database_object():
    def __init__(self):
        self.artist = "Tool"
        self.title = "Sober"
        self.album = "Lateralus"
        self.genre = "Rock"
        self.filepath = "./glitch.m4a"


databaseObj = database_object()


player = Player()
player.set_playback_mode("repeat_queue")
print(player.add_youtube("https://www.youtube.com/watch?v=8oOF5A0wd4Q"))
print(player.add_local_database_object(databaseObj))
player.play()
time.sleep(1000)

