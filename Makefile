upload:
	python woco/__main__.py run -c examples/mathiaschaize.com/config.yml

remove:
	python woco/__main__.py run remove -c examples/mathiaschaize.com/config.yml -k "jewellery_ring_2024-09-03T23:00:31.877519"

build-source:
	pip install build
	python -m build
	pip install -e .

clean:
	rm -rf __pycache__
	rm -rf .venv
