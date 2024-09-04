from typing import Union
from typing_extensions import Literal


class GoogleClass():
    def function_with_colon(self, a: int, b: int) -> None:
        """Summary

            Args:
                a (int): here's a string with a colon :
                b (int): A normal parameter
        """
        pass

    def function_with_literal(self, a: Literal['b', 'c']) -> None:
        """_summary_

        Args:
            a (Literal['b', 'c']): Literal parameter
        """
        pass

    def function_with_pipe(self, a: Union[int, float]) -> Union[int, float]:
        """_summary_

        Args:
            a (int | float): Union type parameter
        Returns:
            (int | float): Union type return value
        """

        return 0

    def func_optional_argument(self, a: int, b: int = 0) -> None:
        """Function with optional argument

        Args:
            a (int): [description]
            b (int, optional): [description]
        """
        pass

    def func_self_reference(self, a: "GoogleClass") -> "GoogleClass":
        """Function with self reference

        Args:
            a (GoogleClass): [description]
        
        Returns:
            GoogleClass: [description]
        """
        return GoogleClass()

    def func_self_union_reference(self, a: Union["GoogleClass", str]) -> Union["GoogleClass", str]:
        """Function with self reference

        Args:
            a (Union[GoogleClass, str]): [description]
        
        Returns:
            Union[GoogleClass, str]: [description]
        """
        return ""

