from enum import IntEnum
import inspect
from sys import modules
import types

from types import FunctionType, ModuleType
from typing import Any, Dict, List, Optional, Type

from pydoctest.logging import log
from pydoctest.configuration import Configuration
from pydoctest.parsers.parser import Parameter
from pydoctest.exceptions import ParseException
from pydoctest.utilities import get_exceptions_raised, is_excluded_function


class Range():

    def __init__(self, start_line: int, end_line: int, start_character: int, end_character: int) -> None:
        """Creates a new range object, used for indicating errors in vscode.

        TODO: Are these zero- or one-indexed?

        Args:
            start_line (int): Where the range starts.
            end_line (int): Where the range ends.
            start_character (int): The column the range starts in (in start_line).
            end_character (int): The column the range ends in (in end_line).
        """
        self.start_line: int = start_line
        self.end_line: int = end_line
        self.start_character: int = start_character
        self.end_character: int = end_character

    def to_dict(self) -> Dict[str, Any]:
        """Serializes this class to dict, which is useful for the JSONReporter.

        Returns:
            Dict[str, Any]: The range.
        """
        return {
            'start_line': self.start_line,
            'end_line': self.end_line,
            'start_character': self.start_character,
            'end_character': self.end_character
        }


class ValidationCounts():
    def __init__(self) -> None:
        """Helper class for storing counts from running Pydoctest.
        """
        self.module_count = 0
        self.functions_succeeded = 0
        self.functions_failed = 0
        self.functions_skipped = 0

    def get_total(self) -> int:
        """Returns the total number of functions executed.

        Returns:
            int: The total count.
        """
        return self.functions_succeeded + self.functions_failed + self.functions_skipped


class ResultType(IntEnum):
    NOT_RUN = 0
    OK = 1
    FAILED = 2
    SKIPPED = 3
    NO_DOC = 4


class Result():
    def __init__(self) -> None:
        """Base Result class for storing result and fail_reason.
        """
        # TODO: Rename result -> Status?
        self.result: ResultType = ResultType.NOT_RUN
        self.fail_reason: str = ""

    # TODO: Rather than have all Result-subclasses implement this, we can probably make a generic function
    def to_dict(self) -> Dict[str, Any]:
        """Serializes this class to dict, which is useful for the JSONReporter.

        Returns:
            Dict[str, Any]: The result and fail-reason.
        """
        return { 'result': self.result, 'fail_reason': self.fail_reason }


