import sys
from typing import Union


class CorrectTestClass():
    def empty_func(self) -> None:
        """Empty func
        """
        pass

    def func_returns_none(self, a: int) -> None:
        """Func returns None

        Args:
            a (int): [description]
        """
        pass

    def func_returns_int(self) -> int:
        """Func returns int

        Returns:
            int: [description]
        """
        pass

    def func_has_arg_returns_arg(self, a: int) -> float:
        """Func takes argument and returns argument

        Args:
            a (int): [description]

        Returns:
            float: [description]
        """
        pass

    def func_has_raises_doc(self, a: int) -> int:
        """[summary]

        Args:
            a (int): [description]

        Raises:
            Exception: [description]

        Returns:
            int: [description]
        """
        raise Exception()

    def func_with_multiline_summary(self, a: int) -> int:
        """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Mauris tellus diam, iaculis et nisl sit amet, tristique sodales massa.
        Proin lacinia faucibus ex a scelerisque. Fusce mauris orci, finibus a cursus vitae, luctus sit amet erat.
        Ut dignissim elit nec nisi faucibus lobortis.
        Proin varius mi lectus, at gravida nisl dapibus et. Nunc ac sagittis sapien.
        Praesent tincidunt ac tellus ut mollis. Integer tincidunt pretium diam, quis aliquet turpis volutpat quis.
        Nulla at est facilisis, scelerisque ipsum in, interdum dolor. Vivamus fermentum placerat mattis.
        Ut nec augue nec ex sodales ornare vel sit amet urna. Nunc scelerisque risus nisi, quis pharetra nibh fermentum auctor.
        Donec ultrices lectus eu mauris lacinia, nec tincidunt tortor facilisis.
        Sed condimentum elit non metus sagittis tempor. Cras mollis lacus lacus, vitae placerat quam laoreet id.

        Args:
            a (int): [description]

        Returns:
            int: [description]
        """
        pass

    def func_no_summary(self) -> None:
        """
        """
        pass

    if sys.version_info[:2] >= (3,10):
        def func_returns_union(self) -> Union[int, str]:
            """Func returns int | str

            Returns:
                int | str: [description]
            """
            pass

        def func_has_union_arg(self, a: Union[int, str]) -> None:
            """Func takes union argument

            Args:
                a (int | str): [description]
            """
            pass

    def func_with_optional(self, a: int = 0) -> int:
        """[summary]

        Args:
            a (int, optional): [description]

        Returns:
            int: [description]
        """
        pass

    def method_with_self_class_union(x: "CorrectTestClass | str") -> "CorrectTestClass":
        """[summary]

        Args:
            x (CorrectTestClass | str): [description]

        Returns:
            CorrectTestClass: [description]
        """
        pass

