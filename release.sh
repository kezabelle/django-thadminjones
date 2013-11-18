bumpversion
rm -rf dist/*
rm -rf *.egg-info
rm -rf *.egg
python setup.py clean
python setup.py sdist
python setup.py bdist_egg
python setup.py bdist_wheel
twine upload dist/*
