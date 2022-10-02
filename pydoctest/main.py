from enum import Enum
import sys
import os
import argparse
import pathlib
import inspect
import traceback

import importlib
import importlib.util
from importlib.abc import Loader
from importlib.machinery import ModuleSpec

from types import FunctionType, ModuleType
from typing import List, Optional, Type

from pydoctest import logging
from pydoctest.version import VERSION
from pydoctest.configuration import Configuration, Verbosity
from pydoctest.reporters.reporter import Reporter
from pydoctest.reporters.json_reporter import JSONReporter
from pydoctest.reporters.text_reporter import TextReporter
from pydoctest.validation import ModuleValidationResult, Result, ResultType, ValidationResult, validate_class, validate_function
from pydoctest.utilities import parse_cli_list

# We always want to exclude setup.py
DEFAULT_EXCLUDE_PATHS = [ "**/setup.py" ]

CONFIG_FILE_NAME = 'pydoctest.json'
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

    def validate(self, modules: Optional[List[str]] = None) -> ValidationResult:
        """Validate the found modules using the provided reporter.

        Args:
            modules (Optional[List[str]]): Optionally, specify directly the modules rather than discover.

        Returns:
            ValidationResult: Information about whether validation succeeded.
        """
        logging.log('Starting validating')
        result = ValidationResult()

        if modules is None:
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

        if not os.path.exists(module_path) or module_spec is None or not isinstance(module_spec.loader, Loader):
            result.result = ResultType.NOT_RUN
            result.fail_reason = f"Failed to load file from location: {module_path}"
            return result

        try:
            module_type = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module_type)
        except ModuleNotFoundError as e:
            result.result = ResultType.FAILED
            result.fail_reason = f"Failed to load module dependant module: {str(e)}"
            return result
        except Exception as e:
            result.result = ResultType.FAILED
            result.fail_reason = f"Failed to load module (possibly due to syntax errors): {module_path} - error: {str(e)}"
            return result

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

    def __is_excluded_path(self, path: pathlib.Path, exclude_paths: List[str]) -> bool:
        """
        Returns whether the found path is excluded by any of the exclude_paths.

        Args:
            path (pathlib.Path): The path to test
            exclude_paths (List[str]): The exclude paths

        Returns:
            bool: If path is excluded.
        """
        return any(path.match(e_p) for e_p in exclude_paths)

    def discover_modules(self) -> List[str]:
        """Discovers modules using the configuration include/exclude paths.

        Returns:
            List[str]: A list of paths to modules to be validated.
        """
        include_file_paths: List[str] = []

        include_paths = self.config.include_paths
        exclude_paths = self.config.exclude_paths + DEFAULT_EXCLUDE_PATHS

        for include_path in include_paths:
            path = pathlib.Path(self.config.working_directory)
            disovered_paths = list(path.glob(include_path))
            allowed_paths = [str(p) for p in disovered_paths if not self.__is_excluded_path(p, exclude_paths)]
            include_file_paths.extend(allowed_paths)

        return include_file_paths


def get_configuration(root_dir: str, config_path: Optional[str] = None) -> Configuration:
    """Searches for CONFIG_FILE_NAME in root_dir, unless a path is provided.

    Args:
        root_dir (str): The directory to search in.
        config_path (Optional[str]): [description]. Defaults to None.

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
    parser.add_argument("--version", help="Show version", action='store_true')
    parser.add_argument("--file", help="Analyze single file")
    parser.add_argument("--parser", help="Docstring format, either: google|sphinx|numpy")

    # TODO: Implement splitting by comma and
    parser.add_argument("--include-paths", help="Pattern to include paths by, defaults to \"**/*.py\"")
    parser.add_argument("--exclude-paths", help="Pattern to exclude paths by, defaults to \"**/__init__.py, **/setup.py\"")

    args = parser.parse_args()

    try:
        if args.version:
            print(VERSION)
            sys.exit(0)

        if args.debug:
            logging.set_verbose(True)

        config = get_configuration(os.getcwd(), args.config)

        # Imports will not work, unless we pretend this script is executed in the current directory.
        sys.path.insert(0, '')

        reporter = get_reporter(config, args.reporter)

        if args.verbosity:
            config.verbosity = Verbosity(int(args.verbosity))

        if args.parser:
            config.parser = args.parser

        if args.include_paths:
            config.include_paths = parse_cli_list(args.include_paths)

        if args.exclude_paths:
            config.exclude_paths = parse_cli_list(args.exclude_paths)

        # Check that parser exists before running.
        config.get_parser()

        ds = PyDoctestService(config)

        if args.file:
            result = ds.validate([os.path.abspath(args.file)])
        else:
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
