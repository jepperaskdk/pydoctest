
import os
from pydoctest.configuration import Configuration
from pydoctest.main import PyDoctestService


class TestIncludePaths():
    def test_include_paths_single_file_root(self) -> None:
        """
        Tests that specifying a file in the root directory is discovered.
        """
        config = Configuration.get_default_configuration()
        config.working_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "deep_project"))
        config.include_paths = ["root.py"]
        service = PyDoctestService(config)
        modules = service.discover_modules()

        assert len(modules) == 1
        assert modules[0].endswith("root.py")

    def test_include_paths_single_file_subdirectory(self) -> None:
        """
        Tests that specifying a file in a subdirectory is discovered.
        """
        config = Configuration.get_default_configuration()
        config.working_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "deep_project"))
        config.include_paths = ["b/c/d/file_d.py"]
        service = PyDoctestService(config)
        modules = service.discover_modules()

        assert len(modules) == 1
        assert modules[0].endswith("file_d.py")

    def test_include_paths_wildcard(self) -> None:
        """
        Tests that including on wildcard in a directory, only returns valid matches.
        """
        config = Configuration.get_default_configuration()
        config.working_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "deep_project"))
        config.include_paths = ["a/file_a_*.py"]
        service = PyDoctestService(config)
        modules = service.discover_modules()
        modules_sorted = sorted(modules)

        assert len(modules) == 2
        assert modules_sorted[0].endswith('file_a_1.py')
        assert modules_sorted[1].endswith('file_a_2.py')

    def test_include_paths_recursive_single_file(self) -> None:
        """
        Tests that including recursively for file, returns those files in multiple levels.
        """
        config = Configuration.get_default_configuration()
        config.working_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "deep_project"))
        config.include_paths = ["c/**/file_c.py"]
        service = PyDoctestService(config)
        modules = service.discover_modules()
        modules_sorted = sorted(modules)

        assert len(modules) == 3
        assert modules_sorted[0].endswith('c/file_c.py')
        assert modules_sorted[1].endswith('c/subdirectory/file_c.py')
        assert modules_sorted[2].endswith('c/subdirectory/subsubdirectory/file_c.py')

    def test_include_paths_recursive_wildcard(self) -> None:
        """
        Tests that including recursively with wildcard, returns those files.
        """
        config = Configuration.get_default_configuration()
        config.working_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "deep_project"))
        config.include_paths = ["**/file*.py"]
        service = PyDoctestService(config)
        modules = service.discover_modules()

        assert len(modules) == 9
