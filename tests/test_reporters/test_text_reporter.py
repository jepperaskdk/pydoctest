from typing import Optional, Type
from pydoctest.validation import ClassValidationResult, FunctionValidationResult, ModuleValidationResult, ResultType, ValidationResult
from pydoctest.configuration import Configuration, Verbosity
from pydoctest.reporters.text_reporter import TextReporter


def get_result_object(result_type: ResultType, fail_reason: Optional[str] = None) -> ValidationResult:
    def fn() -> None:
        pass
    result = ValidationResult()
    result.result = result_type
    result.module_results = [ModuleValidationResult("ModulePath")]
    result.module_results[0].result = result_type
    result.module_results[0].function_results = [FunctionValidationResult("FunctionName")]
    result.module_results[0].function_results[0].result = result_type
    if fail_reason:
        result.module_results[0].function_results[0].fail_reason = fail_reason

    result.module_results[0].class_results = [ClassValidationResult("ClassName")]
    result.module_results[0].class_results[0].result = result_type
    if fail_reason:
        result.module_results[0].class_results[0].fail_reason = fail_reason

    result.module_results[0].class_results[0].function_results = [FunctionValidationResult("MethodName")]
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
        assert output == 'Function: FunctionName OK\nFunction: MethodName OK\n'

    def test_text_reporter_failed(self) -> None:
        config = Configuration.get_default_configuration()
        config.verbosity = Verbosity.SHOW_ALL
        reporter = TextReporter(config)

        result = get_result_object(ResultType.FAILED, "FAIL REASON")
        output = reporter.get_output(result)
        assert output == 'Function: FunctionName FAIL | FAIL REASON\nFunction: MethodName FAIL | FAIL REASON\n'

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
        assert output == 'Function: FunctionName is missing a docstring\nFunction: MethodName is missing a docstring\n'
