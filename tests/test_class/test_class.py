from pydoctest.configuration import Configuration
from pydoctest.validation import ResultType, validate_class, validate_function
from pydoctest.main import PyDoctestService

import tests.test_class.correct_class
import tests.test_class.nodocstring_class
import tests.test_class.incorrect_class
import tests.test_class.raises_class


class TestDocs():
    # test correct_class
    def test_correct_class_module(self) -> None:
        config = Configuration.get_configuration_from_path("tests/test_class/pydoctest_correct_class.json")

        ds = PyDoctestService(config)
        result = ds.validate()
        assert result.result == ResultType.OK

    def test_correct_class_class_is_ok(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_class(tests.test_class.correct_class.CorrectTestClass, config, tests.test_class.correct_class)
        assert result.result == ResultType.OK
        for res in result.function_results:
            assert res.result == ResultType.OK

    def test_correct_class_empty_func(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_class.correct_class.CorrectTestClass.empty_func, config, tests.test_class.correct_class)
        assert result.result == ResultType.OK

    def test_correct_class_func_returns_none(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_class.correct_class.CorrectTestClass.func_returns_none, config, tests.test_class.correct_class)
        assert result.result == ResultType.OK

    def test_correct_class_returns_int(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_class.correct_class.CorrectTestClass.func_returns_int, config, tests.test_class.correct_class)
        assert result.result == ResultType.OK

    def test_correct_class_has_arg_returns_arg(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_class.correct_class.CorrectTestClass.func_has_arg_returns_arg, config, tests.test_class.correct_class)
        assert result.result == ResultType.OK

    # Test nodocstring_class
    def test_func_no_docstring_no_fail(self) -> None:
        config = Configuration.get_default_configuration()
        config.fail_on_missing_docstring = False
        result = validate_function(tests.test_class.nodocstring_class.ClassNoDocString.func_no_docstring, config, tests.test_class.correct_class)
        assert result.result == ResultType.NO_DOC

    def test_func_no_docstring_do_fail(self) -> None:
        config = Configuration.get_default_configuration()
        config.fail_on_missing_docstring = True
        result = validate_function(tests.test_class.nodocstring_class.ClassNoDocString.func_no_docstring, config, tests.test_class.correct_class)
        assert result.result == ResultType.FAILED

    def test_func_no_summary_no_fail(self) -> None:
        config = Configuration.get_default_configuration()
        config.fail_on_missing_summary = False
        result = validate_function(tests.test_class.nodocstring_class.ClassNoDocString.func_no_summary, config, tests.test_class.correct_class)
        assert result.result == ResultType.OK

    def test_func_no_summary_do_fail(self) -> None:
        config = Configuration.get_default_configuration()
        config.fail_on_missing_summary = True
        result = validate_function(tests.test_class.nodocstring_class.ClassNoDocString.func_no_summary, config, tests.test_class.correct_class)
        assert result.result == ResultType.FAILED
        assert result.fail_reason == 'Function does not have a summary'

    def test_func_with_raises(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_class.raises_class.RaisesClass.func_with_raise_and_args_and_return, config, tests.test_class.incorrect_class)
        assert result.result == ResultType.OK

    # Test incorrect_class
    def test_incorrect_class_module(self) -> None:
        config = Configuration.get_configuration_from_path("tests/test_class/pydoctest_incorrect_class.json")
        ds = PyDoctestService(config)
        result = ds.validate()
        assert result.result == ResultType.FAILED

    def test_incorrect_class_is_fail(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_class(tests.test_class.incorrect_class.IncorrectTestClass, config, tests.test_class.incorrect_class)
        assert result.result == ResultType.FAILED
        for res in result.function_results:
            assert res.result == ResultType.FAILED

    def test_incorrect_class_empty_func(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_class.incorrect_class.IncorrectTestClass.empty_func, config, tests.test_class.incorrect_class)
        assert result.result == ResultType.FAILED
        assert result.fail_reason == "Number of arguments differ. Expected (from signature) 0 arguments, but found (in docs) 1."

    def test_incorrect_class_func_returns_none(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_class.incorrect_class.IncorrectTestClass.func_returns_none, config, tests.test_class.incorrect_class)
        assert result.result == ResultType.FAILED
        assert result.fail_reason == "Return type differ. Expected (from signature) <class 'NoneType'>, but got (in docs) <class 'int'>."

    def test_incorrect_class_func_returns_int(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_class.incorrect_class.IncorrectTestClass.func_returns_int, config, tests.test_class.incorrect_class)
        assert result.result == ResultType.FAILED
        assert result.fail_reason == "Return type differ. Expected (from signature) <class 'int'>, but got (in docs) <class 'bool'>."

    def test_incorrect_class_func_has_arg_returns_arg(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_class.incorrect_class.IncorrectTestClass.func_has_arg_returns_arg, config, tests.test_class.incorrect_class)
        assert result.result == ResultType.FAILED
        assert result.fail_reason == "Return type differ. Expected (from signature) <class 'float'>, but got (in docs) <class 'NoneType'>."

    def test_incorrect_class_func_name_mismatch(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_class.incorrect_class.IncorrectTestClass.func_name_mismatch, config, tests.test_class.incorrect_class)
        assert result.result == ResultType.FAILED
        assert result.fail_reason == "Argument name differ. Expected (from signature) 'a', but got (in docs) 'b'"

    def test_incorrect_class_func_type_mismatch(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_class.incorrect_class.IncorrectTestClass.func_type_mismatch, config, tests.test_class.incorrect_class)
        assert result.result == ResultType.FAILED
        assert result.fail_reason == "Argument type differ. Argument 'a' was expected (from signature) to have type '<class 'int'>', but has (in docs) type '<class 'float'>'"

    # Test counts_class
    def test_counts_class(self) -> None:
        config = Configuration.get_configuration_from_path("tests/test_class/pydoctest_get_counts.json")
        config.fail_on_missing_docstring = False

        ds = PyDoctestService(config)
        result = ds.validate()
        counts = result.get_counts()

        assert counts.functions_failed == 1
        assert counts.functions_skipped == 1
        assert counts.functions_succeeded == 2
        assert counts.module_count == 1

        assert counts.get_total() == 4

    # Test enum_in_module
    def test_enum_in_module(self) -> None:
        # Test that enums are ignored
        config = Configuration.get_configuration_from_path("tests/test_class/pydoctest_enum_in_module.json")
        ds = PyDoctestService(config)
        result = ds.validate()
        assert len(result.module_results[0].class_results) == 1
        assert result.module_results[0].class_results[0].class_name == "ExampleClass"

    # Test no include_paths in config
    def test_no_include_paths(self) -> None:
        config = Configuration.get_configuration_from_path("tests/test_class/test_no_include_paths/pydoctest.json")
        ds = PyDoctestService(config)
        result = ds.validate()
        assert result.result == ResultType.OK

        # Assert that 1 module was found in root. We do not search recursively.
        assert len(result.module_results) == 1

    # Test incorrect raise
    def test_func_with_missing_raise(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_class.raises_class.RaisesClass.func_with_missing_raise, config, tests.test_class.incorrect_class)
        assert result.result == ResultType.FAILED

    def test_func_with_incorrect_raise(self) -> None:
        config = Configuration.get_default_configuration()
        result = validate_function(tests.test_class.raises_class.RaisesClass.func_with_incorrect_raise, config, tests.test_class.incorrect_class)
        assert result.result == ResultType.FAILED

    def test_fail_on_raises_section_dont_fail(self) -> None:
        config = Configuration.get_default_configuration()
        config.fail_on_raises_section = False
        result = validate_function(tests.test_class.raises_class.RaisesClass.func_with_incorrect_raise, config, tests.test_class.incorrect_class)
        assert result.result == ResultType.OK

    # Test multiline strings
    def test_raises_on_function_with_multiline_string(self) -> None:
        """
        Solves: https://github.com/jepperaskdk/pydoctest/issues/40.
        """
        config = Configuration.get_default_configuration()
        config.fail_on_raises_section = True
        result = validate_function(tests.test_class.raises_class.RaisesClass.func_with_raise_multiline_string, config, tests.test_class.incorrect_class)
        assert result.result == ResultType.OK
