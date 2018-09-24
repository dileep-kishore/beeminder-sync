# Beeminder Sync

[![Documentation Status](https://img.shields.io/readthedocs/beeminder-sync.svg?style=for-the-badge)](https://beeminder-sync.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://img.shields.io/travis/dileep-kishore/beeminder-sync.svg?style=for-the-badge)](https://travis-ci.org/dileep-kishore/beeminder-sync)
[![codecov](https://img.shields.io/codecov/c/github/dileep-kishore/beeminder-sync.svg?style=for-the-badge)](https://codecov.io/gh/dileep-kishore/beeminder-sync)
[![Requirements Status](https://img.shields.io/requires/github/dileep-kishore/beeminder-sync.svg?style=for-the-badge)](https://requires.io/github/dileep-kishore/beeminder-sync/requirements/?branch=master)
[![pypi](https://img.shields.io/pypi/v/beeminder_sync.svg?style=for-the-badge)](https://pypi.python.org/pypi/beeminder_sync)

A `Python` CLI to sync various data sources with [Beeminder](https://github.com/dileep-kishore/beeminder-sync)

  - Free software: MIT license
  - Documentation: <https://beeminder-sync.readthedocs.io>.

## Work in progress

This is a 'work in progress' use with caution

### Demo

![Demo](assets/demo.gif)

## Features

- Use the Beeminder API from the comfort of your terminal!
- Cool interactive CLI created using [`click`](http://click.pocoo.org/6/) and [`halo`](https://github.com/ManrajGrover/halo)
- Python package can also be used directly for programmatic access
- Filter and query output using the `--query` option and [`jq`](https://stedolan.github.io/jq/) syntax
- Display output as a `table` or in `json` format

## Coming Soon

- Integrations with various source APIs like `wakatime`, `ticktick` and `google-fit`
- Ability to run as a background service
- Save data to a local `sqlite` database

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
