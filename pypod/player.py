from threading import Thread
from typing import Optional
from pathlib import Path
from itertools import cycle

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
        self._thread = None
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
        self.playlist = cycle(playlist)

    def play_playlist(self):
        for song in self.playlist:
            t = Thread(target=song.play,)
            self._current = song
            t.start()
            break
        print("Finished whole playlist")

    def play(self):
        if self.is_playing:
            return

        print("Unpausing current song")
        # un-pause section
        song = self.song
        if song is not None and song.paused:
            song.paused = False
            return 

        # play from playlist section
        song = next(self.playlist)
        self._play_song(song)
        
    def _play_song(self, song):
        t = Thread(target=song.play,)
        self._current = song
        print(f"Start playing {song} song")
        t.start()
        self._thread = t

    def exit(self):
        if self.song is not None:
            print("Stopping current song")
            self.song.stop()
            self._thread.join()

    @property
    def is_playing(self) -> bool:
        return self._current is not None and not self._current.paused

    @property
    def song(self) -> Optional[Song]:
        """Return currently playing song"""
        return self._current

    def pause(self):
        if self.is_playing:
            print("Pausing current song")
            self.song.pause()

    def next(self):
        if self.song is not None:
            self.song.stop()
        song = next(self.playlist)
        print(f"Playing next {song} {song.stopped} {song.paused}")
        self._play_song(song)

    def prev(self):
        if self.song is not None:
            self.song.stop()

    def __del__(self):
        """Cleanup"""
        # TODO: save playlist/song state on exit?


if __name__ == "__main__":
    from pypod import config
    filename = config.ASSETS_DIR / "rain_and_storm.wav"
    player = Pod()
    playlist = player.generate_playlist(filename)
    player.load(playlist)
    player.play()
