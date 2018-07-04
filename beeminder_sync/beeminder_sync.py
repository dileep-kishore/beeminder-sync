"""
    The main beeminder-sync class
"""

from configparser import ConfigParser
import os
import pathlib
import shutil
from typing import Dict

import click
from halo import Halo

from .config import read_config, verify_config, write_config


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
        self._spinner = Halo(text="Initializing application...", color='green', spinner="dots")
        self._spinner.start()
        if not self.base_dir.is_dir():
            os.mkdir(self.base_dir)
            # TODO: Also need to reinitialize the other files that are supposed to be here
        if self._verify_config(config_path):
            self._spinner.fail("The configuration file provided is not valid")
            raise ValueError("The configuration file provided is not valid")
        self.config_path = config_path
        self.config = self._read_replace_config()
        self._spinner.succeed(text="Initialization successful")

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
            self._spinner.fail(f"The configuration file: {config_path} does not exist")
            raise FileNotFoundError(f"The configuration file: {config_path} does not exist")
        return validity

    def _read_replace_config(self) -> ConfigParser:
        """
            Determines whether to configuration file is to be replaced or not
            Also returns the appropriate `ConfigParser` instance

            Returns
            -------
            ConfigParser
        """
        base_config = self.base_dir / "config.ini"
        if base_config != self.config_path and base_config.exists():
            answer = click.confirm(
                "A configuration file already exists at {self.base_dir}. Replace?",
                default=False,
                abort=True,
            )
            if answer:
                shutil.copy(base_config, self.base_dir / "config.ini.bak")
                shutil.copy(self.config_path, base_config)
        elif base_config != self.config_path:
            shutil.copy(self.config_path, base_config)
        return read_config(base_config)

    def update(self, section: str, option: str, value: str):
        """
            Update a particular value in the configuration file

            Parameters
            ----------
            section : str
                Section header
            option : str
                Option name
            value : str
                Value to be added

            Returns
            -------
            str
                Returns the value that was updated
        """
        self._spinner.start()
        self.config.set(section, option, value=value)
        write_config(self.config_path, self.config)
        self._spinner.succeed(text="Update successful")
        return self.config.get(section, option)

    def get(self, section: str, option: str):
        """
            Get a particular value from the configuration file

            Parameters
            ----------
            section : str
                Section header
            option : str
                Option name

            Returns
            -------
            str
                Returns the option value for the desired section and optio
        """
        self._spinner.start()
        if section in self.config.sections() and option in self.config.options(section):
            val = self.config.get(section, option)
            self._spinner.succeed(text=val)
            return val
        else:
            self._spinner.fail("Incorrect section or option value entered")
            raise ValueError("Incorrect section or option value entered")

    def set_spinner(self, settings: Dict[str, str]) -> Halo:
        """
            Update settings for spinner instance

            Parameters
            ----------
            settings : Dict[str, str]
                A dictionary containing the updated settings for the spinner

            Returns
            -------
            Halo
                Returns the spinner instance
        """
        for key in settings:
            if key in ['spinner', 'text', 'color']:
                setattr(self._spinner, key, settings[key])
            else:
                raise KeyError("Unsupported attribute supplied to spinner instance")
        return self._spinner
