from enum import Enum
import sys
import os
import argparse
import glob
import inspect
import traceback

import importlib
import importlib.util
from importlib.abc import Loader
from importlib.machinery import ModuleSpec

from types import FunctionType, ModuleType
from typing import List, Optional, Type

from pydoctest import logging
from pydoctest.configuration import Configuration, Verbosity
from pydoctest.reporters.reporter import Reporter
from pydoctest.reporters.json_reporter import JSONReporter
from pydoctest.reporters.text_reporter import TextReporter
from pydoctest.validation import ModuleValidationResult, Result, ResultType, ValidationResult, validate_class, validate_function


CONFIG_FILE_NAME = 'pydoctest.json'
IGNORE_FILES = [ '__init__.py', 'setup.py' ]
REPORTERS = {
    'json': JSONReporter,
    'text': TextReporter
}


class PyDoctestService():
    def __init__(self, config: Configuration) -> None:
        """Instantiates a new Pydoctest-service.

        Args:
            config (Configuration): The configuration to use for testing.
        """
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

        if result.result == ResultType.NOT_RUN:
            result.result = ResultType.OK

        return result

    def validate_module(self, module_path: str) -> ModuleValidationResult:
        """Validates the module, given its path.

        Args:
            module_path (str): Path to a module.

        Returns:
            ModuleValidationResult: Result of validating the module.
        """
        logging.log(f'Validating module: {module_path}')
        result = ModuleValidationResult(module_path)

        module_name = os.path.basename(module_path)
        module_spec: Optional[ModuleSpec] = importlib.util.spec_from_file_location(module_name, module_path)

        if module_spec is None or not isinstance(module_spec.loader, Loader):
            result.result = ResultType.NOT_RUN
            result.fail_reason = f"Failed to load spec from file location: {module_path}"
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
            class_result = validate_class(cl, self.config, module_type)
            if class_result.result == ResultType.FAILED:
                result.result = ResultType.FAILED
            result.class_results.append(class_result)

        return result

    def get_global_functions(self, module: ModuleType) -> List[FunctionType]:
        """Gets the global functions of the module.

        Args:
            module (ModuleType): The module to extract global functions from.

        Returns:
            List[FunctionType]: A list of global functions in the module.
        """
        fns = []
        for name, obj in inspect.getmembers(module, lambda x: inspect.isfunction(x) and x.__module__ == module.__name__):
            fns.append(obj)
        return fns

    def get_classes(self, module: ModuleType) -> List[Type]:
        """Get classes defined in module.

        Args:
            module (ModuleType): The module to extract classes from.

        Returns:
            List[Type]: A list of classes defined in the module.
        """
        classes: List[type] = []
        # getmembers will also return imports etc. so we require classes to be part of this module
        for name, obj in inspect.getmembers(module, lambda x: inspect.isclass(x) and x.__module__ == module.__name__):
            if issubclass(obj, Enum):
                # Ignore enums
                continue
            classes.append(obj)
        return classes

    def discover_modules(self) -> List[str]:
        """Discovers modules using the configuration include/exclude paths.

        Returns:
            List[str]: A list of paths to modules to be validated.
        """
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
        # TODO: Is the interface better by returning Optional[Configuration] (None here)?
        # Then it is clearer that a config was not found.
        return Configuration.get_default_configuration(root_dir)

    path = os.path.join(root_dir, config_paths[0])
    return Configuration.get_configuration_from_path(path)


def get_reporter(config: Configuration, reporter: Optional[str] = None) -> Reporter:
    """We offer to output results using either TextReporter and JSONReporter.
    This list of reporters can be extended with more reporters as they simply implement a get_output function.

    Args:
        config (Configuration): The configuration currently used.
        reporter (Optional[str]): Desired reporter [text | json]

    Raises:
        Exception: Raised if desired reporter does not exist.

    Returns:
        Reporter: Reporter if provided, otherwise text.
    """
    if reporter is None:
        return REPORTERS['text'](config)

    if reporter in REPORTERS.keys():
        return REPORTERS[reporter](config)
    else:
        raise Exception(f"Unknown reporter: {reporter}. Please use one of the following: {', '.join(REPORTERS.keys())}")


def main() -> None:  # pragma: no cover
    """Main function invoked when running script.
    """
    # TODO: Could allow arguments directly to pydoctest for overriding .json config arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path to config JSON file, e.g. pydoctest.json")
    parser.add_argument("--reporter", help="Reporter to use, either 'json' or 'text'")
    parser.add_argument("--verbosity", help="0 = quiet, 1 = show failed, 2 = show all")
    parser.add_argument("--debug", help="Verbose logging", action='store_true')
    args = parser.parse_args()

    try:
        if args.debug:
            logging.set_verbose(True)

        config = get_configuration(os.getcwd(), args.config)
        reporter = get_reporter(config, args.reporter)

        if args.verbosity:
            config.verbosity = Verbosity(int(args.verbosity))

        # Check that parser exists before running.
        config.get_parser()

        ds = PyDoctestService(config)
        result = ds.validate()

        output = reporter.get_output(result)

        if isinstance(reporter, TextReporter) and config.verbosity != Verbosity.QUIET:
            counts = result.get_counts()
            output += f"Tested {counts.get_total()} function(s) across {counts.module_count} module(s).\n"
            output += f"Succeeded: {counts.functions_succeeded}, Failed: {counts.functions_failed}, Skipped: {counts.functions_skipped}"

        print(output)

        if result.result != ResultType.OK:
            sys.exit(1)
    except Exception as e:
        print(traceback.format_exc())
        print(f"Error occurred: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
