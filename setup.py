#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests',
    'click',
    'halo',
    'furl',
    'maya',
    'pyjq',
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Dileep Kishore",
    author_email='k.dileep1994@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    description="A python CLI to sync various datasources with Beeminder",
    entry_points={
        'console_scripts': [
            'beeminder_sync=beeminder_sync.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='beeminder_sync',
    name='beeminder_sync',
    packages=find_packages(include=['beeminder_sync']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/dileep-kishore/beeminder_sync',
    version='0.2.0',
    zip_safe=False,
)
