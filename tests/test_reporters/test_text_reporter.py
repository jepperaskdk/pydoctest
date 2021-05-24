import inspect
from types import FunctionType
from typing import Optional, Type, cast
from pydoctest.validation import ClassValidationResult, FunctionValidationResult, ModuleValidationResult, ResultType, ValidationResult
from pydoctest.configuration import Configuration, Verbosity
from pydoctest.reporters.text_reporter import TextReporter


def get_result_object(result_type: ResultType, fail_reason: Optional[str] = None) -> ValidationResult:
    def FunctionName() -> None:
        pass

    def MethodName() -> None:
        pass

    result = ValidationResult()
    result.result = result_type
    result.module_results = [ModuleValidationResult("ModulePath")]
    result.module_results[0].result = result_type
    result.module_results[0].function_results = [FunctionValidationResult(cast(FunctionType, FunctionName))]
    result.module_results[0].function_results[0].result = result_type
    if fail_reason:
        result.module_results[0].function_results[0].fail_reason = fail_reason

    result.module_results[0].class_results = [ClassValidationResult("ClassName")]
    result.module_results[0].class_results[0].result = result_type
    if fail_reason:
        result.module_results[0].class_results[0].fail_reason = fail_reason

    result.module_results[0].class_results[0].function_results = [FunctionValidationResult(cast(FunctionType, MethodName))]
    result.module_results[0].class_results[0].function_results[0].result = result_type
    if fail_reason:
        result.module_results[0].class_results[0].function_results[0].fail_reason = fail_reason

    return result


class TestTextReporter():
    def test_text_reporter_success_verbosity_1(self) -> None:
        config = Configuration.get_default_configuration()
        config.verbosity = Verbosity.SHOW_FAILED
        reporter = TextReporter(config)

        result = get_result_object(ResultType.OK)
        output = reporter.get_output(result)
        assert output == ""

    def test_text_reporter_success_verbosity_2(self) -> None:
        config = Configuration.get_default_configuration()
        config.verbosity = Verbosity.SHOW_ALL
        reporter = TextReporter(config)

        result = get_result_object(ResultType.OK)
        output = reporter.get_output(result)
        messages = [m for m in output.split("Function:") if m]

        assert 'FunctionName' in messages[0]
        assert 'OK' in messages[0]

        assert 'MethodName' in messages[1]
        assert 'OK' in messages[1]

    def test_text_reporter_failed(self) -> None:
        config = Configuration.get_default_configuration()
        config.verbosity = Verbosity.SHOW_ALL
        reporter = TextReporter(config)

        result = get_result_object(ResultType.FAILED, "FAIL REASON")
        output = reporter.get_output(result)
        messages = [m for m in output.split("Function:") if m]

        assert 'FunctionName' in messages[0]
        assert 'FAIL | FAIL REASON' in messages[0]

        assert 'MethodName' in messages[1]
        assert 'FAIL | FAIL REASON' in messages[1]

    def test_text_reporter_no_doc_no_fail(self) -> None:
        config = Configuration.get_default_configuration()
        config.verbosity = Verbosity.SHOW_ALL
        config.fail_on_missing_docstring = False
        reporter = TextReporter(config)

        result = get_result_object(ResultType.NO_DOC)
        output = reporter.get_output(result)
        assert output == ''

    def test_text_reporter_no_doc_do_fail(self) -> None:
        config = Configuration.get_default_configuration()
        config.verbosity = Verbosity.SHOW_ALL
        config.fail_on_missing_docstring = True
        reporter = TextReporter(config)

        result = get_result_object(ResultType.NO_DOC)
        output = reporter.get_output(result)

        messages = [m for m in output.split("Function:") if m]
        assert 'FunctionName' in messages[0]
        assert 'is missing a docstring' in messages[0]

        assert 'MethodName' in messages[1]
        assert 'is missing a docstring' in messages[1]
