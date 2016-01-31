This folder is initially empty. It is where the output data produced by the scripts in
[src/micromagnetic_simulation_scripts/](../../src/micromagnetic_simulation_scripts/)
will be placed.

To produce this data, run the following commands in the toplevel directory of this repository.

    make generate-oommf-data
    make generate-nmag-data

Alternatively, you can run the scripts called `generate_data.sh`
in the `oommf` and `nmag` subfolders of
[src/micromagnetic_simulation_scripts/](../../src/micromagnetic_simulation_scripts/).
