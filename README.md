# Proposal of a micromagnetic standard problem for ferromagnetic resonance simulations

Accompanying repository for the paper, available at...

## Authors
Alexander Baker, Shilei Zhang, Weiwei Wang, Gregory Ashton, Marijan Beg,
Maximilian Albert, Dmitri Chernyshenko, Marc-Antonio Bisotti, Matteo Franchin,
Chun Lian Hu, Robert Stamps, Thorsten Hesjedal, and Hans Fangohr*

*fangohr@soton.ac.uk

## Software

To run the code in this repository, the following software must be installed:

* [OOMMF](http://math.nist.gov/oommf/)
* [Nmag](http://nmag.soton.ac.uk/nmag/)
* [Python](https://www.python.org)
* Python modules:
  * numpy
  * matplotlib

### Checking the installation

To check you have the required software:

* For `OOMMF` please check the output of

    ```bash
    $ tclsh $OOMMFTCL +version
    ```

  Note that `$OOMMFTCL` is an environment variable pointing to the installed
  `oommf.tcl` file in the directory where `OOMMF` is installed. This can be
  set in `.bashrc` by

    ```bash
    OOMMFTCL=/path/to/install/oommf/oommf.tcl
    export OOMMFTCL
    ```
	
  For more information on installing and running OOMMF, refer to:
  http://math.nist.gov/oommf/software-12.html

* For `Nmag` check your installation by running

    ```bash
    nsim --version
    ```
    
  For more information on installing and running Nmag, refer to:
  http://nmag.soton.ac.uk
  
## Instructions

### Cloning

To get a local copy of this repository, clone it by running

```bash
git clone git@github.com:fangohr/micromagnetic-standard-problem-ferromagnetic-resonance.git
```

### Reproducing results

This repository contains scripts to reproduce the standard problem results as
presented in the paper. There are two directories in `src/` directory: `nmag_scripts/` and `oommf_scripts/`. Each directory contains the scripts to create figures 2, 3, 4 and 5 from the paper. For each folder we include a `Makefile` which can be run in several ways:

1. To produce figures using the data in the repository, execute `make figures`.

2. To produce the data, execute `make data`.

3. Executing `make clean_all`, deletes all figures and data from the current directory, and then `make all` can be executed. This will generate both the data and figures without using any precomputed (saved) data.

If the data provided by this repository has been overwritten, the data can be retrieved by:

```bash
$ git checkout Dynamic_txyz.txt mxs.npy mys.npy mzs.npy
```

### Nmag mesh discretization

As discussed in the section 3D of the paper, finite element and finite difference techniques produce slightly different results due to their different handling
of demagnetization energy.

The finite element approach can be brought into agreement with finite difference through an appropriate choice of mesh discretization. The standard simulation uses one based on a 5x5x5nm cell size, but in figure 13 we show the spectra resulting from a 2x2x1nm cell size. This mesh is also provided, and can be utilized in simulations by changing the variable `mesh_name` in both `relaxation_stage.py` and `dynamic_stage.py` to `mesh_name = meshes/mesh_221.nmesh.h5`

## Todo
1. Check and proof-read the README in particular the installation instructions
   for OOMMF.

   Marijan: I polished this file and am happy with how it looks.
   The installation of oommf and nmag are never easy, so maybe it is the best
   to refer users to webpages.

2. Understand why the output of the standard problem for `Nmag` varies between
   runs. This can be reproduced by entering `Nmag_standard_problem` and running

    ```bash
    $ make data
    $ mv Dynamic_txyz.txt Dynamic_txyz.txt.old
    $ make data
    ```

   and then comparing `Dynamic_txyz.txt` with `Dynamic_txyz.txt.old`
   
   Marijan: This problem was probably caused by the wrong data committed to the
   repository. I have tested multiple runs on two different machines, and there are
   no differences.

3. Understand why the output `Dynamic_txyz.txt` from `Nmag` is different from `OOMMF`. This can be demonstrated with the cached data already in the repository by running [Todo3.py](Todo3.py)

   Marijan: This problem is now solved and it was caused by the Nmag tolerances. These tolerances are now reduced and agreement is good. We need to discuss whether changing tolerances is ok for standard problem. Also, we should remember to remove Todo.py and comparison.pdf files from the repository later.
