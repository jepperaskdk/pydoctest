from collections import deque
import inspect
import ast
import textwrap

from types import FunctionType, ModuleType
from typing import List, Type, cast

from pydoc import locate

from pydoctest.exceptions import UnknownTypeException


class LocateResult():
    """Small DTO for storing type and method used for finding it.
    Makes testing easier.
    """
    def __init__(self, t: Type, method: str) -> None:
        """Instantiates a new LocateResult

        Args:
            t (Type): The type returned.
            method (str): The method used to locate it.
        """
        self.type = t
        self.method = method


def get_type_from_module(type_string: str, module: ModuleType) -> LocateResult:
    """Attempts to return the type, given the type_string and module it is extracted from.

    Args:
        type_string (str): String version of a string, e.g. "Optional[str]"
        module (ModuleType): The module the type_string is extracted from.

    Raises:
        UnknownTypeException: If unable to find the type, we throw an Exception.

    Returns:
        LocateResult: A LocateResult wrapping the type when found.
    """
    # First let pydoc attempt to locate the type
    located_type: Type = cast(Type, locate(type_string))
    if located_type:
        return LocateResult(located_type, 'locate')

    # Try to eval it.
    try:
        # We pass the globals of module to eval, so lookups should work.
        t = eval(type_string, vars(module))
        return LocateResult(t, 'eval')
    except NameError:
        pass

    # Search imported modules in module
    # Inspired by this: https://stackoverflow.com/a/11781721/3717691
    # TODO: We limit the search by count, not by depth. Should it be configurable, e.g. when large codebases?
    SEARCHES_LEFT = 1_000
    q = deque([module])
    while q and SEARCHES_LEFT > 0:
        m = q.popleft()
        try:
            t = eval(type_string, vars(m))
            return LocateResult(t, 'deque')
        except NameError:
            pass

        for name, item in inspect.getmembers(m):
            if inspect.ismodule(item):
                q.append(item)
            elif inspect.isclass(item) and item.__module__ != module.__name__:
                mod = inspect.getmodule(item)
                if mod:
                    q.append(mod)
        SEARCHES_LEFT -= 1

    # TODO: We should make this configurable in config
    raise UnknownTypeException(f"Was unable to detect the type of: {type_string} from module: {module.__file__}.\nIf you believe this is a bug, please file it here: https://github.com/jepperaskdk/pydoctest/issues")


class RaiseVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        """A NodeVisitor which collects the id's of ast.Raise objects from parsing the function.
        """
        self.nodes: List[str] = []

    def visit(self, n: ast.AST) -> None:
        """Visits the node and if the node is an ast.Raise, we collect its id.

        Args:
            n (ast.AST): The node to test.

        """
        if isinstance(n, ast.Raise) and n.exc and isinstance(n.exc, ast.Call) and isinstance(n.exc.func, ast.Name):
            self.nodes.append(n.exc.func.id)
        super().visit(n)


def get_exceptions_raised(fn: FunctionType, module: ModuleType) -> List[str]:
    """Get exceptions raised in fn.

    NOTE: We currently only return exceptions explicitly raised by the function.
    This means, that exceptions raised from super-calls are not returned,
    and exceptions thrown by called functions in the function are not returned.

    Args:
        fn (FunctionType): The function to get raised exceptions from.
        module (ModuleType): The module in which the function is defined.

    Returns:
        List[str]: The list of exceptions thrown.
    """
    # TODO: How do we compile functions, without having to check indentation

    fn_source = inspect.getsource(fn)
    max_indents = 10

    # Try to parse, and if IndentationError, dedent up to 10 times.
    while max_indents > 0:
        try:
            tree = ast.parse(fn_source)
            break
        except IndentationError as e:
            fn_source = textwrap.dedent(fn_source)
            max_indents -= 1

    visitor = RaiseVisitor()
    visitor.generic_visit(tree)

    # Make sure we dont return duplicate exceptions
    return list(set(visitor.nodes))


def parse_cli_list(content: str, separator: str = ',') -> List[str]:
    """
    Parses a string-list by splitting on separator, trimming and removing empty results.

    Args:
        content (str): The string coming from a cli command.
        separator (str): The separator to split the list by. Defaults to ','.

    Returns:
        List[str]: The list-items.
    """
    items = content.split(separator)
    return [i.strip() for i in items if i]
