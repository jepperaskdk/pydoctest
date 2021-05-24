from enum import IntEnum
import inspect
import types
from pydoctest.parsers.parser import Parameter

from types import FunctionType, ModuleType
from typing import Any, Dict, List, Optional, Type

from pydoctest.logging import log
from pydoctest.configuration import Configuration


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
    def __init__(self, function: FunctionType) -> None:
        """Result class for storing results of testing functions.

        Args:
            function (FunctionType): A reference to the function that was tested.
        """
        super().__init__()
        self.function = function

    def to_dict(self) -> Dict[str, Any]:
        """Serializes this class to dict, which is useful for the JSONReporter.

        Returns:
            Dict[str, Any]: The result, fail_reason and function_name.
        """
        return {
            **super().to_dict(),
            'function': str(self.function)
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
    result = FunctionValidationResult(fn)

    doc = inspect.getdoc(fn)
    if not doc:
        if config.fail_on_missing_docstring:
            result.result = ResultType.FAILED
            result.fail_reason = f"Function does not have a docstring"
        else:
            result.result = ResultType.NO_DOC
        return result

    sig = inspect.signature(fn)
    sig_parameters = [Parameter(name, proxy.annotation) for name, proxy in sig.parameters.items() if name != "self"]
    sig_return_type = type(None) if sig.return_annotation is None else sig.return_annotation

    parser = config.get_parser()
    doc_parameters = parser.get_parameters(doc, module_type)
    doc_return_type = parser.get_return_type(doc, module_type)

    if sig_return_type != doc_return_type:
        result.result = ResultType.FAILED
        result.fail_reason = f"Return type differ. Expected (from signature) {sig_return_type}, but got (in docs) {doc_return_type}."
        return result

    if len(sig_parameters) != len(doc_parameters):
        result.result = ResultType.FAILED
        result.fail_reason = f"Number of arguments differ. Expected (from signature) {len(sig_parameters)} arguments, but found (in docs) {len(doc_parameters)}."
        return result

    for sigparam, docparam in zip(sig_parameters, doc_parameters):
        if sigparam.name != docparam.name:
            result.result = ResultType.FAILED
            result.fail_reason = f"Argument name differ. Expected (from signature) '{sigparam.name}', but got (in docs) '{docparam.name}'"
            return result

        # NOTE: Optional[str] == Union[str, None] # True
        if sigparam.type != docparam.type:
            result.result = ResultType.FAILED
            result.fail_reason = f"Argument type differ. Argument '{sigparam.name}' was expected (from signature) to have type '{sigparam.type}', but has (in docs) type '{docparam.type}'"
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

    # for name, item in class_instance.__dict__.items():
    for name, item in inspect.getmembers(class_instance):
        if inspect.isfunction(item):
            function_result = validate_function(item, config, module_type)
            if function_result.result == ResultType.FAILED:
                class_result.result = ResultType.FAILED
            class_result.function_results.append(function_result)

    # If result has not been changed at this point, it must be OK
    if class_result.result == ResultType.NOT_RUN:
        class_result.result = ResultType.OK

    return class_result
