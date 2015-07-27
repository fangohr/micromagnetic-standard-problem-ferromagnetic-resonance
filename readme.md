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

### Installation

To get started please begin with

    $ python setup.install install

This will install a python module `micromagnetic_standard_problem_FMR` required
to generate the figures.

## Structure of this repository

For each software package, we have a directory containing the scripts required
to run the standard_problem and a second folder containing the cached data
(simulation results).

## How to reproduce the results 
