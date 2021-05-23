import json
from pydoctest.reporters.reporter import Reporter
from pydoctest.validation import ValidationResult


class JSONReporter(Reporter):
    def get_output(self, result: ValidationResult) -> str:
        """Returns the JSON output by walking the ValidationResult object.

        Args:
            result (ValidationResult): The results from running Pydoctest

        Returns:
            str: The JSON output to be returned.
        """
        dict_result = result.to_dict()
        return json.dumps(dict_result)
