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
@click.option("--method", "-m", default=None, help="Either 'GET' or 'POST'")
@click.option("--goal", "-g", default=None, help="Beeminder goal to use")
@click.option("--value", "-v", default=None, type=click.INT, help="Value to add to the new data point (POST only)")
@click.option("--comment", "-c", default="", help="Comment to add to the nww data point (POST only)")
@click.option("--timestamp", "-t", default=None, help="Timestamp of the new data point (POST only)")
@click.pass_context
def beeminder(ctx, method, goal, value, comment, timestamp):
    """ Access the beeminder interface """
    beesync = ctx.obj['CONFIG']
    bee = Beeminder.from_config(beesync)
    if not method:
        response = bee.user_details
    elif not goal:
        response = {"goals": bee.goals}
    elif method == 'GET':
        response = bee.get_datapoints(goal)
    elif method == 'POST':
        if timestamp:
            response = bee.create_datapoint(goal, value, comment, timestamp)
        else:
            response = bee.create_datapoint(goal, value, comment)
    else:
        bee.fail(f"Unsupported method {method}. Valid options: ['GET', 'POST']")
    click.secho('\n' + '=' * 36 + "[OUTPUT]" + '=' * 36, fg="white")
    click.secho(json.dumps(response, indent=2, sort_keys=True))
    return 0


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
