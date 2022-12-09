import sys
from typing import Optional

import click
from rich.console import Console

from pypod.player import Pod

console = Console(highlight=False)
player = Pod()

@click.group(invoke_without_command=True)
@click.version_option(message="pypod, version %(version)s")
@click.argument("filepath", metavar="path")
def cli(filepath):
    playlist = player.generate_playlist("assets")
    player.load(playlist)
    player.play()


if __name__ == "__main__":
    cli()