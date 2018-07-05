"""
    Console script for beeminder_sync.
"""

import sys

import click

from . import BeeSync, BEESYNC_DIR, BEESYNC_CONFIG
from .beeminder import Beeminder


# TODO: Anticipate for `envvar` as well.
# What takes higher priority when both `envvar` and `default` are present
BEESYNC_DIR = str(BEESYNC_DIR)
BEESYNC_CONFIG = str(BEESYNC_CONFIG)


@click.group()
@click.option(
    "--basedir",
    "-d",
    envvar="BEESYNC_DIR",
    default=BEESYNC_DIR,
    type=click.Path(),
    help="The path to the base application directory"
)
@click.option(
    "--config",
    "-c",
    default=BEESYNC_CONFIG,
    type=click.Path(exists=True),
    help="The path to the configuration file"
)
@click.pass_context
def main(ctx, basedir, config):
    """ Main entry point to beeminder_sync """
    ctx.obj['CONFIG'] = BeeSync(basedir, config)
    return None


@main.command()
@click.option("--section", "-s", help="Configuration section header")
@click.option("--option", "-o", help="Option name under section")
@click.argument("VALUE", default="")
@click.pass_context
def config(ctx, section, option, value):
    """ Get and set configuration options """
    spinner_settings = dict(color='blue', spinner="dots")
    beesync = ctx.obj['CONFIG']
    if value:
        spinner_settings['text'] = "Updating configuration...",
        beesync.set_spinner(spinner_settings)
        conf_val = beesync.update(section, option, value)
    else:
        spinner_settings['text'] = "Getting configuration...",
        beesync.set_spinner(spinner_settings)
        conf_val = beesync.get(section, option)
    return conf_val


@main.command()
@click.option("--username", "-u")
@click.option("--authtoken", "-p")
@click.argument("--method", "-m")  # TODO: correspond to methods like `get_datapoints`
@click.pass_context
def beeminder(ctx, username, authtoken, method):
    """ Access the beeminder interface """
    beesync = ctx.obj['CONFIG']
    return 0


if __name__ == "__main__":
    main(obj={})
