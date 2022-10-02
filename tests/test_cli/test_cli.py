import json
from json.decoder import JSONDecodeError

from pydoctest.validation import ResultType

from tests.test_suite import TestCase


class TestMain(TestCase):
    def test_verbosity_2_argument(self) -> None:
        out, err = self.execute_command('python3 -m pydoctest.main --config tests/test_cli/pydoctest.json --verbosity 2')
        assert 'example_class_cli.py::ExampleCLIClass::a' in out
        assert 'example_class_cli.py::b' in out
        assert 'Succeeded: 2, Failed: 0, Skipped: 0' in out
        assert len(err) == 0

    def test_verbosity_1_argument(self) -> None:
        out, err = self.execute_command('python3 -m pydoctest.main --config tests/test_cli/pydoctest.json --verbosity 1')
        assert 'function ExampleCLIClass' not in out
        assert 'Succeeded: 2, Failed: 0, Skipped: 0' in out
        assert len(err) == 0

    def test_reporter_json_argument(self) -> None:
        out, err = self.execute_command('python3 -m pydoctest.main --config tests/test_cli/pydoctest.json --reporter json')
        try:
            d = json.loads(out)
            assert d['result'] == ResultType.OK
        except JSONDecodeError as e:
            raise Exception("fail")

    def test_include_paths_argument(self) -> None:
        """
        Tests that the '--include-paths' argument is parsed.
        """
        out, err = self.execute_command('python3 -m pydoctest.main --config tests/test_cli/pydoctest.json --reporter json --include-paths "*.py"')
        output = json.loads(out)
        assert len(output['module_results']) == 4

    def test_include_exclude_paths_argument(self) -> None:
        """
        Tests that the '--exclude-paths' argument is parsed.
        """
        out, err = self.execute_command('python3 -m pydoctest.main --config tests/test_cli/pydoctest.json --reporter json --include-paths "*.py" --exclude-paths "**/excluded_class_cli.py"')
        output = json.loads(out)
        assert len(output['module_results']) == 3

    def test_include_exclude_classes_argument(self) -> None:
        """
        Tests that the '--exclude-classes' argument is parsed.
        """
        assert False

    def test_include_exclude_methods_argument(self) -> None:
        """
        Tests that the '--exclude-methods' argument is parsed.
        """
        assert False

    def test_include_exclude_functions_argument(self) -> None:
        """
        Tests that the '--exclude-functions' argument is parsed.
        """
        assert False
