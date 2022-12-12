from threading import Thread
from pathlib import Path
from pypod.song import WAVSong


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
        self._is_playing = False

    @staticmethod
    def generate_playlist(filepath: str | Path) -> Playlist:
        filepath = Path(filepath)
        if filepath.is_dir():
            raise NotImplementedError("Can load only one file for now")
        
        playlist = Playlist("Default playlist")
        s1 = WAVSong(filepath.absolute())
        playlist.add_song(s1)

        return playlist

    def load(self, playlist: Playlist):
        self.playlist = playlist

    def play(self):
        for s in self.playlist:
            t = Thread(target=s.play,)
            t.start()
            break
        print("Finished whole playlist")

    @property
    def is_playing(self):
        return self._is_playing

    def pause(self):
        pass

    def next(self):
        pass

    def prev(self):
        pass

    def __del__(self):
        """Terminate running threads if any"""


if __name__ == "__main__":
    from pypod import config
    filename = config.ASSETS_DIR / "rain_and_storm.wav"
    player = Pod()
    playlist = player.generate_playlist(filename)
    player.load(playlist)
    player.play()
