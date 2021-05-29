from types import ModuleType
from typing import List, Optional, Type

from pydoctest.parsers.parser import Parameter, Parser
from pydoctest.utilities import get_type_from_module
from pydoctest.exceptions import ParseException


class GoogleParser(Parser):
    def get_summary(self, doc: str, module_type: ModuleType) -> Optional[str]:
        """Returns the summary part of the docstring.

        Args:
            doc (str): The docstring to analyze.
            module_type (ModuleType): The module it was extracted from.

        Returns:
            Optional[str]: The summary, if it exists.
        """
        for needle in [ 'Args:', 'Raises:', 'Returns:' ]:
            if needle in doc:
                summ, _ = doc.split(needle)
                summary = summ.strip()
                return summary if len(summary) > 0 else None

        if len(doc) > 0:
            return doc.strip()

        return None

    def get_parameters(self, doc: str, module_type: ModuleType) -> List[Parameter]:
        """Finds the function arguments as strings, and returns their types as Parameter instances.

        Args:
            doc (str): Function docstring.
            module_type (ModuleType): The module the docstring was extracted from.

        Returns:
            List[Parameter]: The parameters parsed from the docstring.
        """
        if 'Args:' not in doc:
            return []
        _, tail = doc.split("Args:")

        if 'Returns:' in tail:
            arguments_string, _ = tail.split('Returns:')
        else:
            arguments_string = tail

        if 'Raises' in arguments_string:
            arguments_string, _ = tail.split('Raises:')

        # TODO: Improve this. We might encounter more newlines.
        # Google styleguide appears to suggest using tab-indents for separating arguments
        # Could perhaps regex for NAME (TYPE): DESCRIPTION
        args_strings = [arg.strip() for arg in arguments_string.strip().split("\n")]

        parameters = []
        for arg_string in args_strings:
            try:
                docname, tail = [x.strip() for x in arg_string.split('(')]
                doctype, tail = tail.split(':')
                doctype = doctype.replace(')', '')
                doctype = doctype.replace(', optional', '')  # TODO: How do we deal with Optional[int] being (Optional[int], optional)?
                located_type = get_type_from_module(doctype, module_type)
                parameters.append(Parameter(docname, located_type.type))
            except ValueError:
                raise ParseException(arg_string)
        return parameters

    def get_return_type(self, doc: str, module_type: ModuleType) -> Type:
        """Finds the return-type as string and returns it.

        Args:
            doc (str): Function docstring.
            module_type (ModuleType): The module the docstring was extracted from.

        Returns:
            Type: The return type parsed from the docs.
        """
        if 'Returns:' not in doc:
            return type(None)

        _, returns = doc.split("Returns:")

        doctype, _ = returns.strip().split(":")

        return get_type_from_module(doctype, module_type).type
