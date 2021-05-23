import json

from pydoctest.validation import ResultType
from pydoctest.configuration import Configuration, Verbosity
from pydoctest.reporters.json_reporter import JSONReporter
from tests.test_reporters.test_text_reporter import get_result_object


class TestJSONReporter():
    def test_text_reporter_success(self) -> None:
        config = Configuration.get_default_configuration()
        reporter = JSONReporter(config)

        result = get_result_object(ResultType.OK)
        output = reporter.get_output(result)
        d = json.loads(output)
        assert d['result'] == ResultType.OK
        assert d['module_results'][0]['function_results'][0]['result'] == ResultType.OK
        assert d['module_results'][0]['class_results'][0]['function_results'][0]['result'] == ResultType.OK

    def test_text_reporter_failed(self) -> None:
        config = Configuration.get_default_configuration()
        reporter = JSONReporter(config)

        result = get_result_object(ResultType.FAILED, "FAIL REASON")
        output = reporter.get_output(result)
        d = json.loads(output)
        assert d['result'] == ResultType.FAILED
        assert d['module_results'][0]['function_results'][0]['result'] == ResultType.FAILED
        assert d['module_results'][0]['function_results'][0]['fail_reason'] == "FAIL REASON"
        assert d['module_results'][0]['class_results'][0]['function_results'][0]['result'] == ResultType.FAILED
        assert d['module_results'][0]['class_results'][0]['function_results'][0]['fail_reason'] == "FAIL REASON"

    def test_text_reporter_no_doc_no_fail(self) -> None:
        config = Configuration.get_default_configuration()
        config.fail_on_missing_docstring = False
        reporter = JSONReporter(config)

        result = get_result_object(ResultType.NO_DOC)
        output = reporter.get_output(result)
        d = json.loads(output)
        assert d['result'] == ResultType.NO_DOC
        assert d['module_results'][0]['function_results'][0]['result'] == ResultType.NO_DOC
        assert d['module_results'][0]['class_results'][0]['function_results'][0]['result'] == ResultType.NO_DOC
