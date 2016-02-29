TEST_RUNNER ?= py.test
TEST_OPTIONS ?= --capture=no --verbose

all: unit-tests

unit-tests:
	$(TEST_RUNNER) $(TEST_OPTIONS) unit_tests/

compare-data:
	$(TEST_RUNNER) $(TEST_OPTIONS) compare-data/

.PHONY: all unit-tests
