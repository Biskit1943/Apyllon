from player import Player
import time

player = Player()
player.add_local("glitch.m4a")
player.add_youtube("https://www.youtube.com/watch?v=LBZ-3Ugj1AQ")
player.play()

time.sleep(10)
player.next()
time.sleep(10)
