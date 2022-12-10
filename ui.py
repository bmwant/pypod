from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Button, Header, Footer, Static


class ProgressDisplay(Static):
    """A widget to display song's progress."""


class Controls(Static):
    """A buttons widget to control playback."""

    def compose(self) -> ComposeResult:
        """Create child widgets of a stopwatch."""
        yield Button("previous", id="prev", variant="success")
        yield Button("play/pause", id="play", variant="error")
        yield Button("next", id="next")

    def on_button_pressed(self, event: Button.Pressed):
        """Event handler called when a button is pressed."""
        if event.button.id == "play":
            print("play/pause")
        elif event.button.id == "prev":
            print("play prev")
        elif event.button.id == "next":
            print("play next")


class PyPodApp(App):
    """A Python terminal music player app."""

    CSS_PATH = "style.css"
    BINDINGS = [
        ("q", "quit", "quit"),
        ("p", "toggle_play", "play/pause"),
        ("n", "play_next", "next"),
        ("b", "play_prev", "back (previous)"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Container(
            ProgressDisplay("progress bar ... playing"),
            Controls(), 
        )

        yield Footer()

    def action_toggle_play(self):
        pass

    def action_play_next(self):
        print("Going to the next song")

    def action_paly_prev(self):
        print("Going to the previous song")


if __name__ == "__main__":
    app = PyPodApp()
    app.run()