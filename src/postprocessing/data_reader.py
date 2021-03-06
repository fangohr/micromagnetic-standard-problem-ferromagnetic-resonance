import numpy as np
import os

from . import util

#
# If you'd like to support more data formats in addition to the
# existing support for OOMMF, Nmag then you need to create a new
# subclass of BaseDataReader (similar to OOMMFDataReader and
# NmagDataReader above) and add it to `data_reader_classes` below.
#
# The methods you need to implement are:
#
#   _get_timesteps()
#   _get_average_magnetisation()
#   _get_spatially_resolved_magnetisation()
#
# (Note the leading underscore in the names.)
#

class BaseDataReader(object):
    """
    This class encapsulates the reading of raw simulation data from
    a data directory. It provides a unified interface to the output
    generated by various micromagnetic simulation softwares (e.g.
    OOMMF, Nmag) which store their simulation output in different
    formats.

    """

    EXPECTED_DATA_FILES = None  # needs to be overwritten by derived classes

    def __init__(self, data_dir):
        self.data_dir = data_dir
        self._check_expected_data_files_exist()

    def _check_expected_data_files_exist(self):
        """
        Check that all files in `self.EXPECTED_DATA_FILES` exist.
        Raises RuntimeError if one of those files is not found.

        """
        expected_files = [os.path.join(self.data_dir, fname) for fname in self.EXPECTED_DATA_FILES]

        for f in expected_files:
            if not os.path.exists(f):
                raise RuntimeError("Expected data file does not exist: '{}'".format(f))

    def get_timesteps(self, unit='s'):
        """
        Return a 1D numpy array containing the timesteps at which
        the magnetisation was saved during the simulation.

        The argument `unit` can either be 's' (= seconds) or 'ns'
        (= nanoseconds).
        """
        return self._get_timesteps() * util.get_conversion_factor('s', unit)

    def get_dt(self, unit='s'):
        """
        Return float representing the timestep used during the simulation.
        Note that this assumes that all timesteps are equal.

        The argument `unit` can either be 's' (= seconds) or 'ns' (= nanoseconds).
        """
        timesteps = self.get_timesteps(unit)
        return timesteps[1] - timesteps[0]

    def get_num_timesteps(self):
        """
        Return number of timesteps at which the magnetisation was saved
        during the simulation.
        """
        return len(self.get_timesteps())

    def get_average_magnetisation(self, component):
        """
        Return a 1D numpy array containing the values of the
        spatially averaged magnetization sampled at the time-
        steps during the simulation.
        """
        return self._get_average_magnetisation(component)

    def get_spatially_resolved_magnetisation(self, component):
        """
        Return a 3D numpy array containing the values of the spatially
        resolved magnetization for the given magnetisation component
        at all timesteps. The magnetisation is sampled on a regular
        grid of size 24 x 24 in the center of the nano-film so that
        the shape of the returned array is (N, 24, 24), where N is the
        number of timesteps present in the simulation.
        """
        return self._get_spatially_resolved_magnetisation(component)

    def _get_timesteps(self):
        raise NotImplementedError(
            "Data reader of type '{}' does not implement "
            "_get_timesteps()".format(self.__class__.__name__))

    def _get_average_magnetisation(self):
        raise NotImplementedError(
            "Data reader of type '{}' does not implement reading of "
            "spatially averaged magnetisation data.".format(self.__class__.__name__))

    def _get_spatially_resolved_magnetisation(self, component):
        raise NotImplementedError(
            "Data reader of type '{}' does not implement reading of "
            "spatially resolved magnetisation data.".format(self.__class__.__name__))


class OOMMFDataReader(BaseDataReader):
    EXPECTED_DATA_FILES = ['dynamic_txyz.txt', 'mxs.npy', 'mys.npy', 'mzs.npy']

    def __init__(self, data_dir):
        super(OOMMFDataReader, self).__init__(data_dir)

        data_avg_filename = os.path.join(self.data_dir, 'dynamic_txyz.txt')
        self.data_avg = np.loadtxt(data_avg_filename)

    def _get_timesteps(self):
        # Timestamps are contained in the first column of the averaged data
        return self.data_avg[:, 0]

    def _get_average_magnetisation(self, component):
        idx = util.get_index_of_m_avg_component(component)
        return self.data_avg[:, idx]

    def _get_spatially_resolved_magnetisation(self, component):
        filename = os.path.join(self.data_dir, 'm{}s.npy'.format(component))
        m = np.load(filename)
        return m.reshape(-1, 24, 24)


class NmagDataReader(BaseDataReader):
    EXPECTED_DATA_FILES = ['dynamic_txyz.txt', 'mxs.npy', 'mys.npy', 'mzs.npy']

    def __init__(self, data_dir):
        super(NmagDataReader, self).__init__(data_dir)

        data_avg_filename = os.path.join(self.data_dir, 'dynamic_txyz.txt')
        self.data_avg = np.loadtxt(data_avg_filename)

    def _get_timesteps(self):
        # Timestamps are contained in the first column of the averaged data
        return self.data_avg[:, 0]

    def _get_average_magnetisation(self, component):
        idx = util.get_index_of_m_avg_component(component)
        return self.data_avg[:, idx]

    def _get_spatially_resolved_magnetisation(self, component):
        filename = os.path.join(self.data_dir, 'm{}s.npy'.format(component))
        m = np.load(filename)
        return m.reshape(-1, 24, 24)


data_reader_classes = {
    'OOMMF': OOMMFDataReader,
    'Nmag': NmagDataReader,
    }


def DataReader(data_path, data_format):
    """
    """
    try:
        cls = data_reader_classes[data_format]
    except KeyError:
        supported_data_formats = list(data_reader_classes.keys())
        raise ValueError(
            ("Unsupported data format: '{}'. Supported values: {} "
             "".format(data_format, supported_data_formats)))

    return cls(data_path)
