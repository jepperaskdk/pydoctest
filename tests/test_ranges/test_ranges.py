import pydoc

from pydoctest.configuration import Configuration
from pydoctest.validation import validate_function, ResultType

import tests.test_ranges.example_class
import tests.test_class.raises_class


class TestRanges():
    def test_func_no_summary(self) -> None:
        config = Configuration.get_default_configuration()
        config.fail_on_missing_summary = True
        result = validate_function(tests.test_ranges.example_class.ExampleClass.func_no_summary, config, tests.test_ranges.example_class)
        assert result.result == ResultType.FAILED
        assert result.fail_reason == 'Function does not have a summary'
        assert result.range is not None
        assert result.range.start_line == 5
        assert result.range.end_line == 12

    def test_func_no_docstring(self) -> None:
        config = Configuration.get_default_configuration()
        config.fail_on_missing_docstring = True
        result = validate_function(tests.test_ranges.example_class.ExampleClass.func_no_docstring, config, tests.test_ranges.example_class)
        assert result.result == ResultType.FAILED
        assert result.fail_reason == 'Function does not have a docstring'
        assert result.range is not None
        assert result.range.start_line == 16
        assert result.range.end_line == 16

    def test_func_parse_exception(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_ranges.example_class.ExampleClass.func_parse_exception, config, tests.test_ranges.example_class)
        assert result.result == ResultType.FAILED
        assert 'Unable to parse docstring' in result.fail_reason
        assert result.range is not None
        assert result.range.start_line == 22
        assert result.range.end_line == 32

    def test_func_return_type_differ(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_ranges.example_class.ExampleClass.func_return_type_differ, config, tests.test_ranges.example_class)
        assert result.result == ResultType.FAILED
        assert 'Return type differ' in result.fail_reason
        assert result.range is not None
        assert result.range.start_line == 38
        assert result.range.end_line == 45

    def test_func_number_of_arguments_differ(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_ranges.example_class.ExampleClass.func_number_of_arguments_differ, config, tests.test_ranges.example_class)
        assert result.result == ResultType.FAILED
        assert 'Number of arguments differ' in result.fail_reason
        assert result.range is not None
        assert result.range.start_line == 51
        assert result.range.end_line == 58

    def test_func_argument_name_differ(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_ranges.example_class.ExampleClass.func_argument_name_differ, config, tests.test_ranges.example_class)
        assert result.result == ResultType.FAILED
        assert 'Argument name differ' in result.fail_reason
        assert result.range is not None
        assert result.range.start_line == 64
        assert result.range.end_line == 71

    def test_func_argument_type_differ(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_ranges.example_class.ExampleClass.func_argument_type_differ, config, tests.test_ranges.example_class)
        assert result.result == ResultType.FAILED
        assert 'Argument type differ' in result.fail_reason
        assert result.range is not None
        assert result.range.start_line == 77
        assert result.range.end_line == 84

    def test_func_number_of_raised_exceptions_differ(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_ranges.example_class.ExampleClass.func_number_of_raised_exceptions_differ, config, tests.test_ranges.example_class)
        assert result.result == ResultType.FAILED
        assert 'Number of listed raised exceptions does not match actual' in result.fail_reason
        assert result.range is not None
        assert result.range.start_line == 89
        assert result.range.end_line == 100

    def test_func_listed_exceptions_not_match(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_ranges.example_class.ExampleClass.func_listed_exceptions_not_match, config, tests.test_ranges.example_class)
        assert result.result == ResultType.FAILED
        assert 'Listed raised exceptions does not match actual' in result.fail_reason
        assert result.range is not None
        assert result.range.start_line == 113
        assert result.range.end_line == 123
