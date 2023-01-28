"""Testing features"""
import time
from threading import Thread

from pypod import config
from pypod.song import WAVSong


def main():
    filepath = config.ASSETS_DIR / "rain_and_storm.wav"
    s1 = WAVSong(filepath=filepath)

    t = Thread(
        target=s1.play,
    )
    t.start()
    time.sleep(2)
    s1.paused = True
    time.sleep(2)
    s1.paused = False
    time.sleep(3)
    s1.paused = True


if __name__ == "__main__":
    main()
