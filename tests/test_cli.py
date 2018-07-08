#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `beeminder_sync` package."""

from click.testing import CliRunner
import pytest

from beeminder_sync import cli


def test_cli_config():
    """ Test getting configuration value """
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['config', '-s', 'beeminder', '-o', 'api'], input='y')
    print(result.output)
    assert result.exit_code == 0
    assert "Initialization successful" in result.output
    assert "beeminder.api" in result.output


def test_content():
    """Sample pytest test function with the pytest fixture as an argument."""
    pass


def test_main_cli():
    """ Test the main cli """
    runner = CliRunner()
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0
    assert "Main entry point to beeminder_sync" in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "Show this message and exit." in help_result.output
