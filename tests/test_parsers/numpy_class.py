# TODO: Convert google format below to numpy.

def failing_global_function(a: int) -> int:
    """[summary]
                            <-- missing args
    Returns:
        int: [description]
    """
    pass


class IncorrectTestClass():
    def empty_func(self) -> None:
        """Empty func

        Args:
            a (int): [description]          <-- should have no args
        """
        pass

    def func_returns_none(self, a: int) -> None:
        """Func returns None

        Args:
            a (int): [description]

        Returns:
            int: [description]              <-- should not be there
        """
        pass

    def func_returns_int(self) -> int:
        """Func returns int

        Returns:
            bool: [description]             <-- incorrect
        """
        pass

    def func_has_arg_returns_arg(self, a: int) -> float:
        """Func takes argument and returns argument
                        <-- should have args and returns
        """
        pass

    def func_has_raises_doc(self, a: int) -> int:
        """[summary]

        Raises:
            Exception: [description]           <-- Only have raises
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
            b (int): [description]          <-- incorrect

        Returns:
            int: [description]
        """
        pass

    def func_name_mismatch(self, a: int) -> int:
        """[summary]

        Args:
            b (int): [description]      <-- name is not 'a'

        Returns:
            int: [description]
        """
        pass

    def func_type_mismatch(self, a: int) -> int:
        """[summary]

        Args:
            a (float): [description]        <-- float is not int

        Returns:
            int: [description]
        """
        pass

    def func_parse_exception(self, a: int) -> int:
        """[summary]

        Args:
            THISDOESNTPARSE

        Raises:
            THISDOESNTPARSE

        Returns:
            THISDOESNTPARSE
        """
        pass


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


class RaisesClass():
    def func_with_raise(self) -> None:
        """
        Raises:
            RuntimeError: [description]
            ValueError: [description]
            IndexError: [description]
        """
        if 2 == 3:
            raise RuntimeError()

        if 2 == 4:
            raise ValueError()

        if 2 == 5:
            raise IndexError()

    def func_with_raise_and_args(self, a: int, b: float) -> None:
        """
        Raises:
            RuntimeError: [description]
            ValueError: [description]
            IndexError: [description]
        """
        if 2 == 3:
            raise RuntimeError()

        if 2 == 4:
            raise ValueError()

        if 2 == 5:
            raise IndexError()

    def func_with_raise_and_args_and_return(self, a: int, b: float) -> bool:
        """[summary]

        Args:
            a (int): [description]
            b (float): [description]

        Raises:
            RuntimeError: [description]
            ValueError: [description]
            IndexError: [description]

        Returns:
            bool: [description]
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

        Raises:
            RuntimeError: [description]
            IndexError: [description]
        """
        if 2 == 4:
            raise ValueError()

        if 2 == 5:
            raise IndexError()

    def func_with_raise_count_mismatch(self) -> None:
        """[summary]

        Raises:
            RuntimeError: [description]
            IndexError: [description]
        """
        if 2 == 3:
            raise RuntimeError()

        if 2 == 4:
            raise ValueError()

        if 2 == 5:
            raise IndexError()