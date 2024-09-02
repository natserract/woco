install:
	pyenv exec python3 -m venv .venv
	. .venv/bin/activate && python setup.py install

build-package:
	pip install build
	python -m build

clean:
	rm -rf __pycache__
	rm -rf .venv
