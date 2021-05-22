rm -rf dist
rm -rf build

# TODO: Extract these to a file that can be run once instead?
python3.6 -m pip install --upgrade build
python3.6 -m pip install --upgrade virtualenv
python3.6 -m pip install --user --upgrade twine

python3.6 -m build
python3.6 -m twine upload --repository testpypi dist/*
