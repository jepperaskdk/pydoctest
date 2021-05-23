import pytest
from pydoctest.configuration import Configuration


class TestConfiguration():
    def test_configuration_from_path(self) -> None:
        config = Configuration.get_configuration_from_path("tests/test_configuration/pydoctest.json")
        assert config.parser == "parsername"

        assert config.include_paths == [ "/path/to/module" ]
        assert config.exclude_paths == [ "/excludes/0", "excludes/1" ]

        assert config.fail_on_missing_docstring == True

    def test_configuration_unknown_parser(self) -> None:
        config = Configuration.get_configuration_from_path("tests/test_configuration/pydoctest.json")
        config.parser = "kldfgjndfgnjg"

        with pytest.raises(Exception):
            config.get_parser()

    def test_configuration_unknown_keys(self) -> None:
        with pytest.raises(Exception):
            config = Configuration.get_configuration_from_path("tests/test_configuration/pydoctest_unknown_keys.json")
