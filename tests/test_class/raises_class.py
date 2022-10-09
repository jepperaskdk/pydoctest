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

    def func_with_raise_and_args(self) -> None:
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

    def func_with_raise_multiline_string(self) -> None:
        """
        [summary]
        """
        multiline_string = """
this has weird indentation
        """
        pass
