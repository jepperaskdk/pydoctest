pydoctest: docstring signature verification

![example workflow](https://github.com/jepperaskdk/pydoctest/actions/workflows/python-package.yml/badge.svg)
[![codecov](https://codecov.io/gh/jepperaskdk/pydoctest/branch/main/graph/badge.svg?token=NSOW53NY9R)](https://codecov.io/gh/jepperaskdk/pydoctest)
[![PyPI version pydoctest](https://badge.fury.io/py/pydoctest.svg)](https://pypi.python.org/pypi/pydoctest/)


=======================================
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

Currently, only google is supported.

License
-------

Pydoctest is licensed under the terms of the MIT License (see the LICENSE file).
