class ClassNoDocString():
    def func_with_docstring(self, a: int) -> int:
        """[summary]

        Args:
            a (int): [description]

        Returns:
            int: [description]
        """
        pass

    def func_no_docstring(self, a: int) -> int:
        pass

    def func_no_summary(self, a: int) -> int:
        """

        Args:
            a (int): [description]

        Returns:
            int: [description]
        """
        pass
