OOMMF_DATA_DIR = micromagnetic_simulation_data/generated_data/oommf
OOMMF_OUTPUT_FILENAMES = dynamic_txyz.txt mxs.npy mys.npy mzs.npy

# Generate the list OOMMF_OUTPUT_FILES by prepending OOMMF_DATA_DIR to
# each filename in OOMMF_OUTPUT_FILENAMES.
OOMMF_OUTPUT_FILES = $(foreach filename,$(OOMMF_OUTPUT_FILENAMES),$(OOMMF_DATA_DIR)/$(filename) )

# Set environment variable needed for the target 'generate-oommf-data'.
# This makes a guess where 'oommf.tcl' is located, based on the assumption
# that OOMMF was installed using conda. If this guess is wrong you need to
# set this environment variable manually.
OOMMFTCL ?= $(shell echo $(shell dirname $(shell which oommf))/../opt/oommf.tcl) \


all: unit-tests reproduce-figures

unit-tests:
	make -C tests/unit_tests/

reproduce-figures:
	make -C tests/reproduce_figures/

generate-oommf-data: $(OOMMF_OUTPUT_FILES)
$(OOMMF_OUTPUT_FILES):
	@cd src/micromagnetic_simulation_scripts/oommf/ && OOMMFTCL=$(OOMMFTCL) ./generate_data.sh

reproduce-figures-from-scratch: generate-oommf-data
	cd src && python reproduce_figures.py

.PHONY: all unit-tests generate-oommf-data reproduce-figures-from-scratch
