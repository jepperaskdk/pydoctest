import os
import sys
import json
from typing import Any, Dict, List, Optional
from enum import IntEnum

from pydoctest.logging import log
from pydoctest.parsers.parser import Parser
from pydoctest.parsers.google_parser import GoogleParser
from pydoctest.parsers.numpy_parser import NumpyParser
from pydoctest.parsers.sphinx_parser import SphinxParser


class Verbosity(IntEnum):
    QUIET = 0
    SHOW_FAILED = 1
    SHOW_ALL = 2


PARSERS = {
    'google': GoogleParser,
    'numpy': NumpyParser,
    'sphinx': SphinxParser
}


class Configuration():
    def __init__(self) -> None:
        """Configuration object to be used while running pydoctest.
        The properties here can be overridden with a pydoctest.json config file.
        """
        self.working_directory: str = ""

        # List of patterns to discover modules by
        self.include_paths: List[str] = [ '**/*.py' ]

        # List of patterns to exclude modules discovered by
        self.exclude_paths: List[str] = [ '**/__init__.py', '**/setup.py' ]

        # Doctype parser to use, defaults to Google
        self.parser = "google"

        # Verbosity of reporter, currently only used by text-reporter
        self.verbosity = Verbosity.SHOW_FAILED

        # Throw an error if function does not have a docstring
        self.fail_on_missing_docstring = False

        # Throw an error if function does not have a summary
        self.fail_on_missing_summary = False

        # Throw an error if 'raises' section does not list all exceptions
        self.fail_on_raises_section = True

    @staticmethod
    def get_default_configuration(root_dir: Optional[str] = None) -> 'Configuration':
        """Returns a configuration with default values.

        Args:
            root_dir (Optional[str]): Directory to use as root.

        Returns:
            'Configuration': A default configuration.
        """
        log("Using default configuration")
        config = Configuration()
        if root_dir:
            config.working_directory = root_dir
        return config

    @staticmethod
    def get_configuration_from_path(config_path: str) -> 'Configuration':
        """Returns a configuration, loaded from the pydoctest.json provided.

        Args:
            config_path (str): The path to a config file.

        Returns:
            'Configuration': A configuration loaded with values from provided path.
        """
        config_path_absolute = os.path.abspath(config_path)
        log(f"Using configuration from path: {config_path_absolute}")

        with open(config_path_absolute, 'r') as f:
            config_dict = json.load(f)
            config = Configuration.from_dict(config_dict)
            config.working_directory = os.path.dirname(config_path_absolute)
            return config

    @staticmethod
    def from_dict(x: Dict[str, Any]) -> 'Configuration':
        """Given a dictionary, returns a Configuration object.

        Args:
            x (Dict[str, Any]): The dictionary to load the configuration values from.

        Returns:
            'Configuration': A configuration loaded with values from the dictionary.
        """
        obj = Configuration()
        for key, value in x.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
            else:
                raise Exception(f'Unknown configuration parameter: {key}')
        return obj

    def get_parser(self) -> Parser:
        """Checks if the desired Parser exists and returns it.

        Raises:
            Exception: If parser from Configuration doesn't exist.

        Returns:
            Parser: A supported Parser.
        """
        if self.parser in PARSERS.keys():
            return PARSERS[self.parser]()
        else:
            raise Exception(f"Unknown parser: {self.parser}. Please use one of the following: {', '.join(PARSERS.keys())}")
