import pydoc
from typing import Dict, Any
import pytest

from pydoctest.parsers.sphinx_parser import SphinxParser
from pydoctest.exceptions import ParseException

import tests.test_parsers.sphinx_class


class TestSphinxParser():

    def test_parse_exception_get_parameters(self) -> None:
        parser = SphinxParser()
        doc = pydoc.getdoc(tests.test_parsers.sphinx_class.IncorrectTestClass.func_parse_exception)
        with pytest.raises(ParseException) as exc_info:
            parser.get_parameters(doc, tests.test_parsers.sphinx_class)

    def test_empty_func(self) -> None:
        parser = SphinxParser()
        doc = pydoc.getdoc(tests.test_parsers.sphinx_class.CorrectTestClass.empty_func)
        arguments = parser.get_parameters(doc, tests.test_parsers.sphinx_class)
        assert len(arguments) == 0, f"SphinxParser failed assertion"

        return_type = parser.get_return_type(doc, tests.test_parsers.sphinx_class)
        assert return_type == type(None), f"SphinxParser failed assertion"

    def test_func_returns_none(self) -> None:
        parser = SphinxParser()
        doc = pydoc.getdoc(tests.test_parsers.sphinx_class.CorrectTestClass.func_returns_none)
        arguments = parser.get_parameters(doc, tests.test_parsers.sphinx_class)
        assert len(arguments) == 1, f"SphinxParser failed assertion"
        assert arguments[0].type == int, f"SphinxParser failed assertion"

        return_type = parser.get_return_type(doc, tests.test_parsers.sphinx_class)
        assert return_type == type(None), f"SphinxParser failed assertion"

    def test_func_returns_int(self) -> None:
        parser = SphinxParser()
        doc = pydoc.getdoc(tests.test_parsers.sphinx_class.CorrectTestClass.func_returns_int)
        arguments = parser.get_parameters(doc, tests.test_parsers.sphinx_class)
        assert len(arguments) == 0, f"SphinxParser failed assertion"

        return_type = parser.get_return_type(doc, tests.test_parsers.sphinx_class)
        assert return_type == int, f"SphinxParser failed assertion"

    def test_func_has_arg_returns_arg(self) -> None:
        parser = SphinxParser()
        doc = pydoc.getdoc(tests.test_parsers.sphinx_class.CorrectTestClass.func_has_arg_returns_arg)
        arguments = parser.get_parameters(doc, tests.test_parsers.sphinx_class)
        assert len(arguments) == 1, f"SphinxParser failed assertion"
        assert arguments[0].type == int, f"SphinxParser failed assertion"

        return_type = parser.get_return_type(doc, tests.test_parsers.sphinx_class)
        assert return_type == float, f"SphinxParser failed assertion"

    def test_func_has_raises_doc(self) -> None:
        parser = SphinxParser()
        doc = pydoc.getdoc(tests.test_parsers.sphinx_class.CorrectTestClass.func_has_raises_doc)
        arguments = parser.get_parameters(doc, tests.test_parsers.sphinx_class)
        assert len(arguments) == 1, f"SphinxParser failed assertion"
        assert arguments[0].type == int, f"SphinxParser failed assertion"

        return_type = parser.get_return_type(doc, tests.test_parsers.sphinx_class)
        assert return_type == int, f"SphinxParser failed assertion"

    def test_func_with_multiline_summary(self) -> None:
        parser = SphinxParser()
        doc = pydoc.getdoc(tests.test_parsers.sphinx_class.CorrectTestClass.func_with_multiline_summary)
        arguments = parser.get_parameters(doc, tests.test_parsers.sphinx_class)
        assert len(arguments) == 1, f"SphinxParser failed assertion"
        assert arguments[0].type == int, f"SphinxParser failed assertion"

        return_type = parser.get_return_type(doc, tests.test_parsers.sphinx_class)
        assert return_type == int, f"SphinxParser failed assertion"

    def test_get_summary_multiline_summary(self) -> None:
        parser = SphinxParser()
        doc = pydoc.getdoc(tests.test_parsers.sphinx_class.CorrectTestClass.func_with_multiline_summary)

        summary = parser.get_summary(doc, tests.test_parsers.sphinx_class)
        assert summary is not None
        assert summary == """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Mauris tellus diam, iaculis et nisl sit amet, tristique sodales massa.
Proin lacinia faucibus ex a scelerisque. Fusce mauris orci, finibus a cursus vitae, luctus sit amet erat.
Ut dignissim elit nec nisi faucibus lobortis.
Proin varius mi lectus, at gravida nisl dapibus et. Nunc ac sagittis sapien.
Praesent tincidunt ac tellus ut mollis. Integer tincidunt pretium diam, quis aliquet turpis volutpat quis.
Nulla at est facilisis, scelerisque ipsum in, interdum dolor. Vivamus fermentum placerat mattis.
Ut nec augue nec ex sodales ornare vel sit amet urna. Nunc scelerisque risus nisi, quis pharetra nibh fermentum auctor.
Donec ultrices lectus eu mauris lacinia, nec tincidunt tortor facilisis.
Sed condimentum elit non metus sagittis tempor. Cras mollis lacus lacus, vitae placerat quam laoreet id.""", f"SphinxParser failed assertion"

    def test_get_summary_empty_summary(self) -> None:
        parser = SphinxParser()
        doc = pydoc.getdoc(tests.test_parsers.sphinx_class.CorrectTestClass.func_no_summary)
        arguments = parser.get_parameters(doc, tests.test_parsers.sphinx_class)
        assert len(arguments) == 0, f"SphinxParser failed assertion"

        return_type = parser.get_return_type(doc, tests.test_parsers.sphinx_class)
        assert return_type == type(None), f"SphinxParser failed assertion"

        summary = parser.get_summary(doc, tests.test_parsers.sphinx_class)
        assert summary is None, f"SphinxParser failed assertion"

    def test_func_with_raise_and_args_and_return(self) -> None:
        parser = SphinxParser()
        doc = pydoc.getdoc(tests.test_parsers.sphinx_class.RaisesClass.func_with_raise_and_args_and_return)
        actual_exceptions = parser.get_exceptions_raised(doc)
        expected_exceptions = [ 'RuntimeError', 'ValueError', 'IndexError' ]
        assert len(expected_exceptions) == len(actual_exceptions)

        intersection = set(expected_exceptions) - set(actual_exceptions)
        assert len(intersection) == 0

    def test_func_with_raise_and_args(self) -> None:
        parser = SphinxParser()
        doc = pydoc.getdoc(tests.test_parsers.sphinx_class.RaisesClass.func_with_raise_and_args)
        actual_exceptions = parser.get_exceptions_raised(doc)
        expected_exceptions = [ 'RuntimeError', 'ValueError', 'IndexError' ]
        assert len(expected_exceptions) == len(actual_exceptions)

        intersection = set(expected_exceptions) - set(actual_exceptions)
        assert len(intersection) == 0

        parameters = parser.get_parameters(doc, tests.test_parsers.sphinx_class)
        assert len(parameters) == 2
        assert parameters[0].name == 'a'
        assert parameters[0].type == int

        assert parameters[1].name == 'b'
        assert parameters[1].type == float

    def test_func_with_raise(self) -> None:
        parser = SphinxParser()
        doc = pydoc.getdoc(tests.test_parsers.sphinx_class.RaisesClass.func_with_raise)
        actual_exceptions = parser.get_exceptions_raised(doc)
        expected_exceptions = [ 'RuntimeError', 'ValueError', 'IndexError' ]
        assert len(expected_exceptions) == len(actual_exceptions)

        intersection = set(expected_exceptions) - set(actual_exceptions)
        assert len(intersection) == 0

    def test_func_with_generics(self) -> None:
        parser = SphinxParser()
        doc = pydoc.getdoc(tests.test_parsers.sphinx_class.CorrectTestClass.func_with_generics)
        parameters = parser.get_parameters(doc, tests.test_parsers.sphinx_class)
        assert len(parameters) == 1
        assert parameters[0].type == Dict[str, Any]
        assert parameters[0].name == 'a_a'

        return_type = parser.get_return_type(doc, tests.test_parsers.sphinx_class)
        assert return_type == Dict[str, Any]
