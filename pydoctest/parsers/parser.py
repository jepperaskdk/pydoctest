from enum import IntEnum
from typing import List, Optional, Type
from types import ModuleType


class Section(IntEnum):
    SUMMARY = 0,
    ARGUMENTS = 1,
    RAISES = 2,
    RETURNS = 3


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
    def get_exceptions_raised(self, doc: str) -> List[str]:
        """Returns the exceptions listed as raised in the docstring.

        Args:
            doc (str): The docstring to analyze.

        Raises:
            NotImplementedError: Raised if this is not implemented by subclasses.

        Returns:
            List[str]: List of exceptions raised.
        """
        raise NotImplementedError()

    def get_summary(self, doc: str, module_type: ModuleType) -> Optional[str]:
        """Returns the summary part of the docstring.

        Args:
            doc (str): The docstring to analyze.
            module_type (ModuleType): The module it was extracted from.

        Raises:
            NotImplementedError: Raised if this is not implemented by subclasses.

        Returns:
            Optional[str]: The summary, if it exists.
        """
        raise NotImplementedError()

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
