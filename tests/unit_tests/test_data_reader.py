import numpy as np
from nose.tools import assert_equals, assert_true, assert_raises
from pathlib import Path

from postprocessing import DataReader
from .mock_utils import FakeDataReader

HERE = Path(__file__).parent.resolve()
REF_DATA_DIR = HERE.joinpath('../../micromagnetic_simulation_data/reference_data/')


class DataReaderTestBase(object):
    """
    Base class for tests of the `DataReader` class. These are run for
    particular data formats ('OOMMF', 'Nmag', etc.) in the specific
    subclasses `TestDataReaderOOMMF`, `TestDataReaderNmag` below.

    """

    def test__get_timesteps_returns_expected_timesteps_from_reference_data(self):
        """
        DataReader.get_timesteps() returns expected timesteps from reference data.
        """
        # Read timesteps (in units of seconds and nanoseconds).
        timesteps = self.data_reader.get_timesteps()
        timesteps_ns = self.data_reader.get_timesteps(unit='ns')

        # Create arrays of expected timesteps.
        #
        # Note that the initial timestep at t=0 is not present
        # in the data, i.e. the timesteps start at t=5 ps.
        timesteps_expected = np.linspace(5e-12, 20e-9, 4000)
        timesteps_ns_expected = timesteps_expected * 1e9

        assert_true(np.allclose(timesteps, timesteps_expected, atol=0, rtol=1e-13))
        assert_true(np.allclose(timesteps_ns, timesteps_ns_expected, atol=0, rtol=1e-13))

    def test__get_num_timesteps_returns_number_of_timesteps_present_in_reference_data(self):
        """
        DataReader.get_num_timesteps() returns number of timesteps present in reference data.
        """
        num_timesteps = self.data_reader.get_num_timesteps()

        assert_equals(num_timesteps, 4000)

    def test__get_average_magnetisation_returns_array_of_expected_shape(self):
        """
        DataReader.get_average_magnetisation() returns 1D array of expected shape.
        """
        for component in ('x', 'y', 'z'):
            m_avg = self.data_reader.get_average_magnetisation(component)

            assert_equals(m_avg.shape, (4000,))

    def test__get_spatially_resolved_magnetisation_returns_array_of_expected_shape(self):
        """
        DataReader.get_spatially_resolved_magnetisation() returns 3D array of expected shape.
        """
        for component in ('x', 'y', 'z'):
            m_full = self.data_reader.get_spatially_resolved_magnetisation(component)

            assert_equals(m_full.shape, (4000, 24, 24))

    def test__get_dt_returns_expected_timestep_present_in_reference_data(self):
        """
        DataReader.get_dt() returns expected timestep present in reference data.
        """
        dt = self.data_reader.get_dt()

        assert_true(np.allclose(dt, 5e-12, atol=0, rtol=1e-14))

    def test__data_reader_raises_error_if_data_format_is_not_supported(self):
        """
        DataReader raises error during initialisation if data format is not supported.
        """
        assert_raises(ValueError, DataReader, REF_DATA_DIR.joinpath('oommf/'), data_format='Foobar')


class TestDataReaderOOMMF(DataReaderTestBase):
    @classmethod
    def setUpClass(cls):
        """
        Create an instance of `OOMMFDataReader` which can be re-used for each individual test.
        """
        cls.data_reader = DataReader(REF_DATA_DIR.joinpath('oommf/'), data_format='OOMMF')


class TestDataReaderNmag(DataReaderTestBase):
    @classmethod
    def setUpClass(cls):
        """
        Create an instance of `NmagDataReader` which can be re-used for each individual test.
        """
        cls.data_reader = DataReader(REF_DATA_DIR.joinpath('nmag/'), data_format='Nmag')


class TestFakeDataReader(DataReaderTestBase):
    @classmethod
    def setUpClass(cls):
        """
        Create an instance of `NmagDataReader` which can be re-used for each individual test.
        """
        cls.data_reader = FakeDataReader()
