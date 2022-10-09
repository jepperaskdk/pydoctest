from collections import deque
import re
import inspect
import ast

from types import FunctionType, ModuleType
from typing import Any, List, Optional, Type, cast

from pydoc import locate

from pydoctest.exceptions import UnknownTypeException, ParseException


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


def dedent_from_first(source_string: str) -> str:
    """
    Simple method for dedenting code similar to textwrap.dedent.
    A problem with textwrap.dedent is that it only removes common leading whitespace,
    which is not enough when a function has multilinestrings that has no leading whitespace.

    This function dedents the entire source_string, based on the whitespace/tabs in the first line (i.e. the 'def').

    Args:
        source_string (str): The source code string to dedent.

    Returns:
        str: The source code string dedented once.
    """
    def get_leading_indents(s: str) -> int:
        return len(s) - len(s.lstrip())

    if get_leading_indents(source_string) == 0:
        return source_string

    lines = source_string.splitlines()
    if len(lines) == 0:
        return source_string

    first_leading_indents = get_leading_indents(lines[0])
    for i, line in enumerate(lines):
        if get_leading_indents(line) != 0:
            lines[i] = line[first_leading_indents:]

    return '\n'.join(lines)


def get_exceptions_raised(fn: FunctionType, module: ModuleType) -> List[str]:
    """Get exceptions raised in fn.

    NOTE: We currently only return exceptions explicitly raised by the function.
    This means, that exceptions raised from super-calls are not returned,
    and exceptions thrown by called functions in the function are not returned.

    Args:
        fn (FunctionType): The function to get raised exceptions from.
        module (ModuleType): The module in which the function is defined.

    Raises:
        ParseException: If failing to parse the AST of the source code.

    Returns:
        List[str]: The list of exceptions thrown.
    """
    fn_source = inspect.getsource(fn)

    tree: Optional[Any] = None
    # Try to parse, and if IndentationError, dedent.
    for _ in range(2):
        try:
            tree = ast.parse(fn_source)
            break
        except IndentationError as e:
            fn_source = dedent_from_first(fn_source)

    if tree is None:
        raise ParseException("Failed to parse function source code to detect raised exceptions")

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


def pattern_matches(pattern: str, test_string: str) -> bool:
    """
    Returns whether the string matches the pattern.
    Inspired by this answer, by Mathew Wicks (and Nizam Mohamed): https://stackoverflow.com/a/72400344/3717691

    pathlib.Path.match and fnmatch incorrectly returns recursive results for e.g. *.py.

    Args:
        pattern (str): The pattern, e.g. "**/*.py"
        test_string (str): The string being tested, e.g. "a/b/c/abc.py"

    Returns:
        bool: If test_string is matched by pattern.
    """
    i, n = 0, len(pattern)
    res = ''
    while i < n:
        c = pattern[i]
        i = i + 1
        if c == '*':
            j = i
            if j < n and pattern[j] == '*':
                res = res + '.*/?'
                i = j + 2
            else:
                res = res + '[^/]*'
        else:
            res = res + re.escape(c)
    regex = r'(?s:%s)\Z' % res
    glob_re = re.compile(regex)
    return bool(glob_re.match(test_string))


def is_excluded_path(path: str, exclude_paths: List[str]) -> bool:
    """
    Returns whether the found path is excluded by any of the exclude_paths.

    Args:
        path (str): The path to test
        exclude_paths (List[str]): The exclude paths

    Returns:
        bool: If path is excluded.
    """
    return any(pattern_matches(e_p, path) for e_p in exclude_paths)


def is_excluded_class(class_name: str, exclude_classes: List[str]) -> bool:
    """
    Returns whether the class is excluded by any of the exclude_classes patterns.

    Args:
        class_name (str): The class_name to test
        exclude_classes (List[str]): The exclude class patterns

    Returns:
        bool: If class is excluded.
    """
    return any(pattern_matches(e_p, class_name) for e_p in exclude_classes)


def is_excluded_function(function_name: str, exclude_functions: List[str]) -> bool:
    """
    Returns whether the function (or method) is excluded by any of the exclude_functions patterns.

    Args:
        function_name (str): The function_name to test
        exclude_functions (List[str]): The exclude function patterns

    Returns:
        bool: If function is excluded.
    """
    return any(pattern_matches(e_p, function_name) for e_p in exclude_functions)
