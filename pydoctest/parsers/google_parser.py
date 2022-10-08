import re
from types import ModuleType
from typing import Dict, List, Optional, Type

from pydoctest.parsers.parser import Parameter, Parser, Section
from pydoctest.utilities import get_type_from_module
from pydoctest.exceptions import ParseException, UnknownTypeException


SECTION_NAMES = {
    Section.ARGUMENTS: "Args:",
    Section.RAISES: "Raises:",
    Section.RETURNS: "Returns:",
}

# Regex matches [name] ([type]): [description] with some extra whitespace
# e.g. this would also match: a      (  int   )   :    kmdkfmdf
# It terminates with .* meaning a new match is the terminator. This should support multiline descriptions without having to consider tabs/indentation.
ARGUMENT_REGEX = re.compile(r"\s*(?P<name>(\w+))\s*\((?P<type>[\w\.\[\], \']+)\)\s*:(.*)")


class GoogleParser(Parser):

    def __get_sections(self, doc: str) -> Dict[Section, str]:
        """
        Splits the docstring into sections.

        Args:
            doc (str): The docstring.

        Returns:
            Dict[Section, str]: A map from section-type to section-string.
        """
        result: Dict[Section, str] = {}
        indices = [(section, doc.index(name)) for section, name in SECTION_NAMES.items() if name in doc]
        sections_sorted = sorted(indices, key=lambda kv: kv[1])

        if len(sections_sorted) > 0:
            result[Section.SUMMARY] = doc[:sections_sorted[0][1]]
        else:
            result[Section.SUMMARY] = doc

        for i in range(len(sections_sorted)):
            section, index = sections_sorted[i]

            if i == len(sections_sorted) - 1:
                # Last section
                result[section] = doc[index:]
            else:
                # Has section after, so use following section's index as stop index
                result[section] = doc[index:sections_sorted[i + 1][1]]

        # Make sure we didn't lose any characters
        assert sum(len(s) for s in result.values()) == len(doc)

        return result

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

        sections = self.__get_sections(doc)
        if Section.ARGUMENTS not in sections:
            return []

        parameters = []

        for match in re.finditer(ARGUMENT_REGEX, sections[Section.ARGUMENTS]):
            start, end = match.span()
            name = match.group('name').strip()
            type = match.group('type').strip()

            try:
                located_type = get_type_from_module(type, module_type)
                parameters.append(Parameter(name, located_type.type))
            except UnknownTypeException:
                raise ParseException(f"Unknown type '{type}' in '{sections[Section.ARGUMENTS][start:end].strip()}'")
            except Exception:
                raise ParseException(sections[Section.ARGUMENTS][start:end].strip())

        # If we have an Args section, but no parameters, we must have failed to parse
        if len(parameters) == 0:
            raise ParseException()

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
