from threading import Thread
import time

from rich.progress import Progress, TaskProgressColumn, BarColumn

def update_progress():
    print("Running in the thread")


def run():
    s = Song()
    t = Thread(target=s.play, )
    prog = Progress(BarColumn())
    # cols = Progress.get_default_columns()
    with prog:
        task1 = prog.add_task("[red]Playing...", total=100)
        t.start()
        while not prog.finished:
            prog.update(task1, completed=s.progress)
            print("Reported progress is", s.progress)
            time.sleep(0.1)

    print("We are in the main thread")
    t.join()

class Song:
    def __init__(self):
        self._p = 0

    def play(self):
        for i in range(10):
            print("Playing at second", i, self._p)
            time.sleep(2)
            self._p += 10

    @property
    def progress(self):
        return self._p



if __name__ == "__main__":
    run()
