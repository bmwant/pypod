from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header as Header_
from textual.widgets._header import HeaderTitle
from textual.widgets import Button, Footer, Static, DataTable
from textual.reactive import reactive


from pypod import config
from pypod.player import Pod


class ProgressDisplay(Static):
    """A widget to display song's progress."""


class Controls(Static):
    """A buttons widget to control playback."""

    def compose(self) -> ComposeResult:
        """Create child widgets of a stopwatch."""
        yield Button("❮❮", id="prev", variant="success")
        yield Button("▶", id="play", variant="warning")
        yield Button("❯❯", id="next", variant="success")

    def on_button_pressed(self, event: Button.Pressed):
        """Event handler called when a button is pressed."""
        button = event.button
        if button.id == "play":
            self.app.action_toggle_play()
        elif button.id == "prev":
            self.app.action_play_prev()
        elif button.id == "next":
            self.app.action_play_next()


class Header(Header_):
    DEFAULT_CSS = """
    Header {
        dock: top;
        width: 100%;
        background: $secondary-background;
        color: $text;
        height: 1;
    }
    Header.-tall {
        height: 1;
    }
    """

    def compose(self):
        yield HeaderTitle()

    def on_click(self):
        pass


class PlaylistTable(Static):
    def __init__(self, playlist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.playlist = playlist

    def on_mount(self):
        table = self.query_one(DataTable)
        table.on_click = self.on_click
        table.add_columns("#", "Name", "Duration")
        for i, s in enumerate(self.playlist, start=1):
            duration = s.format_duration(s.duration)
            table.add_row(f"{i}", f"{s}", f"{duration}")

    def compose(self):
        table = DataTable(
            zebra_stripes=True, 
            show_cursor=False,
        )
        yield table

    def on_click(self, *args, **kwargs):
        print("Hanlding this", args, kwargs)


class PyPodApp(App):
    """A Python terminal music player app."""

    CSS_PATH = "style.css"
    BINDINGS = [
        ("q", "quit", "quit"),
        ("p", "toggle_play", "play/pause"),
        ("n", "play_next", "next"),
        ("b", "play_prev", "back (previous)"),
    ]

    song_title = reactive("♫ not playing ♫")

    def __init__(self, player: Pod, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = player

    def on_mount(self):
        # ♫
        self.query_one(HeaderTitle).text = "🎵 PyPod"

    def watch_song_title(self, title: str):
        if not title.startswith("♫"):
            title = f"♫ {title} ..."
        self.query_one("#title").update(title)

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        table = PlaylistTable(
            id="playlist",
            playlist=self.player.playlist,
        )
        yield Container(
            ProgressDisplay(id="title"),
            Controls(), 
            table,
        )

        yield Footer()

    def action_toggle_play(self):
        if self.player.is_playing:
            self.player.pause()
            self.query_one("#play").label = "▶"
        else:
            self.player.play()
            self.query_one("#play").label = "▮▮"
        self.song_title = self.player.song.name

    def action_play_next(self):
        self.player.next()
        self.query_one("#play").label = "▮▮"
        self.song_title = self.player.song.name

    def action_play_prev(self):
        self.player.prev()
        self.query_one("#play").label = "▮▮"
        self.song_title = self.player.song.name

    async def action_quit(self):
        """Quit the app with necessary cleanup."""
        self.player.exit()
        self.exit()


def create_app_debug():
    player = Pod()
    playlist = player.generate_playlist(config.ASSETS_DIR)
    player.load(playlist)
    app = PyPodApp(player=player)
    return app


app = create_app_debug()


if __name__ == "__main__":
    app.run()