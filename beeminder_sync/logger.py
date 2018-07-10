"""
    Module to create and define the logger object and settings
"""


import logging

log = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
)
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.DEBUG)
