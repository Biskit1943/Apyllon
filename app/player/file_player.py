import vlc

class FilePlayer():
    def __init__(self):
        self.vlcInstance = vlc.Instance()
        self.player = self.vlcInstance.media_player_new()

    def load(self, filepath):
        self.player.set_mrl(filepath)

    def play(self):
        self.player.play()

    def stop(self):
        self.player.stop()

if __name__ == "__main__":
    player = FilePlayer()
    player.load("test.mp4")

