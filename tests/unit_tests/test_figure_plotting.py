from matplotlib.testing.decorators import image_comparison

from mock_utils import FakeDataReader
from postprocessing import make_figure_2, make_figure_3, make_figure_4, make_figure_5

TOL = 0



@image_comparison(baseline_images=['mock_figure_2'], extensions=['png', 'pdf'], tol=TOL)
def test__make_figure_2():
    data_reader = FakeDataReader()
    fig = make_figure_2(data_reader)


@image_comparison(baseline_images=['mock_figure_3_zero_damping'], extensions=['png', 'pdf'], tol=TOL)
def test__make_figure_3_zero_damping():
    data_reader = FakeDataReader(damping=0)
    fig = make_figure_3(data_reader)


@image_comparison(baseline_images=['mock_figure_3_nonzero_damping'], extensions=['png', 'pdf'], tol=TOL)
def test__make_figure_3_nonzero_damping():
    data_reader = FakeDataReader(damping=0.08)
    fig = make_figure_3(data_reader)


@image_comparison(baseline_images=['mock_figure_4'], extensions=['png', 'pdf'], tol=TOL)
def test__make_figure_4():
    data_reader = FakeDataReader(damping=0.08)
    fig = make_figure_4(data_reader)


@image_comparison(baseline_images=['mock_figure_5'], extensions=['png', 'pdf'], tol=TOL)
def test__make_figure_5():
    data_reader = FakeDataReader(damping=0.08)
    fig = make_figure_5(data_reader)
