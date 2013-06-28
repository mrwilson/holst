REQUIREMENTS=./requirements.txt
SETUP=./setup.py

all: install

install: tests clean
	@python $(SETUP) install

tests: install-deps
	@nosetests

install-deps:
	@pip install --upgrade -q -r $(REQUIREMENTS)

clean:
	@find . -name '*.pyc' | xargs rm
	@rm -rf build dist *.egg-info
