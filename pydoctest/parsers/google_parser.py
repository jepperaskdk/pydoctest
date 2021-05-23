from types import ModuleType
from typing import List, Type

from pydoctest.parsers.parser import Parameter, Parser
from pydoctest.utilities import get_type_from_module


class GoogleParser(Parser):
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
            docname, tail = [x.strip() for x in arg_string.split('(')]
            doctype, tail = tail.split(':')
            doctype = doctype.replace(')', '')
            doctype = doctype.replace(', optional', '')  # TODO: How do we deal with Optional[int] being (Optional[int], optional)?
            located_type = get_type_from_module(doctype, module_type)
            parameters.append(Parameter(docname, located_type))
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

        return get_type_from_module(doctype, module_type)
