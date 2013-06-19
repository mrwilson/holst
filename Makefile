REQUIREMENTS=./requirements.txt
SETUP=./setup.py

all: install-deps test clean install

install:
	@python $(SETUP) install

tests:
	@nosetests

install-deps:
	@pip install -r $(REQUIREMENTS)

clean:
	@find . -name '*.pyc' | xargs rm
