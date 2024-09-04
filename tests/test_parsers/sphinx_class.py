from typing import Any, Dict, Union


def failing_global_function(a: int) -> int:
    """[summary]
                            <-- missing args
    :return: [description]
    :rtype: int
    """
    return 0


class IncorrectTestClass():
    def empty_func(self) -> None:
        """Empty func

        :param a: [description]             <-- should have no args
        :type a: int
        """
        pass

    def func_returns_none(self, a: int) -> None:
        """Func returns None

        :param a: [description]
        :type a: int

        :return: [description]              <-- should not be there
        :rtype: int
        """
        pass

    def func_returns_int(self) -> int:
        """Func returns int

        :return: [description]
        :rtype: bool                        <-- incorrect
        """
        return 0

    def func_has_arg_returns_arg(self, a: int) -> float:
        """Func takes argument and returns argument

                                            <-- should have args and returns
        """
        return 0.0

    def func_has_raises_doc(self, a: int) -> int:
        """[summary]

        :raises Exception: [description]            <-- Only have raises
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

        :param a: [description]
        :type a: int
        :param b: [description]             <-- incorrect
        :type b: int
        :return: [description]
        :rtype: int
        """
        return 0

    def func_name_mismatch(self, a: int) -> int:
        """[summary]

        :param b: [description]         <-- name is not 'a'
        :type b: int
        :return: [description]
        :rtype: int
        """
        return 0

    def func_type_mismatch(self, a: int) -> int:
        """[summary]

        :param a: [description]
        :type a: float                      <-- float is not int
        :return: [description]
        :rtype: int
        """
        return 0

    def func_parse_exception(self, a: int) -> int:
        """[summary]

        :param a: [description]
        :type THISDOESNTPARSE
        :raises THISDOESNTPARSE
        :return: [description]
        :THISDOESNTPARSE
        """
        return 0


class CorrectTestClass():
    def func_with_generics(self, a_a: Dict[str, Any]) -> Dict[str, Any]:
        """[summary]

        :param a_a: [description]
        :type a_a: Dict[str, Any]
        :return: [description]
        :rtype: Dict[str, Any]
        """
        return {}

    def empty_func(self) -> None:
        """Empty func
        """
        pass

    def func_returns_none(self, a: int) -> None:
        """Func returns None

        :param a: [description]
        :type a: int
        """
        pass

    def func_returns_int(self) -> int:
        """Func returns int

        :return: [description]
        :rtype: int
        """
        return 0

    def func_returns_union(self) -> Union[int, str]:
        """Func returns int or str

        :return: [description]
        :rtype: int | str
        """
        return 0

    def func_has_arg_returns_arg(self, a: int) -> float:
        """Func takes argument and returns argument

        :param a: [description]
        :type a: int
        :return: [description]
        :rtype: float
        """
        return 0.0

    def func_has_union_arg(self, a: Union[int, str]) -> None:
        """Func takes int or str

        :param a: [description]
        :type a: int | str
        """
        pass

    def func_has_raises_doc(self, a: int) -> int:
        """[summary]

        :param a: [description]
        :type a: int
        :raises Exception: [description]
        :return: [description]
        :rtype: int
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

        :param a: [description]
        :type a: int
        :return: [description]
        :rtype: int
        """
        return 0

    def func_no_summary(self) -> None:
        """

        """
        pass

    def func_optional_argument(self, a: int, b: int = 0) -> None:
        """Function with optional argument

        :param a: [description]
        :type a: int
        :param b: [description]
        :type b: int, optional
        """
        pass

    def func_self_reference(self, a: "CorrectTestClass") -> "CorrectTestClass":
        """Function with self reference

        :param a: [description]
        :type a: CorrectTestClass
        :return: [description]
        :rtype: CorrectTestClass
        """
        return CorrectTestClass()

    def func_self_union_reference(self, a: Union["CorrectTestClass", str]) -> Union["CorrectTestClass", str]:
        """Function with self reference

        :param a: [description]
        :type a: Union[CorrectTestClass, str]
        :return: [description]
        :rtype: Union[CorrectTestClass, str]
        """
        return ""


class RaisesClass():

    def func_with_raise(self) -> None:
        """[summary]

        :raises RuntimeError: [description]
        :raises ValueError: [description]
        :raises IndexError: [description]
        """
        if 2 == 3:
            raise RuntimeError()

        if 2 == 4:
            raise ValueError()

        if 2 == 5:
            raise IndexError()

    def func_with_raise_and_args(self, a: int, b: float) -> None:
        """[summary]

        :param a: [description]
        :type a: int
        :param b: [description]
        :type b: float
        :raises RuntimeError: [description]
        :raises ValueError: [description]
        :raises IndexError: [description]
        """
        if 2 == 3:
            raise RuntimeError()

        if 2 == 4:
            raise ValueError()

        if 2 == 5:
            raise IndexError()

    def func_with_raise_and_args_and_return(self, a: int, b: float) -> bool:
        """[summary]

        :param a: [description]
        :type a: int
        :param b: [description]
        :type b: float
        :raises RuntimeError: [description]
        :raises ValueError: [description]
        :raises IndexError: [description]
        :return: [description]
        :rtype: bool
        """
        if 2 == 3:
            raise RuntimeError()

        if 2 == 4:
            raise ValueError()

        if 2 == 5:
            raise IndexError()

        return True

    def func_with_missing_raise(self) -> None:
        """
        """
        if 2 == 5:
            raise IndexError()

    def func_with_incorrect_raise(self) -> None:
        """[summary]

        :raises RuntimeError: [description]
        :raises IndexError: [description]
        """
        if 2 == 4:
            raise ValueError()

        if 2 == 5:
            raise IndexError()

    def func_with_raise_count_mismatch(self) -> None:
        """[summary]

        :raises RuntimeError: [description]
        :raises IndexError: [description]
        """
        if 2 == 3:
            raise RuntimeError()

        if 2 == 4:
            raise ValueError()

        if 2 == 5:
            raise IndexError()
