# -*- coding: utf-8 -*-

"""Console script for beeminder_sync."""
import sys
import click


@click.group()
def main(args=None):
    """Console script for beeminder_sync."""
    click.echo("Replace this message by putting your code into "
               "beeminder_sync.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


@main.command()
@click.option("--username", "-u")
@click.option("--auth_token", "-p")
@click.argument("method")  # TODO: correspond to methods like `get_datapoints`
def beeminder():
    click.echo("Beeminder sub-command")
    return 0


if __name__ == "__main__":
    main()
