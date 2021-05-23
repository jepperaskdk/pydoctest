from enum import Enum
import sys
import os
import argparse
import glob
import inspect

import importlib
import importlib.util
from importlib.abc import Loader
from importlib.machinery import ModuleSpec

from types import FunctionType, ModuleType
from typing import Any, ClassVar, List, Optional

from pydoctest import logging
from pydoctest.configuration import Configuration, Verbosity
from pydoctest.reporters.reporter import Reporter
from pydoctest.reporters.json_reporter import JSONReporter
from pydoctest.reporters.text_reporter import TextReporter
from pydoctest.validation import ClassValidationResult, FunctionValidationResult, ModuleValidationResult, ResultType, ValidationResult, validate_class, validate_function


CONFIG_FILE_NAME = 'pydoctest.json'
IGNORE_FILES = [ '__init__.py', 'setup.py' ]
REPORTERS = {
    'json': JSONReporter,
    'text': TextReporter
}


class PyDoctestService():
    def __init__(self, config: Configuration) -> None:
        self.config = config

    def validate(self) -> ValidationResult:
        """Validate the found modules using the provided reporter.

        Returns:
            ValidationResult: Information about whether validation succeeded.
        """
        logging.log('Starting validating')
        result = ValidationResult()

        modules = self.discover_modules()
        logging.log(f'Found {len(modules)} modules')

        for module in modules:
            module_result = self.validate_module(module)
            if module_result.result == ResultType.FAILED:
                result.result = ResultType.FAILED
            result.module_results.append(module_result)

        return result

    def validate_module(self, module_path: str) -> ModuleValidationResult:
        logging.log(f'Validating module: {module_path}')
        result = ModuleValidationResult(module_path)

        module_name = os.path.basename(module_path)
        module_spec: Optional[ModuleSpec] = importlib.util.spec_from_file_location(module_name, module_path)

        if module_spec is None or not isinstance(module_spec.loader, Loader):
            result.result = ResultType.NOT_RUN
            result.fail_reason = "Failed to load spec from file location"
            return result

        module_type = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module_type)

        # Validate top-level functions in module
        fns = self.get_global_functions(module_type)
        for fn in fns:
            function_result = validate_function(fn, self.config, module_type)
            if function_result.result == ResultType.FAILED:
                result.result = ResultType.FAILED
            result.function_results.append(function_result)

        # Validate top-level classes in module
        classes = self.get_classes(module_type)
        for cl in classes:
            result.class_results.append(validate_class(cl, self.config, module_type))

        return result

    def get_global_functions(self, module: ModuleType) -> List[FunctionType]:
        fns = []
        for name, obj in inspect.getmembers(module, lambda x: inspect.isfunction(x) and x.__module__ == module.__name__):
            fns.append(obj)
        return fns

    def get_classes(self, module: ModuleType) -> List[FunctionType]:
        classes = []
        # getmembers will also return imports etc. so we require classes to be part of this module
        for name, obj in inspect.getmembers(module, lambda x: inspect.isclass(x) and x.__module__ == module.__name__):
            if issubclass(obj, Enum):
                # Ignore enums
                continue
            classes.append(obj)
        return classes

    def discover_modules(self) -> List[str]:
        include_file_paths = []

        paths = self.config.include_paths
        if len(paths) == 0:
            paths = [ "*.py" ]

        for path in paths:
            include_path = os.path.join(self.config.working_directory, path)
            # Remove IGNORE_FILES until we know what to do with them
            # TODO: Implement exclude_paths. Test with fnmatch so we don't have to glob all exclude files?
            include_file_paths.extend([p for p in glob.glob(include_path) if not any([p.endswith(k) for k in IGNORE_FILES])])

        return include_file_paths


def get_configuration(root_dir: str, config_path: Optional[str] = None) -> Configuration:
    """Searches for CONFIG_FILE_NAME in root_dir, unless a path is provided.

    Args:
        root_dir (str): The directory to search in.
        config_path (Optional[str], optional): [description]. Defaults to None.

    Returns:
        Configuration: Either a configuration matching the specified/found one, or a default one.
    """
    if config_path:
        return Configuration.get_configuration_from_path(config_path)

    config_paths = [p for p in os.listdir(root_dir) if p == CONFIG_FILE_NAME]
    if len(config_paths) == 0:
        return Configuration.get_default_configuration()

    return Configuration.get_configuration_from_path(config_paths[0])


def get_reporter(reporter: Optional[str], config: Configuration) -> Reporter:
    """We offer to output results using either TextReporter and JSONReporter.
    This list of reporters can be extended with more reporters as they simply implement a get_output function.

    Args:
        reporter (Optional[str]): Desired reporter [text | json]
        config (Configuration): The configuration currently used.

    Returns:
        Reporter: Reporter if provided, otherwise text.
    """
    if reporter is None:
        return REPORTERS['text'](config)

    if reporter in REPORTERS.keys():
        return REPORTERS[reporter](config)
    else:
        print(f"Unknown reporter: {reporter}. Please use one of the following: {', '.join(REPORTERS.keys())}")
        sys.exit(1)


def main() -> None:
    """Main function invoked when running script.
    """
    # TODO: Could allow arguments directly to pydoctest for overriding .json config arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path to config JSON file, e.g. pydoctest.json")
    parser.add_argument("--reporter", help="Reporter to use, either 'json' or 'text'")
    parser.add_argument("--verbosity", help="0 = quiet, 1 = show failed, 2 = show all")
    parser.add_argument("--debug", help="Verbose logging", action='store_true')
    args = parser.parse_args()

    if args.debug:
        logging.set_verbose(True)

    config = get_configuration(os.getcwd(), args.config)
    reporter = get_reporter(args.reporter, config)

    if args.verbosity:
        config.verbosity = Verbosity(int(args.verbosity))

    # Validates fields, e.g. if parser exists
    config.validate()

    ds = PyDoctestService(config)
    result = ds.validate()

    if config.verbosity != Verbosity.QUIET:
        output = reporter.get_output(result)
        counts = result.get_counts()
        output += f"Tested {counts.get_total()} function(s) across {counts.module_count} module(s).\n"
        output += f"Succeeded: {counts.functions_succeeded}, Failed: {counts.functions_failed}, Skipped: {counts.functions_skipped}"
        print(output)

    # return 0 if validation succeeds
    sys.exit(0 if result.result == ResultType.OK else 1)


if __name__ == '__main__':
    main()
