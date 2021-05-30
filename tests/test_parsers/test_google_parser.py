import pydoc
import pytest

from pydoctest.configuration import PARSERS
from pydoctest.parsers.google_parser import GoogleParser
from pydoctest.exceptions import ParseException

import tests.test_class.incorrect_class


class TestGoogleParser():
    def test_parse_exception_get_parameters(self) -> None:
        parser = GoogleParser()
        doc = pydoc.getdoc(tests.test_class.incorrect_class.IncorrectTestClass.func_parse_exception)
        with pytest.raises(ParseException) as exc_info:
            parser.get_parameters(doc, tests.test_class.incorrect_class)

    def test_parse_exception_get_return_type(self) -> None:
        parser = GoogleParser()
        doc = pydoc.getdoc(tests.test_class.incorrect_class.IncorrectTestClass.func_parse_exception)
        with pytest.raises(ParseException) as exc_info:
            parser.get_return_type(doc, tests.test_class.incorrect_class)

    def test_get_exceptions_raised(self) -> None:
        parser = GoogleParser()
        doc = pydoc.getdoc(tests.test_class.incorrect_class.IncorrectTestClass.func_parse_exception)
        with pytest.raises(ParseException) as exc_info:
            parser.get_exceptions_raised(doc)
