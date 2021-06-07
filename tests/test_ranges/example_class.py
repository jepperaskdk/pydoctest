class ExampleClass():

    # Range should be entire docstring (5..12)
    def func_no_summary(self, a: int) -> int:
        """

        Args:
            a (int): [description]

        Returns:
            int: [description]
        """
        pass

    # Range should be signature (16)
    def func_no_docstring(self, a: int) -> int:
        pass

    # Range should be entire docstring (22..32)
    # TODO: optimize later with specific line perhaps)
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

    # Range should be the line that contains the type (38..44)
    # TODO: Optimization, return only the line with return type
    def func_return_type_differ(self, a: int) -> int:
        """[summary]

        Args:
            a (int): [description]

        Returns:
            bool: [description]
        """
        pass

    # Range should be entire docstring (51..58)
    # TODO: Optimization: If too many args in docstring, highlight which one.
    def func_number_of_arguments_differ(self, a: int, b: int) -> int:
        """[summary]

        Args:
            a (int): [description]

        Returns:
            int: [description]
        """
        pass

    # Range should be the line with the name in (64..71)
    # TODO: Optimization, highlight only 'b' or 'b (int)' - depends on format?
    def func_argument_name_differ(self, a: int) -> int:
        """[summary]

        Args:
            b (int): [description]

        Returns:
            int: [description]
        """
        pass

    # Range should be line with argument in it (77..84)
    # TODO: Optimization, highlight only 'b (int)'
    def func_argument_type_differ(self, a: int) -> int:
        """[summary]

        Args:
            a (bool): [description]

        Returns:
            int: [description]
        """
        pass

    # Range should be entire docstring (89..99)
    def func_number_of_raised_exceptions_differ(self, a: int) -> int:
        """[summary]

        Args:
            a (int): [description]

        Raises:
            RuntimeError: [description]
            ValueError: [description]

        Returns:
            int: [description]
        """
        if 2 == 3:
            raise RuntimeError()

        if 2 == 4:
            raise ValueError()

        if 2 == 5:
            raise IndexError()

    # Range should be entire docstring (113..123)
    # TODO: Optimization, highlight specific conflicts.
    def func_listed_exceptions_not_match(self, a: int) -> int:
        """[summary]

        Args:
            a (int): [description]

        Raises:
            ValueError: [description]

        Returns:
            int: [description]
        """
        raise RuntimeError()
