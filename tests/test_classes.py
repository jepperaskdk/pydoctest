import unittest


class TestClass(unittest.TestCase):
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
