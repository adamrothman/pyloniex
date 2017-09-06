.PHONY: clean tag test retest

version := $(shell python3 setup.py --version)

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	find . -name ".DS_Store" -delete
	rm -rf pyloniex.egg-info

tag:
	git tag $(version)

# Testing

test:
	tox --recreate

retest:
	tox
