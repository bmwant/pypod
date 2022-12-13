from threading import Thread
from typing import Optional
from pathlib import Path

from pypod.song import Song, WAVSong


class Playlist:
    def __init__(self, name: str):
        self.name = name
        self.songs = []
        self._index = 0

    def add_song(self, song):
        self.songs.append(song)

    @property
    def position(self):
        return self._index

    def __getitem__(self, key):
        return self.songs.__getitem__(key)

    def __setitem__(self, key, value):
        self.songs.__setitem__(key, value)

    def __iter__(self):
        return iter(self.songs)

    def __next__(self):
        song = self.songs[self._index]
        self._index += 1
        self._index %= len(self.songs)
        return song

    def get_next(self):
        index = (self._index + 1) % len(self)
        self._index = index
        return self[index]

    def get_prev(self):
        index = (self._index - 1) % len(self)
        self._index = index
        return self[index]

    def __len__(self):
        return len(self.songs)


class Pod:
    def __init__(self):
        self._current : Song = None
        self._thread = None
        self.playlist = None

    @staticmethod
    def generate_playlist(filepath: str | Path) -> Playlist:
        filepath = Path(filepath)
        playlist = Playlist("Default playlist")

        if filepath.is_dir():
            for song_path in sorted(filepath.glob("**/*.wav")):
                song = WAVSong(song_path.absolute())
                playlist.add_song(song)
        else:
            song = WAVSong(filepath.absolute())
            playlist.add_song(song)

        return playlist

    def load(self, playlist: Playlist):
        self.playlist = playlist

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
        song = self.playlist.get_next()
        self._play_song(song)

    def prev(self):
        if self.song is not None:
            self.song.stop()
        song = self.playlist.get_prev()
        self._play_song(song)

    def __del__(self):
        """Cleanup"""
        # TODO: save playlist/song state on exit?


def play_file():
    pass

def play_directory():
    from pypod import config
    player = Pod()
    playlist = player.generate_playlist(config.ASSETS_DIR)
    player.load(playlist)
    player.play()


if __name__ == "__main__":
    play_directory()
