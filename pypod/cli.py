import sys
from typing import Optional

import click
from rich.console import Console



console = Console(highlight=False)


@click.version_option(message="pypod, version %(version)s")
@click.argument("path", metavar="filepath")
def cli(filepath):
    print("This is desired path", filepath)


if __name__ == "__main__":
    cli()