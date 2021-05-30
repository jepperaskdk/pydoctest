import pydoc

from pydoctest.configuration import PARSERS
from pydoctest.parsers.google_parser import GoogleParser

import tests.test_class.correct_class
import tests.test_class.raises_class


class TestParsers():
    def test_empty_func(self) -> None:
        for name, parser in PARSERS.items():
            p = parser()
            doc = pydoc.getdoc(tests.test_class.correct_class.CorrectTestClass.empty_func)
            arguments = p.get_parameters(doc, tests.test_class.correct_class)
            assert len(arguments) == 0, f"Parser {name} failed assertion"

            return_type = p.get_return_type(doc, tests.test_class.correct_class)
            assert return_type == type(None), f"Parser {name} failed assertion"

    def test_func_returns_none(self) -> None:
        for name, parser in PARSERS.items():
            p = parser()
            doc = pydoc.getdoc(tests.test_class.correct_class.CorrectTestClass.func_returns_none)
            arguments = p.get_parameters(doc, tests.test_class.correct_class)
            assert len(arguments) == 1, f"Parser {name} failed assertion"
            assert arguments[0].type == int, f"Parser {name} failed assertion"

            return_type = p.get_return_type(doc, tests.test_class.correct_class)
            assert return_type == type(None), f"Parser {name} failed assertion"

    def test_func_returns_int(self) -> None:
        for name, parser in PARSERS.items():
            p = parser()
            doc = pydoc.getdoc(tests.test_class.correct_class.CorrectTestClass.func_returns_int)
            arguments = p.get_parameters(doc, tests.test_class.correct_class)
            assert len(arguments) == 0, f"Parser {name} failed assertion"

            return_type = p.get_return_type(doc, tests.test_class.correct_class)
            assert return_type == int, f"Parser {name} failed assertion"

    def test_func_has_arg_returns_arg(self) -> None:
        for name, parser in PARSERS.items():
            p = parser()
            doc = pydoc.getdoc(tests.test_class.correct_class.CorrectTestClass.func_has_arg_returns_arg)
            arguments = p.get_parameters(doc, tests.test_class.correct_class)
            assert len(arguments) == 1, f"Parser {name} failed assertion"
            assert arguments[0].type == int, f"Parser {name} failed assertion"

            return_type = p.get_return_type(doc, tests.test_class.correct_class)
            assert return_type == float, f"Parser {name} failed assertion"

    def test_func_has_raises_doc(self) -> None:
        for name, parser in PARSERS.items():
            p = parser()
            doc = pydoc.getdoc(tests.test_class.correct_class.CorrectTestClass.func_has_raises_doc)
            arguments = p.get_parameters(doc, tests.test_class.correct_class)
            assert len(arguments) == 1, f"Parser {name} failed assertion"
            assert arguments[0].type == int, f"Parser {name} failed assertion"

            return_type = p.get_return_type(doc, tests.test_class.correct_class)
            assert return_type == int, f"Parser {name} failed assertion"

    def test_func_with_multiline_summary(self) -> None:
        for name, parser in PARSERS.items():
            p = parser()
            doc = pydoc.getdoc(tests.test_class.correct_class.CorrectTestClass.func_with_multiline_summary)
            arguments = p.get_parameters(doc, tests.test_class.correct_class)
            assert len(arguments) == 1, f"Parser {name} failed assertion"
            assert arguments[0].type == int, f"Parser {name} failed assertion"

            return_type = p.get_return_type(doc, tests.test_class.correct_class)
            assert return_type == int, f"Parser {name} failed assertion"

    def test_get_summary_multiline_summary(self) -> None:
        for name, parser in PARSERS.items():
            p = parser()
            doc = pydoc.getdoc(tests.test_class.correct_class.CorrectTestClass.func_with_multiline_summary)

            summary = p.get_summary(doc, tests.test_class.correct_class)
            assert summary is not None
            assert len(summary) > 0, f"Parser {name} failed assertion"
            assert(len([x for x in summary if x == '\n']) > 1), f"Parser {name} failed assertion"

    def test_get_summary_empty_summary(self) -> None:
        for name, parser in PARSERS.items():
            p = parser()
            doc = pydoc.getdoc(tests.test_class.correct_class.CorrectTestClass.func_no_summary)
            arguments = p.get_parameters(doc, tests.test_class.correct_class)
            assert len(arguments) == 0, f"Parser {name} failed assertion"

            return_type = p.get_return_type(doc, tests.test_class.correct_class)
            assert return_type == type(None), f"Parser {name} failed assertion"

            summary = p.get_summary(doc, tests.test_class.correct_class)
            assert summary is None, f"Parser {name} failed assertion"

    def test_func_with_raise_and_args_and_return(self) -> None:
        for name, parser in PARSERS.items():
            p = parser()
            doc = pydoc.getdoc(tests.test_class.raises_class.RaisesClass.func_with_raise_and_args_and_return)
            actual_exceptions = p.get_exceptions_raised(doc)
            expected_exceptions = [ 'RuntimeError', 'ValueError', 'IndexError' ]
            assert len(expected_exceptions) == len(actual_exceptions)

            intersection = set(expected_exceptions) - set(actual_exceptions)
            assert len(intersection) == 0

    def test_func_with_raise_and_args(self) -> None:
        for name, parser in PARSERS.items():
            p = parser()
            doc = pydoc.getdoc(tests.test_class.raises_class.RaisesClass.func_with_raise_and_args)
            actual_exceptions = p.get_exceptions_raised(doc)
            expected_exceptions = [ 'RuntimeError', 'ValueError', 'IndexError' ]
            assert len(expected_exceptions) == len(actual_exceptions)

            intersection = set(expected_exceptions) - set(actual_exceptions)
            assert len(intersection) == 0

    def test_func_with_raise(self) -> None:
        for name, parser in PARSERS.items():
            p = parser()
            doc = pydoc.getdoc(tests.test_class.raises_class.RaisesClass.func_with_raise)
            actual_exceptions = p.get_exceptions_raised(doc)
            expected_exceptions = [ 'RuntimeError', 'ValueError', 'IndexError' ]
            assert len(expected_exceptions) == len(actual_exceptions)

            intersection = set(expected_exceptions) - set(actual_exceptions)
            assert len(intersection) == 0
