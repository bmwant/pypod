import wave as pywave
import contextlib

import pyaudio

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

    CHUNK = 1024

    def __init__(self, filepath):
        super().__init__(filepath=filepath)
        self._wave = None
        self.py_audio = pyaudio.PyAudio()

    def __enter__(self):
        self._wave = pywave.open(self.filepath, "rb")
        return self

    def __exit__(self, *exc):
        self._wave.close()

    def play(self):
        with pywave.open(self.filepath, "rb") as wave:
            format = self.py_audio.get_format_from_width(
                wave.getsampwidth()
            )
            stream = self.py_audio.open(
                format=format,
                channels=wave.getnchannels(),
                rate=wave.getframerate(),
                output=True,
            )
            with contextlib.closing(stream):
                while data := wave.readframes(self.CHUNK):
                    # todo: report progress
                    stream.write(data)
                stream.stop_stream()
            # at obj deletion?
            self.py_audio.terminate()

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
