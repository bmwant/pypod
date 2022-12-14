from textual.widgets import ListView, ListItem, Static, Label


class PlaylistListView(Static):
    def __init__(self, playlist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.playlist = playlist

    def on_mount(self):
        pass

    def compose(self):
        yield ListView(
            ListItem(Label("One")),
            ListItem(Label("Two")),
            ListItem(Label("Three")),
            ListItem(Label("Four")),
            ListItem(Label("Five")),
            ListItem(Label("Six")),
            ListItem(Label("Seven")),
            ListItem(Label("Eight")),
            ListItem(Label("Second to last one")),
            ListItem(Label("Last one")),
        )