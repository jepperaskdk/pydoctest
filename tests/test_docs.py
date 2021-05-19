import unittest


class TestClass():
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


class TestDocs(unittest.TestCase):
    def test_empty_func(self) -> None:
        pass

    def test_func_returns_none(self) -> None:
        pass

    def test_func_returns_int(self) -> None:
        pass
