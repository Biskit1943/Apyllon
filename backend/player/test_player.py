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
print("1")
print(player.add_youtube("https://www.youtube.com/watch?v=8oOF5A0wd4Q"))
print(player.add_local('./glitch.m4a'))
print(player.add_local_database_object(databaseObj))
print("3")
player.play()
time.sleep(2)
print("4")
player.pause()
time.sleep(2)
print("5")
player.play()
time.sleep(2)
player.play()
time.sleep(2)
print("6")
player.next()
time.sleep(5)
print("6")
player.previous()
time.sleep(5)
player.next()
print(player.get_current_meta())
time.sleep(2)

