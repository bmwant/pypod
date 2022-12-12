from threading import Thread
from typing import Optional
from pathlib import Path

from pypod.song import Song, WAVSong


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
        self._current : Song = None
        self._lock = None
        self.playlist = None

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
        for song in self.playlist:
            t = Thread(target=song.play,)
            self._current = song
            t.start()
            break
        print("Finished whole playlist")

    def terminate(self):
        pass

    @property
    def is_playing(self) -> bool:
        return self._current is not None and not self._current.paused

    @property
    def song(self) -> Optional[Song]:
        """Return currently playing song"""
        return self._current

    def pause(self):
        if self.is_playing:
            self.song.pause()

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
