from types import ModuleType
from typing import List, Optional, Type

from pydoctest.parsers.parser import Parameter, Parser
from pydoctest.utilities import get_type_from_module
from pydoctest.exceptions import ParseException


class GoogleParser(Parser):
    def get_exceptions_raised(self, doc: str) -> List[str]:
        """Returns the exceptions listed as raised in the docstring.

        Args:
            doc (str): The docstring to analyze.

        Raises:
            ParseException: If unable to parse an argument-line.

        Returns:
            List[str]: List of exceptions raised.
        """
        if 'Raises:' not in doc:
            return []

        try:
            _, tail = doc.split('Raises:')

            if 'Returns:' in tail:
                exceptions, returns = tail.split('Returns:')
            else:
                exceptions = tail

            exceptions_raised: List[str] = []
            for exc_line in [x.strip() for x in exceptions.split("\n") if x]:
                if ':' in exc_line:
                    exceptions_raised.append(exc_line.split(":")[0])
                else:
                    raise ParseException(exc_line)

            return exceptions_raised
        except Exception:
            raise ParseException()

    def get_summary(self, doc: str, module_type: ModuleType) -> Optional[str]:
        """Returns the summary part of the docstring.

        Args:
            doc (str): The docstring to analyze.
            module_type (ModuleType): The module it was extracted from.

        Raises:
            ParseException: If unable to parse an argument-line.

        Returns:
            Optional[str]: The summary, if it exists.
        """
        try:
            for needle in [ 'Args:', 'Raises:', 'Returns:' ]:
                if needle in doc:
                    summ, _ = doc.split(needle)
                    summary = summ.strip()
                    return summary if len(summary) > 0 else None

            if len(doc) > 0:
                return doc.strip()

            return None

        except Exception:
            raise ParseException()

    def get_parameters(self, doc: str, module_type: ModuleType) -> List[Parameter]:
        """Finds the function arguments as strings, and returns their types as Parameter instances.

        Args:
            doc (str): Function docstring.
            module_type (ModuleType): The module the docstring was extracted from.

        Raises:
            ParseException: If unable to parse an argument-line.

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

        if 'Raises:' in arguments_string:
            arguments_string, _ = tail.split('Raises:')

        # TODO: Improve this. We might encounter more newlines.
        # Google styleguide appears to suggest using tab-indents for separating arguments
        # Could perhaps regex for NAME (TYPE): DESCRIPTION
        args_strings = [arg.strip() for arg in arguments_string.strip().split("\n")]

        parameters = []
        for arg_string in args_strings:
            try:
                docname, tail = [x.strip() for x in arg_string.split('(', maxsplit=1)]
                doctype, tail = tail.split(':')
                doctype = doctype.replace(')', '')
                doctype = doctype.replace(', optional', '')  # TODO: How do we deal with Optional[int] being (Optional[int], optional)?
                located_type = get_type_from_module(doctype, module_type)
                parameters.append(Parameter(docname, located_type.type))
            except ValueError:
                raise ParseException(arg_string)
            except Exception:
                raise ParseException(arg_string)
        return parameters

    def get_return_type(self, doc: str, module_type: ModuleType) -> Type:
        """Finds the return-type as string and returns it.

        Args:
            doc (str): Function docstring.
            module_type (ModuleType): The module the docstring was extracted from.

        Raises:
            ParseException: If unable to parse the return type line.

        Returns:
            Type: The return type parsed from the docs.
        """
        try:
            if 'Returns:' not in doc:
                return type(None)

            _, returns = doc.split("Returns:")
            try:
                doctype, _ = returns.strip().split(":")
            except ValueError:
                raise ParseException(returns)

            return get_type_from_module(doctype, module_type).type
        except Exception:
            raise ParseException()
