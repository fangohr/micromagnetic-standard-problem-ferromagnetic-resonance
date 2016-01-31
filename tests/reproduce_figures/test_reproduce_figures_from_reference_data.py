"""
The tests in this file re-genereate Figures 2-5 in the paper
from pre-computed reference data and check that the resulting
plots are identical with previously generated reference plots.

"""

import matplotlib; matplotlib.use('agg')
from matplotlib.testing.decorators import image_comparison
from pathlib import Path

from postprocessing import DataReader, make_figure_2, make_figure_3, make_figure_4, make_figure_5

TOL = 0

# Get absolute path to the current directory (to avoid problems if
# this script is invoked from somewhere else).
HERE = Path(__file__).parent.resolve()

#
# Define input and output directories.
#
REF_DATA_DIR_OOMMF = HERE.joinpath('../../micromagnetic_simulation_data/reference_data/oommf/')
REF_DATA_DIR_NMAG = HERE.joinpath('../../micromagnetic_simulation_data/reference_data/nmag/')

#
# Create SimulationReader which provides a convenient way of
# reading raw simulation data and computing derived data.
#
data_reader_oommf = DataReader(REF_DATA_DIR_OOMMF, data_format='OOMMF')
data_reader_nmag = DataReader(REF_DATA_DIR_NMAG, data_format='Nmag')


@image_comparison(baseline_images=['figure_2_OOMMF'], extensions=['png', 'pdf'], tol=TOL)
def test__reproduce_figure_2():
    fig = make_figure_2(data_reader_oommf)


@image_comparison(baseline_images=['figure_3_OOMMF'], extensions=['png', 'pdf'], tol=TOL)
def test__reproduce_figure_3():
    fig = make_figure_3(data_reader_oommf)


@image_comparison(baseline_images=['figure_4_OOMMF'], extensions=['png', 'pdf'], tol=TOL)
def test__reproduce_figure_4():
    fig = make_figure_4(data_reader_oommf)


@image_comparison(baseline_images=['figure_5_OOMMF'], extensions=['png', 'pdf'], tol=TOL)
def test__reproduce_figure_5():
    fig = make_figure_5(data_reader_oommf)
