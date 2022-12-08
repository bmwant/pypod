import wave

class Song:
    def __init__(self, filepath):
        self.filepath = filepath

    def play(self):
        pass

    def duration(self):
        pass

    def progress(self):
        pass

    def name(self):
        return "Song name"

    def __str__(self):
        return "Song name"

    def __rich__(self):
        return "Song name with icon"


class WAVSong(Song):
    def __init__(self, filepath):
        super().__init__(filepath=filepath)
        self._wave = None


    def __enter__(self):
        self._wave = wave.open(self.filepath, "rb")
        return self

    def __exit__(self, *exc):
        self._wave.close()

    @property
    def duration(self):
        frames = self._wave.getnframes()
        rate = float(self._wave.getframerate())
        return frames / rate


if __name__ == "__main__":
    s1 = Song("./assets/camera.wav")
    s2 = Song("./assets/rain_and_storm.wav")
    with s1, s2:
        print(s1.duration)
        print(s2.duration)
