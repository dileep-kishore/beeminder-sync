"""
    The main beeminder-sync class
"""

import pathlib
import os
import click

from .config import read_config, verify_config


class BeeSync:
    """
        The main class for the package
        Stores configuration information

        Parameters
        ----------
        base_dir : pathlib.Path
            The default path to the settings directory
        config_path : pathlib.Path
            The default path to the configuration file

        Attributes
        ----------
        base_dir : pathlib.Path
        config_path : pathlib.Path
    """
    base_dir = pathlib.Path(click.get_app_dir('beeminder_sync'))
    config_path = base_dir / "config.ini"

    def __init__(self, base_dir: pathlib.Path, config_path: pathlib.Path) -> None:
        self.base_dir = base_dir
        if not self.base_dir.is_dir():
            os.mkdir(self.base_dir)
            # TODO: Also need to reinitialize the other files that are supposed to be here
        if self._verify_config(config_path):
            raise ValueError("The configuration file provided is not valid")
        self.config_path = config_path
        # TODO: Check if there's a config file in base_dir
        # If contents of base_dir/config.ini and config_path are the same no need to overwrite

    def _verify_config(self, config_path: pathlib.Path) -> bool:
        """
            Verify whether the configuration file is valid

            Paramters
            ---------
            config_path : pathlib.Path
                The path to the configuration file

            Returns
            -------
            bool
                True if the config file passed in is valid otherwise False
        """
        validity = False
        if config_path.is_file():
            if verify_config(config_path):
                validity = True
        else:
            raise FileNotFoundError(f"The configuration file: {config_path} does not exist")
        return validity

    # TODO: When given a new config.ini copy this to base_dir and make backup of old
