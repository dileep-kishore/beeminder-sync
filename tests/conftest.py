"""
    Common configuration for all the tests
"""

import json
import pathlib
import pytest


BASE_DIR = pathlib.Path.cwd()


@pytest.fixture(scope="module")
def config():
    """ Configuration settings for all the apis """
    fpath = BASE_DIR / "config.json"
    with open(fpath, 'r') as fid:
        data = json.load(fid)
    return data


@pytest.fixture
def beeminder_config(config):
    data = config['beeminder']
    data['required_fields'] = ["api", "username", "auth_token"]
    return data
