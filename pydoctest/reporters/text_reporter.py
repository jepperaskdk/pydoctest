from typing import Optional
from pydoctest.configuration import Verbosity
from pydoctest.reporters.reporter import Reporter
from pydoctest.validation import ClassValidationResult, FunctionValidationResult, ModuleValidationResult, ResultType, ValidationResult


SUCCESS = "OK"
FAILED = "FAIL"
SKIPPED = "SKIPPED"


class TextReporter(Reporter):
    def get_output(self, result: ValidationResult) -> str:
        """Returns the text output by walking the ValidationResult object.

        Args:
            result (ValidationResult): The results from running Pydoctest.

        Returns:
            str: The output to be returned.
        """
        output = ""
        for module_result in result.module_results:
            output += self.get_module_output(module_result)

        return output

    def get_module_output(self, result: ModuleValidationResult) -> str:
        """Returns the text output from the result object from walking the module.

        Args:
            result (ModuleValidationResult): The result from running Pydoctest on the module.

        Returns:
            str: The output of the module.
        """
        output = ""
        if result.fail_reason != "":
            output = f"{result.fail_reason}\n"

        for f_r in result.function_results:
            output += self.get_function_output(f_r)

        for c_r in result.class_results:
            output += self.get_class_output(c_r)

        return output

    def get_function_output(self, result: FunctionValidationResult, class_name: Optional[str] = None) -> str:
        """Returns the text output from the result object from the function.

        Args:
            result (FunctionValidationResult): The result from running Pydoctest on the function.
            class_name (Optional[str]): Optionally which class this function is run within.
        Returns:
            str: The output from the function.
        """
        module = ""
        if result.module.__file__:
            # Try to get just workspace relative path
            module = result.module.__file__.replace(self.config.working_directory, "")

        function_name = result.function.__name__
        class_name_if_exists = class_name + '::' if class_name is not None else ''
        if result.result == ResultType.OK:
            if self.config.verbosity == Verbosity.SHOW_ALL:
                return f"{module}::{class_name_if_exists}{function_name} {SUCCESS}\n"
            return ""

        if result.result == ResultType.FAILED:
            return f"{module}::{class_name_if_exists}{function_name} {FAILED} | {result.fail_reason}\n"

        if result.result == ResultType.NO_DOC and self.config.fail_on_missing_docstring:
            return f"{module}::{class_name_if_exists}{function_name} is missing a docstring\n"

        return ""

    def get_class_output(self, result: ClassValidationResult) -> str:
        """Returns the text output from the result object from the class.

        Args:
            result (ClassValidationResult): The result from running Pydoctest on the class.

        Returns:
            str: The output of the class and its functions.
        """
        output = ""
        for fn in result.function_results:
            output += self.get_function_output(fn, class_name=result.class_name)
        return output
