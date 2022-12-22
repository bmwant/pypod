from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header as Header_
from textual.widgets._header import HeaderTitle
from textual.widgets import Button, Footer, Static, Label
from textual.reactive import reactive

from pypod import config
from pypod.ui import ProgressDisplay, PlaylistListView
from pypod.utils import sec_to_time
from pypod.player import Pod


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

    song_title = reactive("♫ not playing ♫")

    def __init__(self, player: Pod, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = player

    def on_mount(self):
        # ♫
        self.query_one(HeaderTitle).text = "🎵 PyPod"
        self.set_interval(0.5, self.change_song)

    def watch_song_title(self, title: str):
        if not title.startswith("♫"):
            title = f"♫ {title} ..."
        self.query_one("#title").update(title)

    def change_song(self):
        # TODO: check the end of playlist
        if self.player.auto_finish.is_set():
            self.action_play_next()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        table = PlaylistListView(
            id="playlist",
            playlist=self.player.playlist,
        )
        yield Container(
            Label(id="title"),
            ProgressDisplay(id="prog"),
            Controls(),
            table,
        )

        yield Footer()

    def action_toggle_play(self):
        progress : ProgressDisplay = self.query_one("#prog")
        if self.player.is_playing:
            progress.pause()
            self.player.pause()
            self.query_one("#play").label = "▶"
        else:
            self.player.play()
            self.query_one("#play").label = "▮▮"
            if progress.timer is None:
                progress.display_progress(self.player.song)
            else:
                progress.resume()
        self.song_title = self.player.song.name

    def action_play_next(self):
        progress : ProgressDisplay = self.query_one("#prog")
        self.player.next()
        self.query_one("#play").label = "▮▮"
        self.song_title = self.player.song.name
        progress.display_progress(self.player.song)

    def action_play_prev(self):
        progress : ProgressDisplay = self.query_one("#prog")
        self.player.prev()
        self.query_one("#play").label = "▮▮"
        self.song_title = self.player.song.name
        progress.display_progress(self.player.song)

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
