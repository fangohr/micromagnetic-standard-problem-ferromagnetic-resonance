# Proposal of a micromagnetic standard problem for ferromagnetic resonance simulations

This repository accompanies the paper _"Proposal of a standard problem for ferromagnetic resonance simulations"_ available at _[...]_.
It provides data files and scripts which allow the reader to reproduce these results. Users can also use this code as a basis to apply
it to their own micromagnetic problems.

Start by reading [Quick start](#quick-start) below. It provides an overview of the contents of this repository and the different ways
in which you can use it.


## Authors
Alexander Baker, Marijan Beg, Gregory Ashton, Weiwei Wang,
Maximilian Albert, Dmitri Chernyshenko, Shilei Zhang, Marc-Antonio Bisotti, Matteo Franchin,
Chun Lian Hu, Robert Stamps, Thorsten Hesjedal, and Hans Fangohr*

*fangohr@soton.ac.uk


## Table of contents

- [Quick start](#quick-start)
- [Prerequisites](#prerequisites)
- [Repository structure](#repository-structure)
- [Detailed installation instructions for prerequisites](#detailed-installation-instructions-for-prerequisites)


## Quick start

_Before you start check the [prerequisites](#prerequisites) to make sure you have the necessary software installed._

Depending on your interest and expertise, you can use this repository in the following ways (in increasing order of difficulty).
These are described in more detail below, but if you are impatient you can simply run the given `make` command for each step.

- Download or browse the [data files](./micromagnetic_simulation_data/reference_data/oommf/) underlying figures 2-5 in the paper.

- Re-produce the main figures 2-5 in the paper from our pre-computed reference data. (No micromagnetic software needed.)

  `make reproduce-figures-from-oommf-reference-data`

- Run our micromagnetic simulation scripts to re-generate the raw data files (OOMMF required).

  `make recompute-oommf-data`

- Produce figures 2-5 "from scratch", based on freshly computed micromagnetic simulation data from the previous step.
  This is useful to verify that you get the same results on your own computer.

  `make reproduce-figures-from-oommf-recomputed-data`

- Run the standard problem with your own micromagnetic software, and use our code to plot and compare the results. (Advanced.)


In the rest of this document we start by describing the structure of
this repository and giving a brief overview of its contents. Then we
explain in more details the different ways in which you may want to
use it.


## Prerequisites

To run the code in this repository, the following software must be installed:

* [OOMMF](http://math.nist.gov/oommf/)
* [Python](https://www.python.org)
* Python modules:
  * numpy
  * scipy
  * matplotlib
* [git](https://git-scm.com/) (optional, required to clone the repository. Download zip file as alternative.) 
* [Nmag](http://nmag.soton.ac.uk/nmag/) (optional)

_TODO: Mention the versions that are required (if any), or at least the ones we used for testing._

The easiest and most convenient way of installing these prerequisites
is by using `conda`. This is described in the [detailed installation
instructions](#detailed-installation-instructions-for-prerequisites)
below.

Using `conda` has multiple advantages: the installation works the same
way for all operating systems, everything is installed locally in your
home directory so that it does not interfere with your system and you
can easily remove everything should you wish to do so.

If you do not want to use `conda` then you can install the
prerequisites manually, for example using `pip` (for Python modules)
and/or using the package manager of your operating system.


## Repository structure

The conceptual layout of this repository is as follows (we have omitted
some files and directories that are not relevant to the end user).

```
.
├── micromagnetic_simulation_data/
│   ├── reference_data/
│   │   └── oommf/
│   │   ├── nmag/
│   └── recomputed_data/
│
├── figures/
│   ├── reference_plots_from_paper/
│   ├── generated_from_reference_data/
│   └── generated_from_recomputed_data/
│
├── src/
│   ├── micromagnetic_simulation_scripts/
│   │   └── oommf/
│   │   ├── nmag/
│   ├── postprocessing/
│   └── reproduce_figures.py
│
└── tests/
```


- `micromagnetic_simulation_data/`

  - `reference_data/`

    The "raw" micromagnetic simulation data that we used to produce
    Figures 2-5 in the paper (it was generated using the scripts in
    the `src/` folder). We provide reference data produced with both
    OOMMF and Nmag.

  - `recomputed_data/`

    Initially empty. When you run the micromagnetic simulation scripts
    in the `src/` folder, they will place their output in this
    directory. This allows you to compare data computed on your
    machine to our reference data in order to check that you get the
    same results.

- `figures/`

  - `reference_plots_from_paper/`

    This folder contains the exact plots that were used for Figures
    2-5 in the paper (in .png and .pdf format). They were generated
    using the scripts in `src/`, applied to the OOMMF reference data.

  - `generated_from_reference_data/`

    `generated_from_recomputed_data/`

    Both of these folders are initially empty. When you run the
    plotting scripts in the `src/` folder, they will place their
    output plots in these directories. This allows you to re-produce
    the plots from our paper (either using the reference data we
    provide, or using data that was re-computed on your own machine)
    to check that you get the same results.

- `src/`

  - `micromagnetic_simulation_scripts/`

    - `oommf/`

      `nmag/`

      These folders contain scripts for both OOMMF and Nmag which
      implement the simulation setup described in our paper. You can
      run these to re-compute the "raw" data that serves as the basis
      for our figures.

  - `postprocessing/`

    This folder contains a small Python module to facilitate the
    reading of raw simulation data and plotting of the figures.

  - `reproduce_figures.py`

    A Python script which allows you to conveniently produce the plots
    for Figures 2-5 from micromagnetic simulation data (both from our
    reference data and from re-computed data).

- `tests/`

  This directory contains our automated test suite. For the most part
  you can ignore the contents, but they provide an easy way to run the
  entire test pipeline and check that you can reproduce our results.

  Running the command
  ```
  make test
  ```
  will perform the following sub-steps.

  1. `make unit-tests`

     Runs a set of tests which check that our own code implementation
     works correctly. These should pass if you have all the
     prerequisites installed correctly. Therefore, an errors in this
     step probably indicates that something is wrong with your setup.

  2. `make reproduce-figures-from-oommf-reference-data`

     Runs the script `src/reproduce_figures.py` using our OOMMF
     reference data as input. Produces the plots for Figures 2-5 and
     places them in the output directory `figures/generated_from_reference_data/oommf/`.

  3. `make recompute-oommf-data`

     Runs the simulation scripts in `src/micromagnetic_simulation_scripts/oommf/`
     to re-compute the "raw" data using OOMMF. The resulting data files are placed
     in `micromagnetic_simulation_data/recomputed_data/oommf/`.

  4. `make compare-data`

     Compares the freshly computed data from step (iii) with our
     reference data to ensure that both coincide.

  5. `make reproduce-figures-from-oommf-recomputed-data`

     Runs the script `src/reproduce_figures.py` using the data
     computed in step (iii) as input. Produces the plots for Figures
     2-5 and places them in the output directory
     `figures/generated_from_recomputed_data/oommf/`.


## Detailed installation instructions for prerequisites

These instructions assume that you are on some kind of Linux/Unix
system. While the code should certainly work on Windows, we have not
tested this and some of the instructions below may need tweaking. If
you use Windows and find any missing steps then feel free to contact
us (or even better submit a Pull Request for this repository).

The easiest way of installing all the prerequisites is using [`conda`](http://conda.pydata.org/docs/).
The `conda` installer allows you to create dedicated Python environments very easily
(similar to Python's `virtualenv`, but in a much cleaner and more powerful way).
It also allows to install non-Python packages and thus provides an easy way of making OOMMF available.

Since conda does not touch your system installation at all and installs everything in a local directory
(in a subfolder of your home directory by default), you can even use conda temporarily to test this
repository. Afterwards you can delete the conda installation folder again, which will bring your system
back into the original state.

Use the following steps to install `conda` and create a conda environment containing all required
dependencies. (If you do not want to use `conda` then you will need to install these manually or
via the package manager of your operating system.)

1. Install `conda`. There are two options for this:

  - Install the [full Anaconda Python distribution](https://www.continuum.io/downloads).
    This is almost 300 MB in size but comes bundled with a lot of Python packages useful for scientific computing.

  - Install [Miniconda](http://conda.pydata.org/miniconda.html). This is much smaller (ca. 30 MB)  because it only
    makes the `conda` command available and leaves the installation of additional packages to you.

  Either choice is fine. The installation works by simply downloading the installer from one of the links above
  and running it. The installer will not touch your system but install everything into a local folder
  (for example, `~/miniconda3` in your home directory). If you wish to get rid of your conda installation,
  simply delete this folder.

2. Make sure that your `~/.bashrc` file contains a  line similar to the following. The conda installer will
  typically offer to add this for you automatically.

  ````
  export PATH=~/miniconda3/bin:$PATH
  ````

  Note that the exact path may depend on whether you installed Miniconda or the full Anaconda distribution,
  so if you add this manually then make sure it points to the correct location of your installation.

3. To activate the conda installation, run
   ````
  source ~/.bashrc
   ````

  Alternatively, opening a new terminal window is likely to achieve the same. This step makes the conda executable available in the terminal.
  
4. Create a new conda environment called `fmr-stdproblem` which contains all necessary packages (these are specified in the file `conda_environment.yml`).

  ````
  conda env create --name fmr-stdproblem -f conda_environment.yml
  ````

5. Activate the newly created environment

  ````
  source activate fmr-stdproblem 
  ````

This should provide all the necessary requirements. If you ever want to delete the conda installation,
simply remove the folder where conda was installed (for example, `~/miniconda3`) and remove the line
rom your `~/.bashrc` file that was added in step 2 above.


### Running scripts in this repository

- If you are using conda (see instructions above), make sure that your conda environment for this repository is activated:

  ````
  source activate fmr-stdproblem
  ````

- Clone this repository and change into the newly created directory.

  ````
  git clone https://github.com/maxalbert/micromagnetic-standard-problem-ferromagnetic-resonance_v3_rewrite.git
  cd micromagnetic-standard-problem-ferromagnetic-resonance_v3_rewrite
  ````
      
- Run the unit tests to check that everything is installed correctly. (This step is optional but recommended.)

  ````
  make unit-tests
  ````

- Reproduce the figures using our pre-computed reference data:

  ````
  make reproduce-figures-from-oommf-reference-data
  ````

  If the unit tests passed then this step should also work because the
  only difference is that it uses 'real' data instead of mock data.

  Because this step uses pre-computed data it does not require any
  micromagnetic software to be installed.

- Re-generate the raw data by running the OOMMF simulation:

  ````
  make generate-oommf-data
  ````

  This will produce four data files (`dynamic_txyz.txt`, `mxs.npy`, `mys.npy`, `mzs.npy`)
  in the directory `micromagnetic_simulation_data/recomputed_data/oommf/` in this repository.
  It obviously requires OOMMF to be installed. If you are using `conda` as specified in
  the installation instructions above then OOMMF will automatically be installed.
