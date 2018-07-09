"""
    Common configuration for all the tests
"""

from configparser import ConfigParser
import pathlib
import shutil

import pytest

from beeminder_sync.beeminder import Beeminder
from beeminder_sync import BeeSync


BASE_DIR = pathlib.Path.cwd()


# NOTE: We cannot test the creation a config because that requires a user input
@pytest.fixture(scope="module")
def config_paths(tmpdir_factory):
    """ The configuration for the application data """
    base_factory = tmpdir_factory.mktemp("beeminder_sync")
    base_path = pathlib.Path(str(base_factory))
    config_path = base_path / "config.ini"
    shutil.copy(BeeSync._config_template_path, config_path)
    return base_path, config_path


@pytest.fixture(scope="module")
def config():
    """ Configuration settings for all the apis """
    fpath = BASE_DIR / "config.ini"
    config = ConfigParser()
    with open(fpath, 'r') as fid:
        config.read_file(fid)
    return config


@pytest.fixture
def beeminder_config(config):
    """ The configuration for the beeminder api """
    assert 'beeminder' in config.keys()
    data = dict(config['beeminder'])
    data['required_fields'] = ["api", "username", "auth_token"]
    return data


@pytest.fixture
def beeminder_interface(beeminder_config):
    """ The `Beeminder` instance to communicate with the api """
    base_url = beeminder_config["api"]
    username = beeminder_config["username"]
    auth_token = beeminder_config["auth_token"]
    interface = Beeminder(base_url, username, auth_token)
    return interface
