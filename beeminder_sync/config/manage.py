"""
    Module to manage configuration for the CLI
"""

from configparser import ConfigParser
import pathlib


REQ_SECTIONS = ['beeminder', 'database']
REQ_OPTIONS = {
    'beeminder': ['api', 'username', 'auth_token'],
    'database': ['url']
}


def read_config(config_path: pathlib.Path) -> ConfigParser:
    """
        Read and parse configuration file from path

        Parameters
        ----------
        config_path : pathlib.Path
            The path to the configuration file

        Returns
        -------
        ConfigParser
            The configuration file read as a ConfigParser instance
    """
    config = ConfigParser()
    with open(config_path, 'r') as fid:
        config.read_file(fid)
    return config


def verify_config(config_path: pathlib.Path) -> bool:
    """
        Verify whether configuration file is valid

        Parameters
        ----------
        config_path : pathlib.Path
            The path to the configuration file

        Returns
        -------
        bool
            True if the configuration file is valid otherwise False
    """
    config = ConfigParser()
    try:
        with open(config_path, 'r') as fid:
            config.read_file(fid)
        if any(not config.has_section(section) for section in REQ_SECTIONS):
            return False
        for section in REQ_OPTIONS:
            for option in REQ_OPTIONS['section']:
                if not config.has_option(section, option):
                    return False
        return True
    except:
        return False
