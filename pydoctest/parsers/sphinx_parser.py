import re

from types import ModuleType
from typing import List, Optional, Type

from pydoctest.parsers.parser import Parameter, Parser
from pydoctest.utilities import get_type_from_module
from pydoctest.exceptions import ParseException

"""
Based on this style guide:
https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html

"""


class SphinxParser(Parser):
    def __init__(self) -> None:
        """Parser for Sphinx docstring style."""
        super().__init__()
        self.parameter_name_regex = re.compile(r":param\s+(\w+):")
        self.parameter_type_regex = re.compile(r":type\s+\w+:\s*([\w\[\], ]+)")
        self.return_type_regex = re.compile(r":rtype:\s*([\w\[\], ]+)")
        self.raises_regex = re.compile(r":raises\s+(\w+):")

    def get_exceptions_raised(self, doc: str) -> List[str]:
        """Returns the exceptions listed as raised in the docstring.

        Args:
            doc (str): The docstring to analyze.

        Raises:
            ParseException: Raised if any error happens during parsing.

        Returns:
            List[str]: List of exceptions raised.
        """
        try:
            raised_exceptions: List[str] = []
            for line in doc.split('\n'):
                match = self.raises_regex.match(line)
                if match is None:
                    continue
                doctype = match.groups()[0]
                raised_exceptions.append(doctype)
            return raised_exceptions
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
        try:
            # Find first occurance of :param, :type, :return, :rtype, :raises
            indices = [doc.find(x) for x in [':param', ':type', ':return', ':rtype', ':raises'] if doc.find(x) >= 0]
            if len(indices) == 0:
                return doc if len(doc) > 0 else None

            min_index = min(indices)
            summary = doc[0: min_index].rstrip()
            return summary if len(summary) > 0 else None
        except Exception as e:
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
        try:
            lines = doc.split('\n')
            parameters: List[Parameter] = []
            var_name: Optional[str] = None
            for line in lines:
                if var_name is None:
                    match = self.parameter_name_regex.match(line)
                    if match is not None:
                        var_name = match.groups()[0]
                else:
                    match = self.parameter_type_regex.match(line)
                    if match is not None:
                        var_type = match.groups()[0]
                        located_type = get_type_from_module(var_type, module_type)
                        parameters.append(Parameter(var_name, located_type.type))
                        var_name = None
            if var_name is not None:
                # There must have been an error parsing :type:
                raise ParseException()

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
        try:
            for line in doc.split('\n'):
                match = self.return_type_regex.match(line)
                if match is None:
                    continue
                doctype = match.groups()[0]
                return get_type_from_module(doctype, module_type).type
            return type(None)
        except Exception:
            raise ParseException()
