from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header as Header_
from textual.widgets._header import HeaderTitle
from textual.widgets import Button, Footer, Static, DataTable


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


class PyPodApp(App):
    """A Python terminal music player app."""

    CSS_PATH = "style.css"
    BINDINGS = [
        ("q", "quit", "quit"),
        ("p", "toggle_play", "play/pause"),
        ("n", "play_next", "next"),
        ("b", "play_prev", "back (previous)"),
    ]

    def __init__(self, player: Pod, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = player


    def on_mount(self):
        table = self.query_one(DataTable)
        # ♫
        self.query_one(HeaderTitle).text = "🎵 PyPod"
        table.add_columns("#", "Name", "Duration")
        for i, s in enumerate(self.player.playlist, start=1):
            table.add_row(f"{i}", f"{s}", f"{s.duration}")

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Container(
            ProgressDisplay("progress bar ... playing"),
            Controls(), 
            DataTable(id="playlist"),
        )

        yield Footer()

    def action_toggle_play(self):
        if self.player.is_playing:
            self.player.pause()
            self.query_one("#play").label = "▶"
        else:
            self.player.play()
            self.query_one("#play").label = "pause"

    def action_play_next(self):
        self.player.next()
        self.query_one("#play").label = "▮▮"

    def action_play_prev(self):
        self.player.prev()
        self.query_one("#play").label = "▮▮"

    async def action_quit(self):
        """Quit the app with necessary cleanup."""
        self.player.exit()
        self.exit()


def create_app_debug():
    filename = config.ASSETS_DIR / "rain_and_storm.wav"
    player = Pod()
    playlist = player.generate_playlist(filename)
    player.load(playlist)
    app = PyPodApp(player=player)
    return app


app = create_app_debug()


if __name__ == "__main__":
    app.run()