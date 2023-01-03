from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Footer, Label
from textual.widgets._header import HeaderTitle

from pypod import config
from pypod.player import Pod
from pypod.ui import Controls, Header, PlaylistListView, ProgressDisplay


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
        song_index = self.player.playlist.position
        self.query_one("#playlist").set_index(song_index)

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
        progress: ProgressDisplay = self.query_one("#prog")
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
        progress: ProgressDisplay = self.query_one("#prog")
        self.player.next()
        self.query_one("#play").label = "▮▮"
        self.song_title = self.player.song.name
        progress.display_progress(self.player.song)

    def play_index(self, index: int):
        progress: ProgressDisplay = self.query_one("#prog")
        print(f"Want to play {index}")
        self.player.at_index(index)
        self.query_one("#play").label = "▮▮"
        self.song_title = self.player.song.name
        progress.display_progress(self.player.song)

    def action_play_prev(self):
        progress: ProgressDisplay = self.query_one("#prog")
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
