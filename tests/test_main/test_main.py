from pydoctest.configuration import Configuration
from pydoctest.validation import ResultType, validate_class, validate_function
from pydoctest.main import PyDoctestService, get_configuration


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
        assert config.working_directory.endswith("tests/test_main")

        # Used by another test, but we use it to verify we found the right pydoctest.json
        assert config.include_paths == [ "notpythonmodule" ]

    def test_get_configuration_with_config_path(self) -> None:
        config = get_configuration("this is ignored", "tests/test_main/pydoctest.json")
        assert config.working_directory.endswith("tests/test_main")

        # Used by another test, but we use it to verify we found the right pydoctest.json
        assert config.include_paths == [ "notpythonmodule" ]

    def test_get_configuration_with_no_config(self) -> None:
        config = get_configuration("tests/test_main/no_config_here")
        assert config.working_directory.endswith("tests/test_main/no_config_here")

        # Default configs have empty include_paths
        assert config.include_paths == []
