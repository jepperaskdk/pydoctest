import pydoc

from pydoctest.parsers.google_parser import GoogleParser

import tests.test_class.correct_class


class TestGoogleParser():
    def test_empty_func(self) -> None:
        google_parser = GoogleParser()
        doc = pydoc.getdoc(tests.test_class.correct_class.CorrectTestClass.empty_func)
        arguments = google_parser.get_parameters(doc, tests.test_class.correct_class)
        assert len(arguments) == 0

        return_type = google_parser.get_return_type(doc, tests.test_class.correct_class)
        assert return_type == type(None)

    def test_func_returns_none(self) -> None:
        google_parser = GoogleParser()
        doc = pydoc.getdoc(tests.test_class.correct_class.CorrectTestClass.func_returns_none)
        arguments = google_parser.get_parameters(doc, tests.test_class.correct_class)
        assert len(arguments) == 1
        assert arguments[0].type == int

        return_type = google_parser.get_return_type(doc, tests.test_class.correct_class)
        assert return_type == type(None)

    def test_func_returns_int(self) -> None:
        google_parser = GoogleParser()
        doc = pydoc.getdoc(tests.test_class.correct_class.CorrectTestClass.func_returns_int)
        arguments = google_parser.get_parameters(doc, tests.test_class.correct_class)
        assert len(arguments) == 0

        return_type = google_parser.get_return_type(doc, tests.test_class.correct_class)
        assert return_type == int

    def test_func_has_arg_returns_arg(self) -> None:
        google_parser = GoogleParser()
        doc = pydoc.getdoc(tests.test_class.correct_class.CorrectTestClass.func_has_arg_returns_arg)
        arguments = google_parser.get_parameters(doc, tests.test_class.correct_class)
        assert len(arguments) == 1
        assert arguments[0].type == int

        return_type = google_parser.get_return_type(doc, tests.test_class.correct_class)
        assert return_type == float

    def test_func_has_raises_doc(self) -> None:
        google_parser = GoogleParser()
        doc = pydoc.getdoc(tests.test_class.correct_class.CorrectTestClass.func_has_raises_doc)
        arguments = google_parser.get_parameters(doc, tests.test_class.correct_class)
        assert len(arguments) == 1
        assert arguments[0].type == int

        return_type = google_parser.get_return_type(doc, tests.test_class.correct_class)
        assert return_type == int

    def test_func_with_multiline_summary(self) -> None:
        google_parser = GoogleParser()
        doc = pydoc.getdoc(tests.test_class.correct_class.CorrectTestClass.func_with_multiline_summary)
        arguments = google_parser.get_parameters(doc, tests.test_class.correct_class)
        assert len(arguments) == 1
        assert arguments[0].type == int

        return_type = google_parser.get_return_type(doc, tests.test_class.correct_class)
        assert return_type == int
