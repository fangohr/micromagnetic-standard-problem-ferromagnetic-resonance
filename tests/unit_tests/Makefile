TEST_RUNNER ?= py.test
TEST_OPTIONS ?= --capture=no --verbose

all: test

test:
	PYTHONPATH=../../src:$$PYTHONPATH $(TEST_RUNNER) $(TEST_OPTIONS) .
