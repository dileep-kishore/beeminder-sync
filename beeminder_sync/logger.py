"""
    Module to create and define the logger object and settings
"""


import logging
import os

from . import BEESYNC_DIR

# TODO: Make this more modular (just importable) Maybe put this in beeminder_sync
ENV_PATH = os.environ.get('BEESYNC_DIR')
BASE_DIR = ENV_PATH if ENV_PATH else str(BEESYNC_DIR)


log = logging.getLogger('beeminder_sync')
handler = logging.FileHandler(BASE_DIR)
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
)
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.DEBUG)