class FunctionValidationResult(Result):
    def __init__(self, function: FunctionType, module: ModuleType) -> None:
        """Result class for storing results of testing functions.

        Args:
            function (FunctionType): A reference to the function that was tested.
            module (ModuleType): The module containing the function - used when outputting text results to identify the file.
        """
        super().__init__()
        self.module = module
        self.function = function
        self.range: Optional[Range] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serializes this class to dict, which is useful for the JSONReporter.

        Returns:
            Dict[str, Any]: The result, fail_reason and function_name.
        """
        return {
            **super().to_dict(),
            'function': str(self.function),
            'range': self.range.to_dict() if self.range else None
        }


class ClassValidationResult(Result):
    def __init__(self, class_name: str) -> None:
        """Result class for storing results of testing classes.

        Args:
            class_name (str): The name of the class.
        """
        super().__init__()
        self.class_name = class_name
        self.function_results: List[FunctionValidationResult] = []

    def to_dict(self) -> Dict[str, Any]:
        """Serializes this class to dict, which is useful for the JSONReporter.

        Returns:
            Dict[str, Any]: The result, fail_reason, class_name and function_results.
        """
        return {
            **super().to_dict(),
            'class_name': self.class_name,
            'function_results': [
                r.to_dict() for r in self.function_results
            ]
        }


class ModuleValidationResult(Result):
    def __init__(self, module_path: str) -> None:
        """Result class for storing results of testing modules.

        Args:
            module_path (str): The path to the module tested.
        """
        super().__init__()
        self.module_path = module_path
        self.function_results: List[FunctionValidationResult] = []
        self.class_results: List[ClassValidationResult] = []

    def to_dict(self) -> Dict[str, Any]:
        """Serializes this class to dict, which is useful for the JSONReporter.

        Returns:
            Dict[str, Any]: The result, fail_reason, module_path, function_results and class_results.
        """
        return {
            **super().to_dict(),
            'module_path': self.module_path,
            'function_results': [
                r.to_dict() for r in self.function_results
            ],
            'class_results': [
                r.to_dict() for r in self.class_results
            ]
        }


class ValidationResult(Result):
    def __init__(self) -> None:
        """Result class for storing results of running pydoctest on a project.
        """
        super().__init__()
        self.module_results: List[ModuleValidationResult] = []

    def to_dict(self) -> Dict[str, Any]:
        """Serializes this class to dict, which is useful for the JSONReporter.

        Returns:
            Dict[str, Any]: The result, fail_reason and module_results.
        """
        return {
            **super().to_dict(),
            'module_results': [
                r.to_dict() for r in self.module_results
            ]
        }

    def get_counts(self) -> ValidationCounts:
        """Counts the failed, succeeded and skipped tests of running pydoctest.

        Returns:
            ValidationCounts: The counts object.
        """
        counts = ValidationCounts()
        counts.module_count = len(self.module_results)

        def increment(fn_result: FunctionValidationResult) -> None:
            if fn_result.result == ResultType.FAILED:
                counts.functions_failed += 1
            elif fn_result.result == ResultType.OK:
                counts.functions_succeeded += 1
            else:
                counts.functions_skipped += 1

        for m in self.module_results:
            for fn in m.function_results:
                increment(fn)
            for c in m.class_results:
                for fn in c.function_results:
                    increment(fn)
        return counts


def __get_docstring_range(fn: FunctionType, module_type: ModuleType, docstring: Optional[str] = None) -> Optional[Range]:
    """Returns the range for the docstring.

    Args:
        fn (FunctionType): The function to validate.
        module_type (ModuleType): The module from which the function was extracted.
        docstring (Optional[str]): Optionally, the docstring.

    Returns:
        Optional[Range]: The range, if found.
    """
    lines, line_number = inspect.getsourcelines(fn)
    start_line, end_line = -1, -1
    for i, l in enumerate(lines):
        if l.count('"""') == 2:
            # One liner
            return Range(line_number + i, line_number + i, 0, 0)

        if '"""' in l:
            if start_line == -1:
                start_line = line_number + i
            elif end_line == -1:
                end_line = line_number + i
                return Range(start_line, end_line, 0, 0)
    return None


