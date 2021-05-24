import sys
import pytest

# These two imports are necessary for test_get_type_from_module_bfs
import pydoctest
from pydoctest.configuration import Configuration

from pydoctest.validation import ResultType, validate_class, validate_function
from pydoctest.main import PyDoctestService
from pydoctest.utilities import get_type_from_module
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
        with pytest.raises(Exception) as exc_info:
            result = validate_function(tests.test_utilities.example_class.ExampleClass.func_raises, config, tests.test_utilities.example_class)
        assert 'Was unable to detect the type of: DEFINITELYNOTACLASS from module:' in str(exc_info.value)
