# Module with fixed number of failed, skipped and ok docstrings

def global_func_ok(a: int) -> int:
    """[summary]

    Args:
        a (int): [description]

    Returns:
        int: [description]
    """
    pass


class CountsClass():
    def func_failed(self, b: int) -> int:
        """[summary]

        Args:
            b (float): [description]        <-- should be int

        Returns:
            float: [description]            <-- should be int
        """
        pass

    def func_skipped(self) -> None:
        pass

    def func_ok(self, a: int) -> int:
        """[summary]

        Args:
            a (int): [description]

        Returns:
            int: [description]
        """
        pass
