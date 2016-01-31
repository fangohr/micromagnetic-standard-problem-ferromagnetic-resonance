This directory contains tests for our code. Run them as follows:

    make unit-tests
    make reproduce-figures

They operate at various levels:

- [unit_tests/](./unit_tests/)

  These tests ensure that the code in the [postprocessing/](../src/postprocessing/)
  module works correctly. They use manually generated "fake" data to ensure that the
  output of computations can be compared to the expected result.

- [reproduce_figures/](./reproduce_figures/)

  These tests re-generate the actual figures in the paper, both from pre-computed
  micromagnetis simulation data and from data that was computed "from scratch" using
  the scripts in [src/micromagnetic_simulation_scripts/oommf/](../src/micromagnetic_simulation_scripts/oommf/).
  The resulting plots are compared with images that were produced before (using the
  unit-tested code) and visually inspected to ensure they are correct.

