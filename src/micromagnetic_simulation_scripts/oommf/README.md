To run the simulation scripts in this directory, first set the environment
variable `OOMMFTCL` to the location of the file `oommf.tcl` in your OOMMF
installation:
```
export OOMMFTCL=/path/to/oomf.tcl
```

Then run:
```
bash generate_data.sh
```

This will run both the relaxation and the dynamic stage of the simulation.

The generated output files will be placed in the directory
`micromagnetic_simulation_data/recomputed_data/oommf/`.
