#!/usr/bin/env python

"""
    config.py
    ~~~~~~~~~

    Manages client configurations, e.g. OL authentication

    :copyright: (c) 2016 by Internet Archive.
    :license: see LICENSE for more details.
"""


import configparser
import os
import types
from collections import namedtuple

path = os.path.dirname(os.path.realpath(__file__))
approot = os.path.abspath(os.path.join(path, os.pardir))


def getdef(self, section, option, default_value):
    """A utility method which allows ConfigParser to be fill in defaults
    for missing fields and values.
    """
    try:
        return self.get(section, option)
    except:
        return default_value


Credentials = namedtuple('Credentials', ['access', 'secret'])


class Config:

    """Manages configurations for the Python OpenLibrary API Client"""

    DEFAULTS = {'s3': {'access': '', 'secret': ''}}

    @classmethod
    def get_config_parser(cls):
        config = configparser.ConfigParser()
        config.getdef = types.MethodType(getdef, config)
        return config

    def __init__(self, config_file=None):
        self.config = self.get_config_parser()
        self.config_file = config_file or self.default_config_file
        self.config.read(self.config_file)

        # make sure config exists, else make default config
        if not os.path.exists(self.config_file):
            self.create_default_config()
        else:
            self.get_config()

    @property
    def default_config_file(self):
        """If no config_file name is specified, returns a valid, canonical
        filepath where the config file can live.
        """
        config_dir = os.path.expanduser('~/.config')
        if not os.path.isdir(config_dir):
            return os.path.expanduser('~/.ol')
        return f'{config_dir}/ol.ini'

    def update(self, config):
        """Updates the config defaults by updating it with config dict values

        Args:
            config (dict)
        """
        config_parser = self.get_config_parser()

        _config = self.DEFAULTS
        _config.update(config)

        for section in _config:
            config_parser.add_section(section)
            for key, default in _config[section].items():
                config_parser.set(section, key, default)

        self.config = config_parser

        with open(self.config_file, 'w') as config_file:
            self.config.write(config_file)

    def create_default_config(self):
        """Creates and saves a new config file with the correct default values
        at the appropriate filepath.
        """
        for section in self.DEFAULTS:
            self.config.add_section(section)
            for key, default in self.DEFAULTS[section].items():
                self.config.set(section, key, default)

        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w') as fh:
                os.chmod(self.config_file, 0o600)
                self.config.write(fh)

    def _get_config(self):
        config = {}
        for section in self.DEFAULTS:
            config[section] = {}
            for key, default in self.DEFAULTS[section].items():
                config[section][key] = self.config.getdef(section, key, default)
        return config

    def get_config(self):
        """Loads an existing config .ini file from the disk and returns its
        contents as a dict
        """
        config = self._get_config()
        access = config['s3'].pop('access')
        secret = config['s3'].pop('secret')
        config['s3'] = Credentials(access, secret) if access and secret else None
        return config
