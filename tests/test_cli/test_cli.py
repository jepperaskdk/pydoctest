import pytest
import json
from json.decoder import JSONDecodeError
import sys
from io import StringIO


from pydoctest.reporters.text_reporter import TextReporter
from pydoctest.reporters.json_reporter import JSONReporter
from pydoctest.configuration import Configuration
from pydoctest.validation import ResultType, validate_class, validate_function
from pydoctest.main import PyDoctestService, get_configuration, get_reporter, main

from tests.test_suite import TestCase


class TestMain(TestCase):
    def test_verbosity_2_argument(self) -> None:
        out, err = self.execute_command('python3 -m pydoctest.main --config tests/test_cli/pydoctest.json --verbosity 2')
        assert 'function ExampleCLIClass' in out
        assert 'Succeeded: 1, Failed: 0, Skipped: 0' in out
        assert len(err) == 0

    def test_verbosity_1_argument(self) -> None:
        out, err = self.execute_command('python3 -m pydoctest.main --config tests/test_cli/pydoctest.json --verbosity 1')
        assert 'function ExampleCLIClass' not in out
        assert 'Succeeded: 1, Failed: 0, Skipped: 0' in out
        assert len(err) == 0

    def test_reporter_json_argument(self) -> None:
        out, err = self.execute_command('python3 -m pydoctest.main --config tests/test_cli/pydoctest.json --reporter json')
        try:
            d = json.loads(out)
            assert d['result'] == ResultType.OK
        except JSONDecodeError as e:
            raise Exception("fail")
