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
print(player.get_queue_name())
player.add_local_database_object(databaseObj)
player.play()
time.sleep(2)
player.get_current_meta()
time.sleep(60)

