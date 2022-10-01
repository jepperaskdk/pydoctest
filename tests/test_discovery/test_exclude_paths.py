
import os
from pydoctest.configuration import Configuration
from pydoctest.main import PyDoctestService


class TestExcludePaths():
    def test_exclude_paths_single_file(self) -> None:
        """
        Tests that excluding a single file is not returned when discovering.
        """
        config = Configuration.get_default_configuration()
        config.working_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "deep_project"))
        config.include_paths = ["**/*.py"]
        config.exclude_paths = ["b/c/d/file_d.py"]
        service = PyDoctestService(config)
        modules = service.discover_modules()

        assert len(modules) == 9
        assert all(not m.endswith('b/c/d/file_d.py') for m in modules)

    def test_exclude_paths_wildcard(self) -> None:
        """
        Tests that excluding using wildcard, doesn't return files matched.
        """
        config = Configuration.get_default_configuration()
        config.working_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "deep_project"))
        config.include_paths = ["a/**/*.py"]
        config.exclude_paths = ["file_a_*.py"]
        service = PyDoctestService(config)
        modules = service.discover_modules()

        assert len(modules) == 1
        assert modules[0].endswith('a/file_not_included.py')

    def test_exclude_paths_recursive_single_file(self) -> None:
        """
        Tests excluding files by filename, recursively.
        """
        config = Configuration.get_default_configuration()
        config.working_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "deep_project"))
        config.include_paths = ["c/**/*.py"]
        config.exclude_paths = ["**/file_c.py"]
        service = PyDoctestService(config)
        modules = service.discover_modules()

        assert len(modules) == 0

    def test_exclude_paths_recursive_wildcard(self) -> None:
        """
        Tests excluding files by wildcard, recursively.
        """
        config = Configuration.get_default_configuration()
        config.working_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "deep_project"))
        config.include_paths = ["**/*.py"]
        config.exclude_paths = ["**/file*.py"]
        service = PyDoctestService(config)
        modules = service.discover_modules()

        assert len(modules) == 1
        assert modules[0].endswith('root.py')
