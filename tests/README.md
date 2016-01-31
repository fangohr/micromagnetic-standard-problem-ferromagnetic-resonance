This directory contains tests for our code that operate at various levels.
Run them as follows:

    make unit-tests
    make reproduce-figures


- `unit_tests/`

  These tests ensure that the code in the [postprocessing/](../src/postprocessing/)
  module works correctly. They use hand-crafted "fake" data to ensure that the
  output of computations can be compared to the expected result.

- `reproduce_figures/`

  These tests re-generate the actual figures in the paper, both from pre-computed
  micromagnetic simulation data and from data that was computed "from scratch" using
  the scripts in [src/micromagnetic_simulation_scripts/oommf/](../src/micromagnetic_simulation_scripts/oommf/).
  The resulting plots are compared with images that were produced previously (using the
  unit-tested code) and visually inspected to ensure they are correct.

