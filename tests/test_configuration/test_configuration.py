from pydoctest.configuration import Configuration


class TestConfiguration():
    def test_configuration_from_path(self) -> None:
        config = Configuration.get_configuration_from_path("tests/test_configuration/pydoctest.json")
        assert config.parser == "parsername"

        assert config.include_paths == [ "/path/to/module" ]
        assert config.exclude_paths == [ "/excludes/0", "excludes/1" ]

        assert config.fail_on_missing_docstring == True
