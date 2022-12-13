from typing import Optional

import click
from rich.console import Console

from pypod import config
from pypod.player import Pod
from pypod.app import PyPodApp

console = Console(highlight=False)


@click.group(invoke_without_command=True)
@click.version_option(message="pypod, version %(version)s")
@click.argument("filepath", metavar="path")
def cli(filepath):
    player = Pod()
    playlist = player.generate_playlist(filepath)
    player.load(playlist)
    app = PyPodApp(player=player)
    app.run()
    

if __name__ == "__main__":
    cli()