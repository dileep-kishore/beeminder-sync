"""
    The main beeminder-sync class
"""

from configparser import ConfigParser
import os
import pathlib
import shutil
import sys
from typing import Dict, Optional

import click
from halo import Halo

from .config import read_config, verify_config, write_config


class BeeSync:
    """
        The main class for the package
        Stores configuration information

        Parameters
        ----------
        base_dir : str
            The default path to the settings directory
        config_path : str
            The default path to the configuration file
        spinner : bool, optinal
            If True then `Halo` spinners are enabled
            Default value is True

        Attributes
        ----------
        base_dir : pathlib.Path
        config_path : pathlib.Path
        config : ConfigParser
            The configuration object
    """
    _config_template_path = pathlib.Path(__file__).parent / "config/config_template.ini"

    def __init__(self, base_dir: str, config_path: str, spinner: bool = True) -> None:
        self._spinner = Halo(
            text="Initializing application...",
            color="green",
            spinner="dots",
            enabled=spinner
        )
        self._spinner.start()
        self.base_dir = pathlib.Path(base_dir)
        if not self.base_dir.is_dir():
            self._spinner.text = "Creating base directory..."
            os.mkdir(self.base_dir)
            # TODO: Also need to reinitialize the other files that are supposed to be here like db
        if config_path:
            config_file = pathlib.Path(config_path)
        else:
            config_file = self.base_dir / "config.ini"
        if not config_file.exists():
            new_config_path = self.base_dir / "config.ini"
            self._spinner.fail("Could not find a configuration file.")
            if answer := click.confirm(
                f"Create new one at {new_config_path}?", default=False, abort=True
            ):
                self._spinner.text = "Creating new configuration file template"
                self._create_config(new_config_path)
                self._spinner.succeed("Configuration template created. Please fill in the required options")
                sys.exit()
        if self._verify_config(config_file):
            self._spinner.fail("The configuration file provided is not valid")
        self.config_path = config_file
        self.config = self._read_replace_config()
        self._spinner.succeed(text="Initialization successful")

    def _create_config(self, config_path: pathlib.Path) -> None:
        """
            Create a config file at destination using the template

            Parameters
            ----------
            config_path : pathlib.Path

            Returns
            -------
            None
        """
        shutil.copy(self._config_template_path, config_path)
        os.chmod(config_path, 0o600)

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
        if base_config != self.config_path:
            if base_config.exists():
                if answer := click.confirm(
                    "A configuration file already exists at {self.base_dir}. Replace?",
                    default=False,
                    abort=True,
                ):
                    shutil.copy(base_config, self.base_dir / "config.ini.bak")
                    shutil.copy(self.config_path, base_config)
                    os.chmod(base_config, 0o600)
            else:
                shutil.copy(self.config_path, base_config)
                os.chmod(base_config, 0o600)
        return read_config(base_config)

    def update(self, section: str, option: str, value: str, silent: bool = False) -> str:
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
            silent : bool
                Flag to silence printing to console

            Returns
            -------
            str
                Returns the value that was updated
        """
        if not silent:
            self._spinner.color = "blue"
            self._spinner.text = "Updating configuration..."
            self._spinner.start()
        if section in self.config.sections() and option in self.config.options(section):
            if not silent:
                self._spinner.info("Overwriting current value")
        self.config.set(section, option, value=value)
        write_config(self.config_path, self.config)
        if not silent:
            self._spinner.succeed(text="Update successful")
        return self.config.get(section, option)

    def get(self, section: str, option: str, silent: bool = False) -> Optional[str]:
        """
            Get a particular value from the configuration file

            Parameters
            ----------
            section : str
                Section header
            option : str
                Option name
            silent : bool
                Flag to silence printing to console

            Returns
            -------
            str
                Returns the option value for the desired section and optio
        """
        if not silent:
            self._spinner.color = "blue"
            self._spinner.text = "Getting configuration..."
            self._spinner.start()
        if section in self.config.sections() and option in self.config.options(section):
            val = self.config.get(section, option)
            if not silent:
                self._spinner.succeed(text=f"{section}.{option}: {val}")
            return val
        else:
            self._spinner.fail("Incorrect section or option value entered")
            click.secho("Possible values are:")
            for section in self.config.sections():
                click.secho(f"section: {section}. options: {self.config.options(section)}")

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

    def fail(self, text: str) -> None:
        """
            Creates a failure message using the `Halo` spinner object

            Parameters
            ----------
            text : str

            Returns
            -------
            None
        """
        self._spinner.fail(text)
