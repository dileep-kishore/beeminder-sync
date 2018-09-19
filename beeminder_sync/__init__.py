"""
    Top-level package for Beeminder Sync.
"""

__author__ = """Dileep Kishore"""
__email__ = 'k.dileep1994@gmail.com'
__version__ = '0.2.1'

import pathlib
import os

import click

from.beeminder_sync import BeeSync


BEESYNC_DIR = pathlib.Path(click.get_app_dir('beeminder_sync'))
ENV_PATH = os.environ.get('BEESYNC_DIR')
BASE_DIR = pathlib.Path(ENV_PATH) if ENV_PATH else BEESYNC_DIR
if not BASE_DIR.exists():
    BASE_DIR.mkdir(parents=True)
