"""
    Console script for beeminder_sync.
"""

import json
import os
import sys

import click

from . import BeeSync, BASE_DIR
from .beeminder import Beeminder


@click.group()
@click.option(
    "--basedir",
    "-d",
    default=str(BASE_DIR),
    type=click.Path(),
    help="The path to the base application directory"
)
@click.option(
    "--config",
    "-c",
    default=None,
    type=click.Path(),
    help="The path to the configuration file"
)
@click.pass_context
def cli(ctx, basedir, config):
    """ Main entry point to beeminder_sync """
    ctx.obj['CONFIG'] = BeeSync(basedir, config)
    return None


@cli.command()
@click.option("--section", "-s", help="Configuration section header")
@click.option("--option", "-o", help="Option name under section")
@click.argument("VALUE", default="")
@click.pass_context
def config(ctx, section, option, value):
    """ Get and set configuration options """
    beesync = ctx.obj['CONFIG']
    if value:
        conf_val = beesync.update(section, option, value)
    else:
        conf_val = beesync.get(section, option)
    return conf_val


@cli.command()
@click.option("--method", "-m")  # TODO: methods like `get_datapoints` -> use `GET` or `POST` instead
@click.argument("method_args", nargs=-1)
@click.pass_context
def beeminder(ctx, method, method_args):
    """ Access the beeminder interface """
    beesync = ctx.obj['CONFIG']
    bee = Beeminder.from_config(beesync)
    if method == 'GET':
        response = bee.get_datapoints(method_args[0])
    elif method == 'POST':
        response = bee.create_datapoint(method_args[0], method_args[1])
    else:
        bee.fail(f"Unsupported method {method}. Valid options: ['GET', 'POST']")
    click.secho(json.dumps(response, indent=2, sort_keys=True))
    return 0


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
