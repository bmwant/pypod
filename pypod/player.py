from threading import Thread


class Playlist:
    def __init__(self, name: str):
        self.name = name
        self.songs = []

    def add_song(self, song):
        self.songs.append(song)

    def __iter__(self):
        return iter(self.songs)


class Pod:
    def __init__(self):
        self._current = None
        self._lock = None
        self.playlist = None

    @staticmethod
    def generate_playlist(filepath):
        playlist = Playlist("Default playlist")
        from pypod.song import WAVSong
        s1 = WAVSong("./assets/rain_and_storm.wav")
        playlist.add_song(s1)

        return playlist

    def load(self, playlist: Playlist):
        self.playlist = playlist

    def play(self):
        for s in self.playlist:
            t = Thread(target=s.play,)
            t.start()
            t.join()
            break
        print("Finished whole playlist")


if __name__ == "__main__":
    player = Pod()
    playlist = player.generate_playlist("assets")
    player.load(playlist)
    player.play()
