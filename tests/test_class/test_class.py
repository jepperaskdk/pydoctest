from pydoctest.configuration import Configuration
from pydoctest.validation import ResultType, validate_class, validate_function

import tests.test_class.example_class


class TestDocs():
    def test_class_is_ok(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_class(tests.test_class.example_class.CorrectTestClass, config, tests.test_class.example_class)
        assert result.result == ResultType.OK
        for res in result.function_results:
            assert res.result == ResultType.OK

    def test_empty_func(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_class.example_class.CorrectTestClass.empty_func, config, tests.test_class.example_class)
        assert result.result == ResultType.OK

    def test_func_returns_none(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_class.example_class.CorrectTestClass.func_returns_none, config, tests.test_class.example_class)
        assert result.result == ResultType.OK

    def test_func_returns_int(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_class.example_class.CorrectTestClass.func_returns_int, config, tests.test_class.example_class)
        assert result.result == ResultType.OK

    def test_func_has_arg_returns_arg(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_class.example_class.CorrectTestClass.func_has_arg_returns_arg, config, tests.test_class.example_class)
        assert result.result == ResultType.OK
