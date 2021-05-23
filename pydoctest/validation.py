from enum import Enum
import inspect
import types
from pydoctest.parsers.parser import Parameter

from types import FunctionType, ModuleType
from typing import Any, Dict, List, Type

from pydoctest.logging import log
from pydoctest.configuration import Configuration


class ValidationCounts():
    def __init__(self) -> None:
        self.module_count = 0
        self.functions_succeeded = 0
        self.functions_failed = 0
        self.functions_skipped = 0

    def get_total(self) -> int:
        return self.functions_succeeded + self.functions_failed + self.functions_skipped


class ResultType(Enum):
    NOT_RUN = 0
    OK = 1
    FAILED = 2
    SKIPPED = 3
    NO_DOC = 4


class Result():
    def __init__(self) -> None:
        self.result: ResultType = ResultType.NOT_RUN
        self.fail_reason: str = ""

    # TODO: Rather than have all Result-subclasses implement this, we can probably make a generic function
    def to_dict(self) -> Dict[str, Any]:
        return { 'result': self.result, 'fail_reason': self.fail_reason }


class FunctionValidationResult(Result):
    def __init__(self, fn: FunctionType) -> None:
        super().__init__()
        self.function = fn

    def to_dict(self) -> Dict[str, Any]:
        return {
            **super().to_dict(),
            'function_name': self.function.__name__
        }


class ClassValidationResult(Result):
    def __init__(self, class_name: str) -> None:
        super().__init__()
        self.class_name = class_name
        self.function_results: List[FunctionValidationResult] = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            **super().to_dict(),
            'class_name': self.class_name,
            'function_results': [
                r.to_dict() for r in self.function_results
            ]
        }


class ModuleValidationResult(Result):
    def __init__(self, module_path: str) -> None:
        super().__init__()
        self.module_path = module_path
        self.function_results: List[FunctionValidationResult] = []
        self.class_results: List[ClassValidationResult] = []

    def to_dict(self) -> Dict[str, Any]:
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
        super().__init__()
        self.module_results: List[ModuleValidationResult] = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            **super().to_dict(),
            'module_results': [
                r.to_dict() for r in self.module_results
            ]
        }

    def get_counts(self) -> ValidationCounts:
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


def type_to_string(t: Type) -> str:
    if t == inspect.Signature.empty:
        return "None"

    sigtype = str(t).replace('typing.', '')
    if '<class' in sigtype:
        sigtype = sigtype.split('\'')[1]
    return sigtype


def validate_function(fn: FunctionType, config: Configuration, module_type: ModuleType) -> FunctionValidationResult:
    log(f"Validating function: {fn.__module__}:{fn.__name__}")
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
    sig_return_type = type_to_string(sig.return_annotation)

    parser = config.get_parser()
    doc_parameters = parser.get_parameters(doc, module_type)
    doc_return_type = parser.get_return_type(doc, module_type)

    if sig_return_type.split(".")[-1] != doc_return_type:
        result.result = ResultType.FAILED
        result.fail_reason = f"Return type differ. Expected (from signature) {sig_return_type}, but got (in docs) {doc_return_type}."
        return result

    if len(sig_parameters) != len(doc_parameters):
        result.result = ResultType.FAILED
        result.fail_reason = f"Number of arguments differ. Expected (from signature) {len(sig_parameters)} arguments, but found (in docs) {len(doc_parameters)}."

    for sigparam, docparam in zip(sig_parameters, doc_parameters):
        if sigparam.name != docparam.name:
            result.result = ResultType.FAILED
            result.fail_reason = f"Argument name differ. Expected (from signature) '{sigparam.name}', but got (in docs) '{docparam.name}'"
            break

        # NOTE: Optional[str] == Union[str, None] # True
        if sigparam.type != docparam.type:
            result.result = ResultType.FAILED
            result.fail_reason = f"Argument type differ. Argument '{sigparam.name}' was expected (from signature) to have type '{sigparam.type}', but has (in docs) type '{docparam.type}'"
            break
    return result


def validate_class(class_instance: Any, config: Configuration, module_type: ModuleType) -> ClassValidationResult:
    log(f"Validating class: {class_instance}")
    class_result = ClassValidationResult(class_instance.__name__)
    for name, item in class_instance.__dict__.items():
        if isinstance(item, types.FunctionType):
            function_result = validate_function(item, config, module_type)
            if function_result.result == ResultType.FAILED:
                class_result.result = ResultType.FAILED
            class_result.function_results.append(function_result)
    return class_result
