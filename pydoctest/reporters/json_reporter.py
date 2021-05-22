import json
from pydoctest.reporters.reporter import Reporter
from pydoctest.validation import ValidationResult


class JSONReporter(Reporter):
    def get_output(self, result: ValidationResult) -> str:
        dict_result = result.to_dict()
        return json.dumps(dict_result)
