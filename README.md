[![Circle CI](https://circleci.com/gh/maxalbert/micromagnetic-standard-problem-ferromagnetic-resonance_v3_rewrite.svg?style=svg)](https://circleci.com/gh/maxalbert/micromagnetic-standard-problem-ferromagnetic-resonance_v3_rewrite)

# Proposal of a micromagnetic standard problem for ferromagnetic resonance simulations

This repository accompanies the paper _"Proposal of a standard problem for ferromagnetic resonance simulations"_ available at _[...]_.
It provides data files and scripts which allow the reader to reproduce these results.

Start by reading [Quick start](#quick-start) below to get an overview of the contents of this repository and how you can use it.

## Authors
Alexander Baker, Marijan Beg, Gregory Ashton, Weiwei Wang,
Maximilian Albert, Dmitri Chernyshenko, Shilei Zhang, Marc-Antonio Bisotti, Matteo Franchin,
Chun Lian Hu, Robert Stamps, Thorsten Hesjedal, and Hans Fangohr*

*fangohr@soton.ac.uk


## Quick start

Depending on your interest and expertise, you can use this repository in various ways.

- Download or browse the data files underlying figures 2-5 in the paper.

- Re-produce the main figures 2-5 in the paper from pre-computed reference data. (No micromagnetic software needed.)

- Run our micromagnetic simulation scripts to re-generate the data files (OOMMF required).

  You can then (optionally) produce figures 2-5 from this re-computed data.
  This is useful to verify that you get the same results on your own computer.


## Detailed installation and running steps

These instructions assume that you are on some kind of Linux/Unix system.
While the code should certainly work on Windows, we have not tested this
nd some of the instructions below may need tweaking to make them work on
Windows. If you are using Windows and find any missing steps then fell
free to contact us (or even better submit a Pull Request for this
repository).

### Prerequisites

To run the code in this repository, the following software must be installed:

* [OOMMF](http://math.nist.gov/oommf/)
* [Nmag](http://nmag.soton.ac.uk/nmag/) (optional)
* [Python](https://www.python.org)
* Python modules:
  * numpy
  * scipy
  * matplotlib
  * click
* [git](https://git-scm.com/) (to clone the repository)

_TODO: Mention the versions that are required (if any), or at least the ones we used for testing._

The easiest way of getting all these installed is using [`conda`](http://conda.pydata.org/docs/).
Since conda does not touch your system installation and installs everything in a local directory
(in a subfolder of your home directory by default), you can even do this temporarily to test this
repository and then delete the conda installation folder again, which will bring your system.

The following instructions assume that you are using `conda`. If this is not the case you will
have to install the required dependencies manually or via the package manager of your operating
system.

- Install `conda`. There are two options for this

  - Install the [full Anaconda Python distribution](https://www.continuum.io/downloads).
    This is almost 300 MB in size but comes bundled with a lot of Python packages useful for scientific computing.

  - Install [Miniconda](http://conda.pydata.org/miniconda.html). This is much smaller (ca. 30 MB)  because it only
    makes the `conda` command available and leaves the installation of additional packages to you.

  Either choice is fine. The installation works by simply downloading the installer from one of the links above
  and running it. The installer will not touch your system but install everything into a local folder
  (for example, `~/miniconda3` in your home directory). If you wish to get rid of your conda installation,
  simply delete this folder.

- Add the following line to your `~/.bashrc` file (the installer will offer to do this for you automatically),
  and then run `source ~/.bashrc`.

       export PATH="~/miniconda3/bin:$PATH"

  This makes the conda executable available in the terminal.

- Create a new conda environment, install the packages specified in `conda_environment.yml` (which include the
  requirements listed above) and activate this environment.

      conda env create -f conda_environment.yml
      source activate fmr-stdproblem


### Running scripts in this repository

- Clone this repository and change into the newly created directory.

      git clone https://github.com/maxalbert/micromagnetic-standard-problem-ferromagnetic-resonance_v3_rewrite.git
      cd micromagnetic-standard-problem-ferromagnetic-resonance_v3_rewrite

- Run the unit tests to check that everything is installed correctly. (This step is optional but recommended.)

      make unit-tests

- Reproduce the figures using our pre-computed reference data:

      make reproduce-figures-from-reference-data

  If the unit tests passed then this step should also work because the
  only difference is that it uses 'real' data instead of mock data.

  Because this step uses pre-computed data it does not require any
  micromagnetic software to be installed.

- Re-generate the raw data by running the OOMMF simulation:

      make generate-oommf-data

  This will produce four data files (`dynamic_txyz.txt`, `mxs.npy`, `mys.npy`, `mzs.npy`)
  in the directory `micromagnetic_simulation_data/generated_data/oommf/` in this repository.
  It obviously requires OOMMF to be installed. If you are using `conda` as specified in
  the installation instructions above then OOMMF will automatically be installed.