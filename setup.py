import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# packages = setuptools.find_packages(where="src")
packages = [ '.' ]
print(packages)

setuptools.setup(
    name="flowdoctest",
    version="0.0.1",
    author="Jeppe Rask",
    author_email="jepperaskdk@gmail.com",
    description="Test if doctype types match signatures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jepperaskdk/doctest",
    project_urls={
        "Bug Tracker": "https://github.com/jepperaskdk/doctest/issues",
    },
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            'flowdoctest=flowdoctest:main'
        ]
    },
    # packages=packages,
    python_requires=">=3.6",
)
