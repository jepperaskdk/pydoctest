from collections import deque
import inspect
from types import ModuleType
from typing import Type, cast

from pydoc import locate


def get_type_from_module(type_string: str, module: ModuleType) -> Type:
    """Attempts to return the type, given the type_string and module it is extracted from.

    Args:
        type_string (str): String version of a string, e.g. "Optional[str]"
        module (ModuleType): The module the type_string is extracted from.

    Raises:
        Exception: If unable to find the type, we throw an Exception.

    Returns:
        Type: The type when found.
    """
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

    # Search imported modules in module
    # Inspired by this: https://stackoverflow.com/a/11781721/3717691
    # TODO: Perhaps we should limit the search depth here?
    q = deque([module])
    while q:
        m = q.popleft()
        try:
            t = eval(type_string, vars(m))
            return t
        except NameError:
            pass
        except TypeError:
            pass

        for name, item in inspect.getmembers(m):
            if inspect.ismodule(item):
                q.append(item)
            elif inspect.isclass(item) and item.__module__ != module.__name__:
                mod = inspect.getmodule(item)
                if mod:
                    q.append(mod)

    # TODO: We should make this configurable in config
    raise Exception(f"Was unable to detect the type of: {type_string} from module: {module.__file__}.\nPlease file this as a bug: https://github.com/jepperaskdk/pydoctest/issues")
