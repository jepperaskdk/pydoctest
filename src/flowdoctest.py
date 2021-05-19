import sys
import os
import importlib
from typing import List


def log(message: str) -> None:
    print(message)


class Reporter():
    pass


class JSONReporter(Reporter):
    pass


class TextReporter(Reporter):
    pass


class ConfigParser():
    pass


class ValidationResult():
    def __init__(self) -> None:
        self.success: bool = False
        self.module_results: List[ModuleValidationResult] = []


class ModuleValidationResult():
    def __init__(self) -> None:
        pass


class ClassValidationResult():
    def __init__(self) -> None:
        pass


class FunctionValidationResult():
    def __init__(self) -> None:
        pass


class DoctestService():
    def __init__(self, reporter: Reporter, config: ConfigParser) -> None:
        self.reporter = reporter
        self.config = config

    def validate(self) -> ValidationResult:
        """Validate the found modules using the provided reporter.

        Returns:
            ValidationResult: Information about whether validation succeeded.
        """
        log('Starting validating')
        result = ValidationResult()

        modules = self.discover_modules()

        for module in modules:
            module_result = self.validate_module(module)
            result.module_results.append(module_result)

        return result

    def validate_module(self, module_path: str) -> ModuleValidationResult:
        log(f'Validating module: {module_path}')
        result = ModuleValidationResult()

        module_name = os.path.basename(module_path)
        module = importlib.import_module(module_name, module_path)

        # Validate top-level functions in module
        # log(module)
        # Validate top-level classes in module

        return result

    def discover_modules(self) -> List[str]:
        return [os.path.abspath(p) for p in os.listdir('.') if p.endswith('.py')]


def main() -> None:
    reporter = JSONReporter()
    config = ConfigParser()
    ds = DoctestService(reporter, config)
    result = ds.validate()
    print(result)

    # return 0 if validation succeeds
    sys.exit(0 if result else 1)


if __name__ == '__main__':
    main()
