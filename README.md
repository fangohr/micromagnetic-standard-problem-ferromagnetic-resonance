[![Circle CI](https://circleci.com/gh/maxalbert/micromagnetic-standard-problem-ferromagnetic-resonance_v3_rewrite.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/maxalbert/micromagnetic-standard-problem-ferromagnetic-resonance_v3_rewrite)

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

- Produce figures 2-5 "from scratch", based on freshly computed micromagnetic simulation data from the previous step.
  This is useful to verify that you get the same results on your own computer.


## Detailed installation and running steps

These instructions assume that you are on some kind of Linux/Unix system.
While the code should certainly work on Windows, we have not tested this
nd some of the instructions below may need tweaking to make them work on
Windows. If you are using Windows and find any missing steps then feel
free to contact us (or even better submit a Pull Request for this
repository).

### Prerequisites

To run the code in this repository, the following software must be installed:

* [OOMMF](http://math.nist.gov/oommf/)
* [Python](https://www.python.org)
* Python modules:
  * numpy
  * scipy
  * matplotlib
  * click
* [git](https://git-scm.com/) (to clone the repository) 
* [Nmag](http://nmag.soton.ac.uk/nmag/) (optional)

_TODO: Mention the versions that are required (if any), or at least the ones we used for testing._

#### Installing required prerequisites using `conda`

The easiest way of getting all the prerequisites installed is using [`conda`](http://conda.pydata.org/docs/).
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

       export PATH=~/miniconda3/bin:$PATH

   Note that the exact path may depend on whether you installed Miniconda or the full Anaconda distribution,
   so if you add this manually then make sure it points to the correct location of your installation.

3. Run `source ~/.bashrc` to activate the conda installation (opening a new terminal window is likely to work as well). This makes the conda executable available in the terminal.

4. Create a new conda environment called `fmr-stdproblem` which contains all necessary packages (these are specified in the file `conda_environment.yml`).

       conda env create --name fmr-stdproblem -f conda_environment.yml

5. Activate the newly created environment

       source activate fmr-stdproblem

This should provide all the necessary requirements. If you ever want to delete the conda installation,
simply remove the folder where conda was installed (for example, `~/miniconda3`) and remove the line
rom your `~/.bashrc` file that was added in step 2 above.


### Running scripts in this repository

- If you are using conda (see instructions above), make sure that your conda environment for this repository is activated:

      source activate fmr-stdproblem

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
