import pydoc
from typing import Any, Dict
import pytest

from pydoctest.parsers.numpy_parser import NumpyParser
from pydoctest.exceptions import ParseException

import tests.test_parsers.numpy_class


class TestNumpyParser():

    def test_parse_exception_get_parameters(self) -> None:
        parser = NumpyParser()
        doc = pydoc.getdoc(tests.test_parsers.numpy_class.IncorrectTestClass.func_parse_exception)
        with pytest.raises(ParseException) as exc_info:
            parser.get_parameters(doc, tests.test_parsers.numpy_class)

    def test_parse_exception_get_return_type(self) -> None:
        parser = NumpyParser()
        doc = pydoc.getdoc(tests.test_parsers.numpy_class.IncorrectTestClass.func_parse_exception)
        with pytest.raises(ParseException) as exc_info:
            parser.get_return_type(doc, tests.test_parsers.numpy_class)

    def test_empty_func(self) -> None:
        parser = NumpyParser()
        doc = pydoc.getdoc(tests.test_parsers.numpy_class.CorrectTestClass.empty_func)
        arguments = parser.get_parameters(doc, tests.test_parsers.numpy_class)
        assert len(arguments) == 0, f"NumpyParser failed assertion"

        return_type = parser.get_return_type(doc, tests.test_parsers.numpy_class)
        assert return_type == type(None), f"NumpyParser failed assertion"

    def test_func_returns_none(self) -> None:
        parser = NumpyParser()
        doc = pydoc.getdoc(tests.test_parsers.numpy_class.CorrectTestClass.func_returns_none)
        arguments = parser.get_parameters(doc, tests.test_parsers.numpy_class)
        assert len(arguments) == 1, f"NumpyParser failed assertion"
        assert arguments[0].type == int, f"NumpyParser failed assertion"

        return_type = parser.get_return_type(doc, tests.test_parsers.numpy_class)
        assert return_type == type(None), f"NumpyParser failed assertion"

    def test_func_returns_int(self) -> None:
        parser = NumpyParser()
        doc = pydoc.getdoc(tests.test_parsers.numpy_class.CorrectTestClass.func_returns_int)
        arguments = parser.get_parameters(doc, tests.test_parsers.numpy_class)
        assert len(arguments) == 0, f"NumpyParser failed assertion"

        return_type = parser.get_return_type(doc, tests.test_parsers.numpy_class)
        assert return_type == int, f"NumpyParser failed assertion"

    def test_func_returns_int_name_type(self) -> None:
        parser = NumpyParser()
        doc = pydoc.getdoc(tests.test_parsers.numpy_class.CorrectTestClass.func_returns_int_name_type)
        arguments = parser.get_parameters(doc, tests.test_parsers.numpy_class)
        assert len(arguments) == 0, f"NumpyParser failed assertion"

        return_type = parser.get_return_type(doc, tests.test_parsers.numpy_class)
        assert return_type == int, f"NumpyParser failed assertion"

    def test_func_has_arg_returns_arg(self) -> None:
        parser = NumpyParser()
        doc = pydoc.getdoc(tests.test_parsers.numpy_class.CorrectTestClass.func_has_arg_returns_arg)
        arguments = parser.get_parameters(doc, tests.test_parsers.numpy_class)
        assert len(arguments) == 1, f"NumpyParser failed assertion"
        assert arguments[0].type == int, f"NumpyParser failed assertion"

        return_type = parser.get_return_type(doc, tests.test_parsers.numpy_class)
        assert return_type == float, f"NumpyParser failed assertion"

    def test_func_has_raises_doc(self) -> None:
        parser = NumpyParser()
        doc = pydoc.getdoc(tests.test_parsers.numpy_class.CorrectTestClass.func_has_raises_doc)
        arguments = parser.get_parameters(doc, tests.test_parsers.numpy_class)
        assert len(arguments) == 1, f"NumpyParser failed assertion"
        assert arguments[0].type == int, f"NumpyParser failed assertion"

        return_type = parser.get_return_type(doc, tests.test_parsers.numpy_class)
        assert return_type == int, f"NumpyParser failed assertion"

    def test_func_with_multiline_summary(self) -> None:
        parser = NumpyParser()
        doc = pydoc.getdoc(tests.test_parsers.numpy_class.CorrectTestClass.func_with_multiline_summary)
        arguments = parser.get_parameters(doc, tests.test_parsers.numpy_class)
        assert len(arguments) == 1, f"NumpyParser failed assertion"
        assert arguments[0].type == int, f"NumpyParser failed assertion"

        return_type = parser.get_return_type(doc, tests.test_parsers.numpy_class)
        assert return_type == int, f"NumpyParser failed assertion"

    def test_get_summary_multiline_summary(self) -> None:
        parser = NumpyParser()
        doc = pydoc.getdoc(tests.test_parsers.numpy_class.CorrectTestClass.func_with_multiline_summary)

        summary = parser.get_summary(doc, tests.test_parsers.numpy_class)
        assert summary is not None
        assert len(summary) > 0, f"NumpyParser failed assertion"
        assert(len([x for x in summary if x == '\n']) > 1), f"NumpyParser failed assertion"

    def test_get_summary_empty_summary(self) -> None:
        parser = NumpyParser()
        doc = pydoc.getdoc(tests.test_parsers.numpy_class.CorrectTestClass.func_no_summary)
        arguments = parser.get_parameters(doc, tests.test_parsers.numpy_class)
        assert len(arguments) == 0, f"NumpyParser failed assertion"

        return_type = parser.get_return_type(doc, tests.test_parsers.numpy_class)
        assert return_type == type(None), f"NumpyParser failed assertion"

        summary = parser.get_summary(doc, tests.test_parsers.numpy_class)
        assert summary is None, f"NumpyParser failed assertion"

    def test_func_with_raise_and_args_and_return(self) -> None:
        parser = NumpyParser()
        doc = pydoc.getdoc(tests.test_parsers.numpy_class.RaisesClass.func_with_raise_and_args_and_return)
        actual_exceptions = parser.get_exceptions_raised(doc)
        expected_exceptions = [ 'RuntimeError', 'ValueError', 'IndexError' ]
        assert len(expected_exceptions) == len(actual_exceptions)

        intersection = set(expected_exceptions) - set(actual_exceptions)
        assert len(intersection) == 0

    def test_func_with_raise_and_args(self) -> None:
        parser = NumpyParser()
        doc = pydoc.getdoc(tests.test_parsers.numpy_class.RaisesClass.func_with_raise_and_args)
        actual_exceptions = parser.get_exceptions_raised(doc)
        expected_exceptions = [ 'RuntimeError', 'ValueError', 'IndexError' ]
        assert len(expected_exceptions) == len(actual_exceptions)

        intersection = set(expected_exceptions) - set(actual_exceptions)
        assert len(intersection) == 0

        parameters = parser.get_parameters(doc, tests.test_parsers.numpy_class)
        assert len(parameters) == 2
        assert parameters[0].name == 'a'
        assert parameters[0].type == int

        assert parameters[1].name == 'b'
        assert parameters[1].type == float

    def test_func_with_raise(self) -> None:
        parser = NumpyParser()
        doc = pydoc.getdoc(tests.test_parsers.numpy_class.RaisesClass.func_with_raise)
        actual_exceptions = parser.get_exceptions_raised(doc)
        expected_exceptions = [ 'RuntimeError', 'ValueError', 'IndexError' ]
        assert len(expected_exceptions) == len(actual_exceptions)

        intersection = set(expected_exceptions) - set(actual_exceptions)
        assert len(intersection) == 0

    def test_func_with_generics(self) -> None:
        parser = NumpyParser()
        doc = pydoc.getdoc(tests.test_parsers.numpy_class.CorrectTestClass.func_with_generics)
        parameters = parser.get_parameters(doc, tests.test_parsers.numpy_class)
        assert len(parameters) == 1
        assert parameters[0].type == Dict[str, Any]
        assert parameters[0].name == 'a_a'

        return_type = parser.get_return_type(doc, tests.test_parsers.numpy_class)
        assert return_type == Dict[str, Any]
