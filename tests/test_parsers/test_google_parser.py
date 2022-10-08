import pydoc
from typing_extensions import Literal
import pytest

from pydoctest.parsers.google_parser import GoogleParser
from pydoctest.exceptions import ParseException

import tests.test_class.incorrect_class
import tests.test_parsers.google_class


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

    def test_empty_func(self) -> None:
        parser = GoogleParser()
        doc = pydoc.getdoc(tests.test_class.correct_class.CorrectTestClass.empty_func)
        arguments = parser.get_parameters(doc, tests.test_class.correct_class)
        assert len(arguments) == 0, f"GoogleParser failed assertion"

        return_type = parser.get_return_type(doc, tests.test_class.correct_class)
        assert return_type == type(None), f"GoogleParser failed assertion"

    def test_func_returns_none(self) -> None:
        parser = GoogleParser()
        doc = pydoc.getdoc(tests.test_class.correct_class.CorrectTestClass.func_returns_none)
        arguments = parser.get_parameters(doc, tests.test_class.correct_class)
        assert len(arguments) == 1, f"GoogleParser failed assertion"
        assert arguments[0].type == int, f"GoogleParser failed assertion"

        return_type = parser.get_return_type(doc, tests.test_class.correct_class)
        assert return_type == type(None), f"GoogleParser failed assertion"

    def test_func_returns_int(self) -> None:
        parser = GoogleParser()
        doc = pydoc.getdoc(tests.test_class.correct_class.CorrectTestClass.func_returns_int)
        arguments = parser.get_parameters(doc, tests.test_class.correct_class)
        assert len(arguments) == 0, f"GoogleParser failed assertion"

        return_type = parser.get_return_type(doc, tests.test_class.correct_class)
        assert return_type == int, f"GoogleParser failed assertion"

    def test_func_has_arg_returns_arg(self) -> None:
        parser = GoogleParser()
        doc = pydoc.getdoc(tests.test_class.correct_class.CorrectTestClass.func_has_arg_returns_arg)
        arguments = parser.get_parameters(doc, tests.test_class.correct_class)
        assert len(arguments) == 1, f"GoogleParser failed assertion"
        assert arguments[0].type == int, f"GoogleParser failed assertion"

        return_type = parser.get_return_type(doc, tests.test_class.correct_class)
        assert return_type == float, f"GoogleParser failed assertion"

    def test_func_has_raises_doc(self) -> None:
        parser = GoogleParser()
        doc = pydoc.getdoc(tests.test_class.correct_class.CorrectTestClass.func_has_raises_doc)
        arguments = parser.get_parameters(doc, tests.test_class.correct_class)
        assert len(arguments) == 1, f"GoogleParser failed assertion"
        assert arguments[0].type == int, f"GoogleParser failed assertion"

        return_type = parser.get_return_type(doc, tests.test_class.correct_class)
        assert return_type == int, f"GoogleParser failed assertion"

    def test_func_with_multiline_summary(self) -> None:
        parser = GoogleParser()
        doc = pydoc.getdoc(tests.test_class.correct_class.CorrectTestClass.func_with_multiline_summary)
        arguments = parser.get_parameters(doc, tests.test_class.correct_class)
        assert len(arguments) == 1, f"GoogleParser failed assertion"
        assert arguments[0].type == int, f"GoogleParser failed assertion"

        return_type = parser.get_return_type(doc, tests.test_class.correct_class)
        assert return_type == int, f"GoogleParser failed assertion"

    def test_get_summary_multiline_summary(self) -> None:
        parser = GoogleParser()
        doc = pydoc.getdoc(tests.test_class.correct_class.CorrectTestClass.func_with_multiline_summary)

        summary = parser.get_summary(doc, tests.test_class.correct_class)
        assert summary is not None
        assert len(summary) > 0, f"GoogleParser failed assertion"
        assert(len([x for x in summary if x == '\n']) > 1), f"GoogleParser failed assertion"

    def test_get_summary_empty_summary(self) -> None:
        parser = GoogleParser()
        doc = pydoc.getdoc(tests.test_class.correct_class.CorrectTestClass.func_no_summary)
        arguments = parser.get_parameters(doc, tests.test_class.correct_class)
        assert len(arguments) == 0, f"GoogleParser failed assertion"

        return_type = parser.get_return_type(doc, tests.test_class.correct_class)
        assert return_type == type(None), f"GoogleParser failed assertion"

        summary = parser.get_summary(doc, tests.test_class.correct_class)
        assert summary is None, f"GoogleParser failed assertion"

    def test_func_with_raise_and_args_and_return(self) -> None:
        parser = GoogleParser()
        doc = pydoc.getdoc(tests.test_class.raises_class.RaisesClass.func_with_raise_and_args_and_return)
        actual_exceptions = parser.get_exceptions_raised(doc)
        expected_exceptions = [ 'RuntimeError', 'ValueError', 'IndexError' ]
        assert len(expected_exceptions) == len(actual_exceptions)

        intersection = set(expected_exceptions) - set(actual_exceptions)
        assert len(intersection) == 0

    def test_func_with_raise_and_args(self) -> None:
        parser = GoogleParser()
        doc = pydoc.getdoc(tests.test_class.raises_class.RaisesClass.func_with_raise_and_args)
        actual_exceptions = parser.get_exceptions_raised(doc)
        expected_exceptions = [ 'RuntimeError', 'ValueError', 'IndexError' ]
        assert len(expected_exceptions) == len(actual_exceptions)

        intersection = set(expected_exceptions) - set(actual_exceptions)
        assert len(intersection) == 0

    def test_func_with_raise(self) -> None:
        parser = GoogleParser()
        doc = pydoc.getdoc(tests.test_class.raises_class.RaisesClass.func_with_raise)
        actual_exceptions = parser.get_exceptions_raised(doc)
        expected_exceptions = [ 'RuntimeError', 'ValueError', 'IndexError' ]
        assert len(expected_exceptions) == len(actual_exceptions)

        intersection = set(expected_exceptions) - set(actual_exceptions)
        assert len(intersection) == 0

    def test_func_with_colon_in(self) -> None:
        """
        Solves: https://github.com/jepperaskdk/pydoctest/issues/29
        """
        parser = GoogleParser()
        doc = pydoc.getdoc(tests.test_parsers.google_class.GoogleClass.function_with_colon)
        params = parser.get_parameters(doc, tests.test_parsers.google_class)

        assert len(params) == 2
        assert params[0].name == "a"
        assert params[0].type == int
        assert params[1].name == "b"
        assert params[1].type == int

    def test_function_with_literal(self) -> None:
        """
        Solves: https://github.com/jepperaskdk/pydoctest/issues/41
        """
        parser = GoogleParser()
        doc = pydoc.getdoc(tests.test_parsers.google_class.GoogleClass.function_with_literal)
        params = parser.get_parameters(doc, tests.test_parsers.google_class)

        assert len(params) == 1
        assert params[0].name == 'a'
        assert params[0].type == Literal['b', 'c']
