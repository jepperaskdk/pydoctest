def global_func_raises() -> None:
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


class ExampleClass():

    def func_raises(self, a: int) -> None:
        """[summary]

        Args:
            a (DEFINITELYNOTACLASS): [description]
        """
        pass

    def func_locate(self, a: int) -> None:
        """[summary]

        Args:
            a (int): [description]
        """
        pass

    def func_with_raise(self, a: int) -> None:
        """

        Args:
            a (int): [description]

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
