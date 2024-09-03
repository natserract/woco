build-source:
	pip install build
	python -m build
	pip install -e .

clean:
	rm -rf __pycache__
	rm -rf .venv
