import sys

# These two imports are necessary for test_get_type_from_module_bfs
import pydoctest
from pydoctest.configuration import Configuration

from pydoctest.validation import ResultType, validate_class, validate_function
from pydoctest.main import PyDoctestService
from pydoctest.utilities import get_exceptions_raised, get_type_from_module, is_excluded_path, parse_cli_list, is_excluded_function, is_excluded_class
import tests.test_utilities.example_class


THIS = sys.modules[__name__]


class DataObject():
    pass


class TestUtilities():
    def test_get_type_from_module_locate(self) -> None:
        result = get_type_from_module('int', THIS)
        assert result.type == int
        assert result.method == 'locate'

        result = get_type_from_module('float', THIS)
        assert result.type == float
        assert result.method == 'locate'

    def test_get_type_from_module_eval(self) -> None:
        result = get_type_from_module('DataObject', THIS)
        assert result.type == DataObject
        assert result.method == 'eval'

    def test_get_type_from_module_bfs(self) -> None:
        # Parser is not found in this module, but it is imported by Configuration which we do import.
        result = get_type_from_module('Parser', THIS)
        assert result.type == pydoctest.parsers.parser.Parser
        assert result.method == 'deque'

    def test_get_type_from_module_raises(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_utilities.example_class.ExampleClass.func_raises, config, tests.test_utilities.example_class)
        assert "Unable to parse docstring: Unknown type 'DEFINITELYNOTACLASS' in 'a (DEFINITELYNOTACLASS): [description]'" in result.fail_reason

    def test_get_exceptions_raised(self) -> None:
        actual_exceptions = get_exceptions_raised(tests.test_utilities.example_class.ExampleClass.func_with_raise, tests.test_utilities.example_class)
        expected_exceptions = [ 'RuntimeError', 'ValueError', 'IndexError' ]
        assert len(expected_exceptions) == len(actual_exceptions)

        intersection = set(expected_exceptions) - set(actual_exceptions)
        assert len(intersection) == 0

    def test_get_exceptions_empty(self) -> None:
        actual_exceptions = get_exceptions_raised(tests.test_utilities.example_class.ExampleClass.func_locate, tests.test_utilities.example_class)
        assert len(actual_exceptions) == 0

    def test_global_func_raises(self) -> None:
        actual_exceptions = get_exceptions_raised(tests.test_utilities.example_class.global_func_raises, tests.test_utilities.example_class)
        expected_exceptions = [ 'RuntimeError', 'ValueError', 'IndexError' ]
        assert len(expected_exceptions) == len(actual_exceptions)

        intersection = set(expected_exceptions) - set(actual_exceptions)
        assert len(intersection) == 0

    def test_parse_cli_list(self) -> None:
        """
        Tests the parse_cli_list function for various inputs.
        """
        assert ["a.py"] == parse_cli_list("a.py")
        assert ["a.py"] == parse_cli_list("a.py,")
        assert ["a.py"] == parse_cli_list(",a.py,")
        assert ["a.py", "b.py"] == parse_cli_list("a.py,b.py")
        assert ["a.py", "b.py"] == parse_cli_list("a.py,       b.py")

    def test_is_excluded_path(self) -> None:
        """
        Tests the is_excluded_path function for exclude patterns.
        """
        assert is_excluded_path("a.py", ["*"])
        assert is_excluded_path("a.py", ["a.py"])
        assert is_excluded_path("a.py", ["*.py"])
        assert not is_excluded_path("a/b/c/d/e.py", ["*.py"])
        assert is_excluded_path("a/b/c/d/e.py", ["**/*.py"])

    def test_is_excluded_class(self) -> None:
        """
        Tests the is_excluded_class function for exclude patterns.
        """
        assert is_excluded_path("TestClass", ["Test*"])
        assert is_excluded_path("TestClass", ["TestClass"])
        assert is_excluded_path("TestClass", ["TestClass*"])
        assert is_excluded_path("TestClass", ["*stCla*"])
        assert is_excluded_path("TestClass", ["*"])
        assert not is_excluded_path("TestClass", ["CrestClass"])

    def test_is_excluded_function(self) -> None:
        """
        Tests the is_excluded_function function for exclude patterns.
        """
        assert is_excluded_function("test_function", ["*"])
        assert is_excluded_function("test_function", ["test_*"])
        assert is_excluded_function("test_function", ["test_function"])
        assert is_excluded_function("test_function", ["test_function*"])
        assert is_excluded_function("test_functionTestClass", ["*st_fu*"])
        assert not is_excluded_function("TestClass", ["CrestClass"])
