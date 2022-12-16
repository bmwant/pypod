import time
import wave as pywave
import contextlib
from pathlib import Path

import pyaudio


# TODO: make abstract class 
class Song:
    def __init__(self, filepath: Path):
        self.filepath: Path = filepath
        self.paused: bool = True
        self.stopped: bool = True

    def play(self):
        pass

    def pause(self):
        self.paused = True

    def stop(self):
        self.stopped = True

    def duration(self):
        pass

    def progress(self):
        pass

    @property
    def name(self):
        return self.filepath.stem

    def __str__(self):
        return self.name

    def __rich__(self):
        return "Song name with icon"


class WAVSong(Song):

    CHUNK = 1024

    def __init__(self, filepath: Path):
        super().__init__(filepath=filepath)
        self.py_audio = pyaudio.PyAudio()

    def play(self):
        with pywave.open(str(self.filepath), "rb") as wave:
            format = self.py_audio.get_format_from_width(
                wave.getsampwidth()
            )
            stream = self.py_audio.open(
                format=format,
                channels=wave.getnchannels(),
                rate=wave.getframerate(),
                output=True,
            )
            self.paused = False
            self.stopped = False
            with contextlib.closing(stream):
                while True:
                    if self.stopped:
                        return
                    if self.paused:
                        if stream.is_active():
                            stream.stop_stream()
                        time.sleep(0.01)
                    else:
                        if stream.is_stopped():
                            stream.start_stream()
                        data = wave.readframes(self.CHUNK)
                        if not data:
                            break
                        stream.write(data)
                stream.stop_stream()
            self.paused = True

    def __del__(self):
        self.py_audio.terminate()

    @property
    def duration(self) -> float:
        with pywave.open(str(self.filepath), "rb") as wave:
            frames = wave.getnframes()
            rate = float(wave.getframerate())
        return frames / rate


if __name__ == "__main__":
    from pypod import config
    filepath = config.ASSETS_DIR / "rain_and_storm.wav"
    s1 = WAVSong(filepath=filepath)
    s1.play()