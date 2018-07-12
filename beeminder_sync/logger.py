"""
    Module to create and define the logger object and settings
"""


import logging
import pathlib
import os

from . import BASE_DIR


log = logging.getLogger('beeminder_sync')
handler = logging.FileHandler(BASE_DIR / "log.txt")
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
)
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.DEBUG)
