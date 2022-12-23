from rich.progress import Progress, Text, Task, TextColumn, BarColumn
from textual.widgets import ListView, ListItem, Static, Label, DataTable

from pypod.song import Song
from pypod.utils import sec_to_time


class PlaylistListView(Static):
    def __init__(self, playlist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.playlist = playlist
        self._list = ListView()

    def on_mount(self):
        # TODO: add header somehow
        for i, s in enumerate(self.playlist, start=1):
            duration = sec_to_time(s.duration)
            self._list.append(
                ListItem(
                    Label(f"{i}"),
                    Label(f"{s}", classes="song-name"),
                    Label(f"{duration}", classes="right"),
                )
            )

    def compose(self):
        yield self._list


class PlaylistTable(Static):
    def __init__(self, playlist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.playlist = playlist
        self.table = DataTable()

    def on_mount(self):
        # table = self.query_one(DataTable)
        table = self.table
        table.add_columns("#", "Name", "Duration")
        for i, s in enumerate(self.playlist, start=1):
            duration = sec_to_time(s.duration)
            table.add_row(f"{i}", f"{s}", f"{duration}")

    def compose(self):
        yield self.table


class ElapsedColumn(TextColumn):
    def __init__(self, *args, **kwargs):
        return super().__init__("", *args, **kwargs)

    def render(self, task: Task) -> Text:
        if task.description == "dummy":
            return "--:--"
        return sec_to_time(task.completed)


class LeftColumn(TextColumn):
    pass


class DurationColumn(TextColumn):
    def __init__(self, *args, **kwargs):
        return super().__init__("", *args, **kwargs)

    def render(self, task: Task) -> Text:
        if task.description == "dummy":
            return "--:--"
        return sec_to_time(task.total)


class ProgressDisplay(Static):
    """A widget to display song's progress."""

    INTERVAL = 0.1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_col = ElapsedColumn()
        self.end_col = DurationColumn()
        self.bar = BarColumn()
        self.p = Progress(
            self.start_col,
            self.bar,
            self.end_col,
        )
        self.task_id = self.p.add_task("dummy")
        self.timer = None

    def render(self):
        return self.p

    def update_progress(self):
        # TODO: this should pick actual progress of the song
        if self.p.finished:
            self.timer.stop_no_wait()
        else:
            self.p.advance(self.task_id, advance=self.INTERVAL)
        self.update()

    def pause(self):
        """Action on song pause to stop progress bar updates"""
        self.timer.pause()

    def resume(self):
        """Action on song play to resume progress bar updates"""
        self.timer.resume()

    def display_progress(self, song: Song):
        self.reset()

        self.task_id = self.p.add_task("play", total=int(song.duration))
        self.timer = self.set_interval(self.INTERVAL, self.update_progress)
        self.update()

    def reset(self):
        if self.task_id is not None:
            self.p.remove_task(self.task_id)

        # TODO: do we actually need this explicit tasks reset
        self.p._tasks = {}
        if self.timer is not None:
            self.timer.stop_no_wait()
            self._timers.discard(self.timer)
