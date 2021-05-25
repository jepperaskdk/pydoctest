from typing import List, Type
from types import ModuleType


class Parameter():
    def __init__(self, name: str, t: Type) -> None:
        """Instantiates a function parameter.

        Args:
            name (str): The name of the argument.
            t (Type): The type of the argument
        """
        self.name = name
        self.type = t


class Parser():
    def get_parameters(self, doc: str, module_type: ModuleType) -> List[Parameter]:
        """Finds the function arguments as strings, and returns their types as Parameter instances.

        Args:
            doc (str): Function docstring.
            module_type (ModuleType): The module the docstring was extracted from.

        Raises:
            NotImplementedError: Raised if this is not implemented by subclasses.

        Returns:
            List[Parameter]: The parameters parsed from the docstring.
        """
        raise NotImplementedError()

    def get_return_type(self, doc: str, module_type: ModuleType) -> Type:
        """Base method for Parsers to return the return-type of a function from its docstring.

        Args:
            doc (str): Function docstring.
            module_type (ModuleType): The module the docstring was extracted from.

        Raises:
            NotImplementedError: Raised if this is not implemented by subclasses.

        Returns:
            Type: The return type parsed from the docs.
        """
        raise NotImplementedError()
