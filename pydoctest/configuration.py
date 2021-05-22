import os
import sys
import json
from typing import Any, Dict, List, Optional
from enum import IntEnum

from pydoctest.logging import log
from pydoctest.parsers.parser import Parser
from pydoctest.parsers.google_parser import GoogleParser
from pydoctest.parsers.numpy_parser import NumpyParser


class Verbosity(IntEnum):
    QUIET = 0
    SHOW_FAILED = 1
    SHOW_ALL = 2


PARSERS = {
    'google': GoogleParser,
    # 'numpy': NumpyParser
    # To be populated
}


class Configuration():
    def __init__(self) -> None:
        self.working_directory: str = ""
        # Empty include_paths assumes all directories in current directory
        self.include_paths: List[str] = []
        self.exclude_paths: List[str] = []

        # Throw an error if function does not have a docstring
        self.fail_on_missing_docstring = False

        # Doctype parser to use, defaults to Google
        self.parser = "google"

        # Verbosity of reporter, currently only used by text-reporter
        self.verbosity = Verbosity.SHOW_FAILED

    @staticmethod
    def get_default_configuration() -> 'Configuration':
        log("Using default configuration")
        return Configuration()

    @staticmethod
    def get_configuration_from_path(config_path: str) -> 'Configuration':
        config_path_absolute = os.path.abspath(config_path)
        log(f"Using configuration from path: {config_path_absolute}")

        with open(config_path_absolute, 'r') as f:
            config_dict = json.load(f)
            config = Configuration.from_dict(config_dict)
            config.working_directory = os.path.dirname(config_path_absolute)
            return config

    @staticmethod
    def from_dict(x: Dict[str, Any]) -> 'Configuration':
        obj = Configuration()
        for key, value in x.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
            else:
                print(f'Unknown configuration parameter: {key}')
                sys.exit(1)
        return obj

    def validate(self) -> None:
        self.get_parser()

    def get_parser(self) -> Parser:
        if self.parser in PARSERS.keys():
            return PARSERS[self.parser]()
        else:
            print(f"Unknown parser: {self.parser}. Please use one of the following: {', '.join(PARSERS.keys())}")
            sys.exit(1)
