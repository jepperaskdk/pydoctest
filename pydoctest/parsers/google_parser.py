import re
import inspect
from pydoc import locate
from types import ModuleType
from typing import List, Tuple, Type, cast
from pydoctest.parsers.parser import Parameter, Parser
from collections import deque


# TODO: Move this out of google_parser, and into a utilities module
def get_type_from_module(type_string: str, module: ModuleType) -> Type:
    # First let pydoc attempt to locate the type
    located_type: Type = cast(Type, locate(type_string))
    if located_type:
        return located_type

    # Try to eval it.
    try:
        # We pass the globals of module to eval, so lookups should work.
        t = eval(type_string, vars(module))
        return t
    except NameError:
        pass

    # Search the module for the type. The above may be good enough.
    for name, typ in inspect.getmembers(module):
        if name == type_string:
            return typ

    raise Exception(f"Was unable to detect the type of: {type_string} from module: {module.__file__}.\nPlease file this as a bug: https://github.com/jepperaskdk/pydoctest/issues")


class GoogleParser(Parser):
    def get_parameters(self, doc: str, module_type: ModuleType) -> List[Parameter]:
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
        if 'Returns:' not in doc:
            return type(None)

        _, tail = doc.split("Returns:")
        if 'Raises:' in tail:
            returns, raises = tail.split("Raises:")
        else:
            returns = tail
        if ':' in returns:
            doctype, _ = returns.strip().split(":")
        else:
            doctype = returns.strip()

        return get_type_from_module(doctype, module_type)
