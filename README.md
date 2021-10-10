pydoctest: docstring signature verification
=======================================
![example workflow](https://github.com/jepperaskdk/pydoctest/actions/workflows/python-package.yml/badge.svg)
[![codecov](https://codecov.io/gh/jepperaskdk/pydoctest/branch/main/graph/badge.svg?token=NSOW53NY9R)](https://codecov.io/gh/jepperaskdk/pydoctest)
[![PyPI version pydoctest](https://badge.fury.io/py/pydoctest.svg)](https://pypi.python.org/pypi/pydoctest/)


File issues here: [Issues tracker](https://github.com/jepperaskdk/pydoctest/issues)

Motivation
------------

Pydoctest helps you verify that your docstrings match your function signatures.
As a codebase evolves, you can some times forget to update the docstrings.


Installation
-----------

Install pydoctest with pip:

    $ python3 -m pip install pydoctest

Usage
-----------
Navigate to your project location, and execute pydoctest

    $ pydoctest

With no pydoctest.json configuration file, it will by default validate all \*.py files in the current directory. See the configuration section for options.
If you get errors with modules not being found, try placing the pydoctest.json differently or executing inside the package.

Output
----------
Pydoctest supports outputting results either as `JSON` or `Text` with different verbosity options. By default, `Text` is returned. To specify the output, invoke with `--reporter` argument:

    $ pydoctest --reporter [json | text]

For Text-output, `--verbosity` can be provided with a value of 0 (quiet), 1 (show failed) or 2 (show all).

    $ pydoctest --reporter text --verbosity 1
Configuration
-----------
Pydoctest can be configured with a config JSON file. By default, it will search for `pydoctest.json` in the directory pydoctest is executed. A path can also be provided when executing:

    $ pydoctest --config /path/to/pydoctest.json

Example pydoctest.json:

```json
{
    "include_paths": [ "server/*.py" ],
    "fail_on_missing_docstring": true,
    "parser": "google",
}
```

Docstring format can be specified with the `--parser` argument:

    $ pydoctest --parser google

Currently, only google, numpy and sphinx are supported.

Full list of arguments:
- "include_paths": [ List of strings ]  # Pattern to search modules with.
- "verbosity": [ 0 | 1 | 2 ]  # How much to print, 0 = quiet, 1 = show failed, 2 = show all
- "parser": [ "google" (default) | "sphinx" | "numpy" ]  # Docstring format to use. Please raise an issue if you need other formats implemented.
- "fail_on_missing_docstring": [ true | false (default) ]  # Mark a function as failed, if it does not have a docstring
- "fail_on_missing_summary": [ true | false (default) ]  # Mark a function as failed, if it does have a docstring, but no summary.
- "fail_on_raises_section": [ true (default) | false ]  # Mark a function as failed, if docstring doesn't mention raised exceptions correctly.

License
-------

Pydoctest is licensed under the terms of the MIT License (see the LICENSE file).
