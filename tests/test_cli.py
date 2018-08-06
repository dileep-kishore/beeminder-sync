"""Tests for `beeminder_sync` package."""

from click.testing import CliRunner
import pytest

from beeminder_sync import cli


def test_cli_config(tmpdir):
    """ Test getting configuration value """
    base_dir = tmpdir.mkdir("beeminder_sync")
    runner = CliRunner()
    result = runner.invoke(
        cli.cli,
        [
            '-d', base_dir,
            'config', '-s', 'beeminder', '-o', 'api'
        ],
        input='y',
        obj={}
    )
    if result.exit_code == 1:
        result = runner.invoke(
            cli.cli,
            [
                '-d', base_dir,
                'config', '-s', 'beeminder', '-o', 'api'
            ],
            input='y',
            obj={}
        )
    assert result.exit_code == 0
    # TODO: Find a way to assert the stdout


def test_main_cli():
    """ Test the main cli """
    runner = CliRunner()
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0
    assert "Main entry point to beeminder_sync" in result.output
    help_result = runner.invoke(cli.cli, ["--help"])
    assert help_result.exit_code == 0
    assert "Show this message and exit." in help_result.output
