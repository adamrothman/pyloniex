.PHONY: clean tag test retest

version := $(shell python3 setup.py --version)

clean:
	find . -name "*.pyc" -delete
	find . -name ".DS_Store" -delete
	find . -name "__pycache__" -delete
	rm -rf .mypy_cache
	rm -rf pyloniex.egg-info

tag:
	git tag $(version)

# Testing

test:
	tox --recreate

retest:
	tox
