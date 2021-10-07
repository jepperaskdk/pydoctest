import pytest

from pydoctest.reporters.text_reporter import TextReporter
from pydoctest.reporters.json_reporter import JSONReporter
from pydoctest.configuration import Configuration
from pydoctest.validation import ResultType, validate_class, validate_function
from pydoctest.main import PyDoctestService, get_configuration, get_reporter


class TestMain():
    def test_not_python_module(self) -> None:
        config = Configuration.get_configuration_from_path("tests/test_main/pydoctest.json")

        ds = PyDoctestService(config)
        result = ds.validate()
        assert result.module_results[0].result == ResultType.NOT_RUN
        assert "Failed to load spec from file location" in result.module_results[0].fail_reason


class TestGetConfiguration():
    def test_get_configuration_with_root_dir(self) -> None:
        config = get_configuration("tests/test_main")
        assert config.working_directory.replace("\\", "/").endswith("tests/test_main")

        # Used by another test, but we use it to verify we found the right pydoctest.json
        assert config.include_paths == [ "notpythonmodule", "notproperpython.py" ]

    def test_get_configuration_with_config_path(self) -> None:
        config = get_configuration("this is ignored", "tests/test_main/pydoctest.json")
        assert config.working_directory.replace("\\", "/").endswith("tests/test_main")

        # Used by another test, but we use it to verify we found the right pydoctest.json
        assert config.include_paths == [ "notpythonmodule", "notproperpython.py" ]

    def test_get_configuration_with_no_config(self) -> None:
        config = get_configuration("tests/test_main/no_config_here")
        assert config.working_directory.replace("\\", "/").endswith("tests/test_main/no_config_here")

        # Default configs have empty include_paths
        assert config.include_paths == []


class TestGetReporter():
    def test_get_default_reporter(self) -> None:
        config = Configuration.get_default_configuration()
        reporter = get_reporter(config=config)
        assert isinstance(reporter, TextReporter)

    def test_get_reporter(self) -> None:
        config = Configuration.get_default_configuration()
        reporter = get_reporter(config=config, reporter="json")
        assert isinstance(reporter, JSONReporter)

    def test_get_non_existing_reporter(self) -> None:
        config = Configuration.get_default_configuration()
        with pytest.raises(Exception) as exn_info:
            reporter = get_reporter(config=config, reporter="doesnotexist")
        assert 'Unknown reporter' in str(exn_info.value)
