all: unit-tests

unit-tests:
	make -C tests/unit_tests/

.PHONY: all unit-tests
