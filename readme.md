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

### Instructions

Each folder contains the scripts to create figures 2,3,4 and 5 from the report
for a particular software. These figures correspond to the standard-problem and
can be used for comparing between the softwares. Each folder contains a `Make`
file which can be run in two ways:

1. To produce the data: enter the folder and execute `make data`.

2. To produce the figures: enter the folder and execute `make`.2. If the first
   step has not been run, these figures are produced using cached data. If you
   overwrite the cached data and wish to retrieve it, this can be done with:

    $ git checkout Dynamic_txyz.txt mxs.npy mys.npy mzs.npy
