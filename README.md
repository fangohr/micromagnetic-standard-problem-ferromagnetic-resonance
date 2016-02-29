[![Circle CI](https://circleci.com/gh/maxalbert/micromagnetic-standard-problem-ferromagnetic-resonance_v3_rewrite.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/maxalbert/micromagnetic-standard-problem-ferromagnetic-resonance_v3_rewrite)

# Proposal of a micromagnetic standard problem for ferromagnetic resonance simulations

This repository accompanies the paper _"Proposal of a standard problem for ferromagnetic resonance simulations"_ available at _[...]_.
It provides data files and scripts which allow the reader to reproduce these results. Alternatively, you can use this code as a basis to apply
it to their own micromagnetic problems.

Start by reading [Quick start](#quick-start) below to get an overview of the contents of this repository and the different ways
in which you can use it.

----------

**Authors:**
Alexander Baker, Marijan Beg, Gregory Ashton, Weiwei Wang,
Maximilian Albert, Dmitri Chernyshenko, Shilei Zhang, Marc-Antonio Bisotti, Matteo Franchin,
Chun Lian Hu, Robert Stamps, Thorsten Hesjedal, and Hans Fangohr*

*fangohr@soton.ac.uk


## Table of contents

- [Quick start](#quick-start)
- [Prerequisites](#prerequisites)
- [Repository structure](#repository-structure)
- [Running the scripts and tests in this repository](#running-the-scripts-and-tests-in-this-repository)
- [Detailed installation instructions for prerequisites](#detailed-installation-instructions-for-prerequisites)


## Quick start

_Before you start, check the [prerequisites](#prerequisites) to make sure you have the necessary software installed._

Depending on your interest and expertise, you can use this repository in different ways:

1. Download or browse the [data files](./micromagnetic_simulation_data/reference_data/oommf/) underlying the main figures 2-5 in the paper.

2. Re-produce figures 2-5 from our pre-computed reference data (no micromagnetic software needed):

   `make reproduce-figures-from-oommf-reference-data`

3. Run our micromagnetic simulation scripts to recompute the raw data files (OOMMF required):

   `make recompute-oommf-data`

   Then compare the recomputed data with our reference data (to verify that you obtain the same results on your computer):

   `make compare-data`

4. Produce figures 2-5 from the freshly computed micromagnetic simulation data from the previous step.
   This is useful to verify that you get the same output plots on your machine.

   `make reproduce-figures-from-oommf-recomputed-data`

5. If you have run the standard problem proposed in the paper with your own micromagnetic software, you can use our plotting code to visualise and compare the results. (Advanced.)


The remainder of this document describes the structure of this
repository and gives a brief overview of its contents. Then we
explain in more details the different ways in which you may want
to use it.


## Prerequisites

To run the code in this repository, the following software must be
installed. For reference, we list the version numbers which we use for
testing, but the code should work with most other versions as well.

* [OOMMF](http://math.nist.gov/oommf/) (1.2.0.4, built from [this tarball](http://math.nist.gov/oommf/dist/oommf12a6_20150930.tar.gz))
* [Python](https://www.python.org) (3.5.1)
* Python modules:
  * numpy (1.10.4)
  * scipy (0.17.0)
  * matplotlib (1.5.1)
  * py.test (2.8.5) _(to run the automated tests)_
* [git](https://git-scm.com/) (2.6.4) _(optional, required to clone the repository. Download zip file as alternative.)_
* [Nmag](http://nmag.soton.ac.uk/nmag/) (0.2.1) _(optional)_

_TODO: Mention the versions that are required (if any), or at least the ones we used for testing._

The easiest and most convenient way of installing these prerequisites
is by using `conda` as described in the [detailed installation
instructions](#detailed-installation-instructions-for-prerequisites)
below.

Using `conda` has multiple advantages: the installation works the same
way for all operating systems, everything is installed locally in your
home directory so that it does not interfere with your system installation,
and you can easily remove everything should you wish to do so.

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
│   │   ├── oommf/
│   │   └── nmag/
│   └── recomputed_data/
│
├── figures/
│   ├── reference_plots_from_paper/
│   ├── generated_from_reference_data/
│   └── generated_from_recomputed_data/
│
├── src/
│   ├── micromagnetic_simulation_scripts/
│   │   ├── oommf/
│   │   └── nmag/
│   ├── postprocessing/
│   └── reproduce_figures.py
│
└── tests/
```


- `micromagnetic_simulation_data/`

  - `reference_data/`

    The "raw" micromagnetic simulation data that we used to produce
    figures 2-5 in the paper (it was generated using the scripts in
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

    This folder contains the exact plots that were used for figures
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

    This folder contains scripts for both OOMMF and Nmag which
    implement the simulation setup for the proposed standard
    problem described in our paper. You can run these scripts
    to re-compute the "raw" data that serves as the basis for
    our figures.

  - `postprocessing/`

    This folder contains a small Python module to facilitate the
    reading of raw simulation data in various formats and
    plotting of the figures.

  - `reproduce_figures.py`

    A Python script which allows you to conveniently produce the plots
    for figures 2-5 from micromagnetic simulation data (both from our
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
     reference data as input. Produces the plots for figures 2-5 and
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
     computed in step (iii) as input. Produces the plots for figures
     2-5 and places them in the output directory
     `figures/generated_from_recomputed_data/oommf/`.




### Running the scripts and tests in this repository

_Before you start, check the [prerequisites](#prerequisites) to make sure you have the necessary software installed._

If you are using conda (see [instructions below](#detailed-installation-instructions-for-prerequisites)),
make sure that your conda environment for this repository is activated:

  ````
  source activate fmr-stdproblem
  ````

Clone this repository and change into the newly created directory.

  ````
  git clone https://github.com/maxalbert/micromagnetic-standard-problem-ferromagnetic-resonance_v3_rewrite.git
  cd micromagnetic-standard-problem-ferromagnetic-resonance_v3_rewrite
  ````

If you want to run all the steps described below at once, simply run:
```
make all
```
This runs the following sub-steps, which you can also perform individually.

- Run the unit tests to check that everything is installed correctly. (This step is optional but recommended.)

  ````
  make unit-tests
  ````

- Reproduce the plots for figures 2-5 using our pre-computed reference data:

  ````
  make reproduce-figures-from-oommf-reference-data
  ````

  If the unit tests passed then this step should also work.
  Because this step uses pre-computed data it does not
  require any micromagnetic software to be installed.
  The resulting plots are placed in the directory
  `figures/generated_from_reference_data/oommf/`.

- Recompute the raw data by running the OOMMF simulation scripts:

  ````
  make recompute-oommf-data
  ````

  This will produce four "raw" data files (`dynamic_txyz.txt`, `mxs.npy`, `mys.npy`, `mzs.npy`)
  in the directory `micromagnetic_simulation_data/recomputed_data/oommf/`.

- Compare the freshly computed data from the previous step with our reference data to ensure that both coincide.

  ```
  make compare-data
  ```

  This reads the data files in the two directories `micromagnetic_simulation_data/reference_data/`
  and `micromagnetic_simulation_data/recomputed_data/` and compares them numerically. If the difference
  is above a small threshold (close to machine precision), the test fails.

- Reproduce the plots for figures 2-5 using the freshly computed reference data.

  ```
  make reproduce-figures-from-oommf-recomputed-data
  ```
  The resulting plots are placed in the directory
  `figures/generated_from_recomputed_data/oommf/`.


## Detailed installation instructions for prerequisites

These instructions assume that you are on some kind of Linux/Unix
system. While the code should certainly work on Windows, we have not
tested this and some of the instructions below may need tweaking.
Also, unfortunately we do not currently provide a conda package for
OOMMF so that you need to install OOMMF yourself (see
[instructions](http://math.nist.gov/oommf/software-12.html) on the
OOMMF homepage). If you use Windows and find any missing steps then
feel free to contact us, or even better submit a pull request (PR) for
this repository.

The easiest way of installing all the prerequisites is using the package manager [`conda`](http://conda.pydata.org/docs/).
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
  so if you add this manually then make sure it points to the correct location of your installation (`conda`
  will print this information at the end of the installation procedure).

3. To activate the conda installation, run
   ````
  source ~/.bashrc
   ````

  Alternatively, opening a new terminal window is likely to achieve the same. This step makes the conda executable available in the terminal.
  
4. Create a new conda environment called `fmr-stdproblem` which contains all necessary packages (these are specified in the file `environment.yml`).

  ````
  conda env create --name fmr-stdproblem -f environment.yml
  ````

5. Activate the newly created environment.

  ````
  source activate fmr-stdproblem 
  ````

This should provide all the necessary prerequisites. If you ever want to delete the conda installation,
simply remove the folder where conda was installed (for example, `~/miniconda3`) and remove the line
from your `~/.bashrc` file that was added in step 2 above.
