OOMMF_DATA_DIR = micromagnetic_simulation_data/generated_data/oommf
OOMMF_OUTPUT_FILENAMES = dynamic_txyz.txt mxs.npy mys.npy mzs.npy

# Generate the list OOMMF_OUTPUT_FILES by prepending OOMMF_DATA_DIR to
# each filename in OOMMF_OUTPUT_FILENAMES.
OOMMF_OUTPUT_FILES = $(foreach filename,$(OOMMF_OUTPUT_FILENAMES),$(OOMMF_DATA_DIR)/$(filename) )


all: unit-tests reproduce-figures

unit-tests:
	make -C tests/unit_tests/

generate-oommf-data: $(OOMMF_OUTPUT_FILES)
$(OOMMF_OUTPUT_FILES):
	@echo "Generating OOMMF data... This may take a while."
	cd src/micromagnetic_simulation_scripts/oommf/ && ./generate_data.sh

reproduce-figures-from-reference-data:
	make -C tests/reproduce_figures/

reproduce-figures-from-scratch: generate-oommf-data
	cd src && python reproduce_figures.py

.PHONY: all unit-tests generate-oommf-data reproduce-figures-from-reference-data reproduce-figures-from-scratch
