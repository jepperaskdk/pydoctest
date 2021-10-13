import re

from types import ModuleType
from typing import List, Optional, Type

from pydoctest.parsers.parser import Parameter, Parser
from pydoctest.utilities import get_type_from_module
from pydoctest.exceptions import ParseException

"""
Based on this style guide:
https://numpydoc.readthedocs.io/en/latest/format.html

It doesn't currently mention a version, but there's an issue on that now:
https://github.com/numpy/numpydoc/issues/333

"""


class NumpyParser(Parser):
    def __init__(self) -> None:
        """Parser for Numpy docstring style."""
        super().__init__()
        self.section_headers = [
            # Rest are not supported (Yields, See Also, Warns, Warnings, Receives)
            'Parameters', 'Returns', 'Raises',
        ]
        # Split by word, newline, a number of '-' and newline
        self.section_regex = re.compile("([a-zA-Z]+)\n[-]+\n")
        self.parameter_regex = re.compile(r"(\w+)\s*:\s*([\w\[\], ]+)")
        self.returns_with_name_regex = re.compile(r"(\w+)\s*:\s*([\w\[\], ]+)")

    def get_exceptions_raised(self, doc: str) -> List[str]:
        """Returns the exceptions listed as raised in the docstring.

        Args:
            doc (str): The docstring to analyze.

        Raises:
            ParseException: Raised if any error happens during parsing.

        Returns:
            List[str]: List of exceptions raised.
        """
        if 'Raises' not in doc:
            return []
        try:
            splits = self.section_regex.split(doc)
            raises_idx = splits.index('Raises')
            if raises_idx == -1 or len(splits) < raises_idx + 1:
                raise ParseException()

            exception_section = splits[raises_idx + 1]

            exceptions_raised: List[str] = []
            for exn_line in exception_section.split('\n'):
                # Heuristic: Assume errors-types are not indented and descriptions are.
                if not exn_line.startswith(' '):
                    exceptions_raised.append(exn_line)

            return exceptions_raised
        except Exception:
            raise ParseException()

    def get_summary(self, doc: str, module_type: ModuleType) -> Optional[str]:
        """Returns the summary part of the docstring.

        Args:
            doc (str): The docstring to analyze.
            module_type (ModuleType): The module it was extracted from.

        Raises:
            ParseException: Raised if any error happens during parsing.

        Returns:
            Optional[str]: The summary, if it exists.
        """
        if len(doc) == 0:
            return None

        try:
            splits = self.section_regex.split(doc)

            if len(splits) > 0 and splits[0] not in self.section_headers:
                return splits[0]

            return None
        except Exception:
            raise ParseException()

    def get_parameters(self, doc: str, module_type: ModuleType) -> List[Parameter]:
        """Finds the function arguments as strings, and returns their types as Parameter instances.

        Args:
            doc (str): Function docstring.
            module_type (ModuleType): The module the docstring was extracted from.

        Raises:
            ParseException: Raised if any error happens during parsing.

        Returns:
            List[Parameter]: The parameters parsed from the docstring.
        """
        if 'Parameters' not in doc:
            return []
        try:
            splits = self.section_regex.split(doc)
            parameters_idx = splits.index('Parameters')
            if parameters_idx == -1 or len(splits) < parameters_idx + 1:
                raise ParseException()

            parameters_section = splits[parameters_idx + 1]
            matches = self.parameter_regex.findall(parameters_section)

            # If we have a parameters section with text, but no matches, we must have bad formatting
            if len(parameters_section) > 0 and len(matches) == 0:
                raise ParseException()

            parameters: List[Parameter] = []
            for param_name, param_type in matches:
                located_type = get_type_from_module(param_type, module_type)
                parameters.append(Parameter(param_name, located_type.type))
            return parameters
        except Exception:
            raise ParseException()

    def get_return_type(self, doc: str, module_type: ModuleType) -> Type:
        """Base method for Parsers to return the return-type of a function from its docstring.

        Args:
            doc (str): Function docstring.
            module_type (ModuleType): The module the docstring was extracted from.

        Raises:
            ParseException: Raised if an exception occurs during parsing

        Returns:
            Type: The return type parsed from the docs.
        """
        # TODO: Use section split regex so we know 'Returns' is not just a random word in docstring, but actually a section header
        if 'Returns' not in doc:
            return type(None)

        try:
            splits = self.section_regex.split(doc)
            parameters_idx = splits.index('Returns')
            if parameters_idx == -1 or len(splits) < parameters_idx + 1:
                raise ParseException()

            returns_section = splits[parameters_idx + 1]
            returns_line = returns_section.split('\n')[0]

            # Test for line with name/type combo
            if ':' in returns_line:
                match = self.returns_with_name_regex.match(returns_line)
                if match is not None:
                    name, doctype = match.groups()
                else:
                    raise ParseException()
            else:
                doctype = returns_line.rstrip('\n')

            return get_type_from_module(doctype, module_type).type
        except Exception:
            raise ParseException()
