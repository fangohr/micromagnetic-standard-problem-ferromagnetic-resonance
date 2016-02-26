OOMMF_DATA_DIR = micromagnetic_simulation_data/generated_data/oommf
OOMMF_OUTPUT_FILENAMES = dynamic_txyz.txt mxs.npy mys.npy mzs.npy

NMAG_DATA_DIR = micromagnetic_simulation_data/generated_data/nmag
NMAG_OUTPUT_FILENAMES = dynamic_txyz.txt mxs.npy mys.npy mzs.npy

# Generate the list of output files for OOMMF by by prepending
# OOMMF_DATA_DIR to each filename in OOMMF_OUTPUT_FILENAMES
# (and similary for Nmag).
OOMMF_OUTPUT_FILES = $(foreach filename,$(OOMMF_OUTPUT_FILENAMES),$(OOMMF_DATA_DIR)/$(filename) )
NMAg_OUTPUT_FILES = $(foreach filename,$(NMAG_OUTPUT_FILENAMES),$(NMAG_DATA_DIR)/$(filename) )

# Set environment variable needed for the target 'generate-oommf-data'.
# This makes a guess where 'oommf.tcl' is located, based on the assumption
# that OOMMF was installed using conda. If this guess is wrong you need to
# set this environment variable manually.
OOMMFTCL ?= $(shell echo $(shell dirname $(shell which oommf))/../opt/oommf.tcl) \


all: unit-tests reproduce-figures-from-reference-data generate-oommf-data reproduce-figures-from-scratch

unit-tests:
	make -C tests/unit_tests/

generate-oommf-data: $(OOMMF_OUTPUT_FILES)
$(OOMMF_OUTPUT_FILES):
	@cd src/micromagnetic_simulation_scripts/oommf/ && OOMMFTCL=$(OOMMFTCL) ./generate_data.sh

generate-nmag-data: $(NMAG_OUTPUT_FILES)
$(NMAG_OUTPUT_FILES):
	@cd src/micromagnetic_simulation_scripts/nmag/ && ./generate_data.sh

reproduce-figures-from-reference-data:
	make -C tests/reproduce_figures/

reproduce-figures-from-scratch: generate-oommf-data
	cd src && python reproduce_figures.py

.PHONY: all unit-tests generate-oommf-data generate-nmag-data reproduce-figures-from-reference-data reproduce-figures-from-scratch
