from pydoctest.configuration import Configuration, Verbosity
from pydoctest.reporters.reporter import Reporter
from pydoctest.validation import ClassValidationResult, FunctionValidationResult, ModuleValidationResult, ResultType, ValidationResult


SUCCESS = "OK"
FAILED = "FAIL"
SKIPPED = "SKIPPED"


class TextReporter(Reporter):
    def get_output(self, result: ValidationResult) -> str:
        """Returns the text output by walking the ValidationResult object.

        Args:
            result (ValidationResult): The results from running Pydoctest

        Returns:
            str: The output to be returned.
        """
        output = ""
        for module_result in result.module_results:
            output += self.get_module_output(module_result)

        return output

    def get_module_output(self, result: ModuleValidationResult) -> str:
        output = ""
        for f_r in result.function_results:
            output += self.get_function_output(f_r)

        for c_r in result.class_results:
            output += self.get_class_output(c_r)

        return output

    def get_function_output(self, result: FunctionValidationResult) -> str:
        if result.result == ResultType.OK:
            if self.config.verbosity == Verbosity.SHOW_ALL:
                return f"Function: {result.function.__module__}:{result.function.__name__} {SUCCESS}\n"
            return ""

        if result.result == ResultType.FAILED:
            return f"Function: {result.function.__module__}:{result.function.__name__} {FAILED} | {result.fail_reason}\n"

        if result.result == ResultType.NO_DOC and self.config.fail_on_missing_docstring:
            return f"Function: {result.function.__name__} is missing a docstring"

        return ""

    def get_class_output(self, result: ClassValidationResult) -> str:
        output = ""
        for fn in result.function_results:
            output += self.get_function_output(fn)
        return output
