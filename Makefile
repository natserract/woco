install:
	pyenv exec python3 -m venv .venv
	. .venv/bin/activate && python setup.py install

dev:
	python woco/__main__.py

build-package:
	pip install build
	python -m build
	pip install -e .

clean:
	rm -rf __pycache__
	rm -rf .venv
