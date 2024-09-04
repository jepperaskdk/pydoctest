# Changelog

## [0.2.2] - 2024-08-28

- Fixed bug where self referenced union string did not parse. See https://github.com/jepperaskdk/pydoctest/issues/55.

## [0.2.1] - 2024-08-26

### Added

- Fixed bug where module and class name-clash would cause the wrong type to be compared.

## [0.2.0] - 2024-08-09

### Added

- [Breaking] Support for "optional" in all Google, Numpy and Sphinx parsers. This is breaking since it will start requiring optional parameters to be marked as optional in docstrings.

## [<=0.1.22]

- Versions below 0.2.0 were not tracked by this document. See [releases](https://github.com/jepperaskdk/pydoctest/releases) on GitHub.