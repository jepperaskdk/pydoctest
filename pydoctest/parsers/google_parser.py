import re

from typing import List, Type
from pydoctest.parsers.parser import Parameter, Parser


class GoogleParser(Parser):
    def get_parameters(self, doc: str) -> List[Parameter]:
        if 'Args:' not in doc:
            return []
        _, tail = doc.split("Args:")
        arguments_string, _ = tail.split("Returns:")

        # TODO: Improve this. We might encounter more newlines.
        # Could perhaps regex for NAME (TYPE): DESCRIPTION
        args_strings = [arg.strip() for arg in arguments_string.strip().split("\n")]

        parameters = []
        for arg_string in args_strings:
            docname, tail = [x.strip() for x in arg_string.split('(')]
            doctype, tail = tail.split(':')
            doctype = doctype.replace(')', '')
            doctype = doctype.replace(', optional', '')  # TODO: How do we deal with Optional[int] being (Optional[int], optional)?
            parameters.append(Parameter(docname, doctype))
        return parameters

    def get_return_type(self, doc: str) -> str:
        if 'Returns:' not in doc:
            return "None"

        _, tail = doc.split("Returns:")
        if 'Raises:' in tail:
            returns, raises = tail.split("Raises:")
        else:
            returns = tail
        if ':' in returns:
            doctype, _ = returns.strip().split(":")
        else:
            doctype = returns.strip()
        return doctype