def validate_function(fn: FunctionType, config: Configuration, module_type: ModuleType) -> FunctionValidationResult:
    """Validates the docstring of a function against its signature.

    Args:
        fn (FunctionType): The function to validate.
        config (Configuration): The configuration to use while validating.
        module_type (ModuleType): The module from which the function was extracted.

    Returns:
        FunctionValidationResult: The result of validating this function.
    """
    log(f"Validating function: {fn}")
    result = FunctionValidationResult(fn, module_type)

    doc = inspect.getdoc(fn)
    if not doc:
        if config.fail_on_missing_docstring:
            result.result = ResultType.FAILED
            result.fail_reason = f"Function does not have a docstring"
            _, line_number = inspect.getsourcelines(fn)
            result.range = Range(line_number, line_number, 0, 0)
        else:
            result.result = ResultType.NO_DOC
        return result

    parser = config.get_parser()

    summary = parser.get_summary(doc, module_type)
    if not summary and config.fail_on_missing_summary:
        result.result = ResultType.FAILED
        result.fail_reason = f"Function does not have a summary"
        result.range = __get_docstring_range(fn, module_type, doc)
        return result

    sig = inspect.signature(fn)
    sig_parameters = [Parameter(name, proxy.annotation) for name, proxy in sig.parameters.items() if name != "self"]
    sig_return_type = type(None) if sig.return_annotation is None else sig.return_annotation

    try:
        doc_parameters = parser.get_parameters(doc, module_type)
        doc_return_type = parser.get_return_type(doc, module_type)
    except ParseException as e:
        result.result = ResultType.FAILED
        result.fail_reason = f"Unable to parse docstring: {str(e)}"
        result.range = __get_docstring_range(fn, module_type, doc)
        return result

    # Validate return type
    if sig_return_type != doc_return_type:
        result.result = ResultType.FAILED
        result.fail_reason = f"Return type differ. Expected (from signature) {sig_return_type}, but got (in docs) {doc_return_type}."
        result.range = __get_docstring_range(fn, module_type, doc)
        return result

    # Validate equal number of parameters
    if len(sig_parameters) != len(doc_parameters):
        result.result = ResultType.FAILED
        result.fail_reason = f"Number of arguments differ. Expected (from signature) {len(sig_parameters)} arguments, but found (in docs) {len(doc_parameters)}."
        result.range = __get_docstring_range(fn, module_type, doc)
        return result

    # Validate name and type of function parameters
    for sigparam, docparam in zip(sig_parameters, doc_parameters):
        if sigparam.name != docparam.name:
            result.result = ResultType.FAILED
            result.fail_reason = f"Argument name differ. Expected (from signature) '{sigparam.name}', but got (in docs) '{docparam.name}'"
            result.range = __get_docstring_range(fn, module_type, doc)
            return result

        # NOTE: Optional[str] == Union[str, None] # True
        if sigparam.type != docparam.type:
            result.result = ResultType.FAILED
            result.fail_reason = f"Argument type differ. Argument '{sigparam.name}' was expected (from signature) to have type '{sigparam.type}', but has (in docs) type '{docparam.type}'"
            result.range = __get_docstring_range(fn, module_type, doc)
            return result

    # Validate exceptions raised
    if config.fail_on_raises_section:
        try:
            sig_exceptions = get_exceptions_raised(fn, module_type)
            doc_exceptions = parser.get_exceptions_raised(doc)

            if len(sig_exceptions) != len(doc_exceptions):
                result.result = ResultType.FAILED
                result.fail_reason = f"Number of listed raised exceptions does not match actual. Doc: {doc_exceptions}, expected: {sig_exceptions}"
                result.range = __get_docstring_range(fn, module_type, doc)
                return result

            intersection = set(sig_exceptions) - set(doc_exceptions)
            if len(intersection) > 0:
                result.result = ResultType.FAILED
                result.fail_reason = f"Listed raised exceptions does not match actual. Docstring: {doc_exceptions}, expected: {sig_exceptions}"
                result.range = __get_docstring_range(fn, module_type, doc)
                return result
        except ParseException as e:
            result.result = ResultType.FAILED
            result.fail_reason = f"Unable to parse docstring: {str(e)}"
            result.range = __get_docstring_range(fn, module_type, doc)
            return result

    result.result = ResultType.OK
    return result


def validate_class(class_instance: Any, config: Configuration, module_type: ModuleType) -> ClassValidationResult:
    """Validates the class by validating each of its methods.

    Args:
        class_instance (Any): A class to validate.
        config (Configuration): The configuration to use while validating.
        module_type (ModuleType): The module from which the class was extracted.

    Returns:
        ClassValidationResult: The result of validating this class.
    """
    log(f"Validating class: {class_instance}")
    class_result = ClassValidationResult(class_instance.__name__)

    for name, item in inspect.getmembers(class_instance):
        if inspect.isfunction(item) and item.__module__ == module_type.__name__:
            if name not in class_instance.__dict__ or item != class_instance.__dict__[name]:
                continue

            # Check if method is excluded
            if is_excluded_function(name, config.exclude_methods):
                continue

            function_result = validate_function(item, config, module_type)
            if function_result.result == ResultType.FAILED:
                class_result.result = ResultType.FAILED

            class_result.function_results.append(function_result)

    # If result has not been changed at this point, it must be OK
    if class_result.result == ResultType.NOT_RUN:
        class_result.result = ResultType.OK

    return class_result
