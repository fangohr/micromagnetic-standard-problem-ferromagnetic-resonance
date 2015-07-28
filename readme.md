# Proposal of a Micromagnetic Standard Problem for Ferromagnetic Resonance Simulations

Online repository for the paper.

## Authors
Alexander Baker, Shilei Zhang, Weiwei Wang, Gregory Ashton, Marijan Beg,
Maximilian Albert, Dmitri Chernyshenko, Marc-Antonio Bisotti, Matteo Franchin,
Chun Lian Hu, Robert Stamps, Thorsten Hesjedal, and Hans Fangohr

## Software

To run the code in this repository you will need to have installed the following:

* [OOMMF](http://math.nist.gov/oommf/)
* [Nmag](http://nmag.soton.ac.uk/nmag/)
* [Python](https://www.python.org)
* Python modules:
  * numpy
  * matplotlib

### Checking the installation

To check you have the installed software:

* For `OOMMF` please check the output of

    ```bash
    $ tclsh $OOMMFTCL +version
    ```

  Note that `$OOMMFTCL` is an enviroment variable pointing to the installed
  `oommf.tcl` file in the directory where you installed `OOMMF`. This can be
  set in `.bashrc` by

    ```bash
    OOMMFTCL=/path/to/install/oommf/oommf.tcl
    export OOMMFTCL
    ```

    The `export` here is required for the `make` files to run properly.

* For `Nmag` check your installation by running

    ```bash
    nsim --version
    ```

## Instructions

### Cloning

To get a local copy of this directory please clone the repository with

```bash
git clone git@github.com:fangohr/micromagnetic-standard-problem-ferromagnetic-resonance.git
```

### Reproducing results

This repository contains several directories, each of which contains scripts to
reproduce the standard problem for ferromagnetic resonance. In particular each
folder contains the scripts to create figures 2,3,4 and 5 from the report for a
particular software. For each folder we include a a `Make` file which can be
run in two ways:

1. To produce the data: enter the folder and execute `make data`.

2. To produce the figures: enter the folder and execute `make`. If the first
   step has not been run, these figures are produced using cached data. If you
   overwrite the cached data and wish to retrieve it, this can be done with:

    ```bash
    $ git checkout Dynamic_txyz.txt mxs.npy mys.npy mzs.npy
    ```

## Todo
1. Check and prood-read the readme in particular the installation instructions
   for OOMMF

2. Understand why the output of the standard problem for `Nmag` varies between
   runs. This can be reproduced by entering `Nmag_standard_problem` and running

    ```bash
    $ make data
    $ mv Dynamic_txyz.txt Dynamic_txyz.txt.old
    $ make data
    ```

   and then comparing `Dynamic_txyz.txt` with `Dynamic_txyz.txt.old`


3. Understand why the output `Dynamic_txyz.txt` from `Nmag` is different from
   `OOMMF`. This can be demonstrated with the cached data already in the repo
   by running [Todo3.py](Todo3.py)
