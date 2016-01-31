This directory contains the "raw" micromagnetic simulation data used
to produce Figures 2-5 in the paper.

- [reference_data/](./reference_data/) contains pre-computed data from
  which the figures in the paper were actually produced.

- [generated_data/](./generated_data/) is initially an empty folder.
  This is where the output data produced by the scripts in
  [src/micromagnetic_simulation_scripts/](../src/micromagnetic_simulation_scripts/)
  will be placed (e.g. when running `make generate-oommf-data` in
  the toplevel folder of this repository).