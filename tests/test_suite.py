import subprocess
import sys

from typing import Tuple
from pydoctest.configuration import Configuration
from pydoctest.main import PyDoctestService
from enum import Enum


class OS(Enum):
    WINDOWS = 0,
    LINUX = 1


def get_os() -> OS:
    if sys.platform == 'win32':
        return OS.WINDOWS
    else:
        return OS.LINUX


class TestPydoctest():
    """
    Uses the library to test its own docstrings - how awesome is that?
    """
    def test_pydoctest(self) -> None:
        config = Configuration.get_configuration_from_path("pydoctest.json")
        ds = PyDoctestService(config)
        result = ds.validate()
        counts = result.get_counts()
        assert counts.functions_failed == 0, "Run pydoctest on project and fix docstrings."
        # TODO: This doesn't artificially bring up our code-coverage, right?


class TestCase():
    def execute_command(self, command: str) -> Tuple[str, str]:
        try:
            if get_os() == OS.WINDOWS:
                # Figure out a more robust way to handle OS
                if command.startswith('python3 '):
                    command = command.replace('python3', 'py', 1)
                p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={'LC_ALL': 'C'})
            p.wait()
            stdout, stderr = p.communicate()
            return str(stdout.decode("utf-8")), str(stderr.decode("utf-8"))
        except Exception as e:
            return "", str(e)
