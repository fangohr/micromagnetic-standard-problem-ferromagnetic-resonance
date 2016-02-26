Contents of this folder:

- [reference_plots_from_paper/](./reference_plots_from_paper/)

  The plots that were used for Figures 2-5 in the paper (in .png and .pdf format).

- [generated_from_reference_data/](./generated_from_reference_data/)

  Initially empty. It is where the plots generated from reference data in
  [micromagnetic_simulation_data/reference_data/](../micromagnetic_simulation_data/reference_data/)
  will be placed when running the following command from the toplevel
  folder of this repository.
  ```
  make reproduce-figures-from-oommf-reference-data
  ```

- [generated_from_recomputed_data/](./generated_from_recomputed_data/)

  Initially empty. It is where the plots generated from recomputed data in
  [micromagnetic_simulation_data/recomputed_data/](../micromagnetic_simulation_data/recomputed_data/)
  will be placed when running the following command from the toplevel
  folder of this repository.
  ```
  make reproduce-figures-from-scratch-with-oommf
  ```
  Note that this command will first produce the recomputed data
  (by running `make generate-oommf-data`), so it may take a while
  to complete.