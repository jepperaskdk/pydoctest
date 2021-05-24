from pydoctest.configuration import Configuration
from pydoctest.validation import ResultType, validate_class, validate_function
from pydoctest.main import PyDoctestService


class TestPydoctest():
    """
    Uses the library to test its own docstrings - how awesome is that?
    """
    def test_pydoctest(self) -> None:
        config = Configuration.get_configuration_from_path("pydoctest.json")
        ds = PyDoctestService(config)
        result = ds.validate()
        counts = result.get_counts()
        assert counts.functions_failed == 0
        # TODO: This doesn't artificially bring up our code-coverage, right?
