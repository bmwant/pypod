from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header as Header_
from textual.widgets._header import HeaderTitle
from textual.widgets import Button, Footer, Static, DataTable
from textual.reactive import watch


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
            print("play prev")
        elif button.id == "next":
            print("play next")


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

    def __init__(self, player, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = player


    def on_mount(self):
        table = self.query_one(DataTable)
        # ♫
        self.query_one(HeaderTitle).text = "🎵 PyPod"
        table.add_columns("#", "Name", "Duration")
        table.add_row("1", "Song", "3:02")

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
            self.player._is_playing = False
        else:
            self.player.play()
            self.query_one("#play").label = "pause"
            self.player._is_playing = True

    def action_play_next(self):
        self.player.next()

    def action_paly_prev(self):
        self.player.prev()


if __name__ == "__main__":
    from pypod import config
    from pypod.player import Pod
    filename = config.ASSETS_DIR / "rain_and_storm.wav"
    player = Pod()
    playlist = player.generate_playlist(filename)
    player.load(playlist)
    app = PyPodApp(player=player)
    app.run()