from pydoctest.configuration import Configuration
from pydoctest.validation import validate_class

import tests.test_class.example_class


class TestDocs():
    def test_empty_func(self) -> None:
        config = Configuration()
        result = validate_class(tests.test_class.example_class.TestClass, config, tests.test_class.example_class)
        assert len(result.function_results) == 0

    def test_func_returns_none(self) -> None:
        pass

    def test_func_returns_int(self) -> None:
        pass
