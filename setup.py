import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

packages = setuptools.find_packages()
print(packages)
setuptools.setup(
    name="pydoctest",
    version="0.1.1",
    author="Jeppe Rask",
    author_email="jepperaskdk@gmail.com",
    description="Test if doctype types match signatures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jepperaskdk/pydoctest",
    project_urls={
        "Bug Tracker": "https://github.com/jepperaskdk/pydoctest/issues",
    },
    package_dir={"": "."},
    packages=packages,
    entry_points={
        'console_scripts': [
            'pydoctest=pydoctest.main:main'
        ]
    },
    python_requires=">=3.6",
)
