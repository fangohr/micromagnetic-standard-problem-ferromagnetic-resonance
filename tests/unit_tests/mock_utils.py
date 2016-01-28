import numpy as np
from numpy import pi

from postprocessing.data_reader import BaseDataReader


class FakeRingdownGenerator(object):
    """
    This class allows the creation of "fake" magnetisation precessions
    which imitate the ringdown phase in a micromagnetic normal mode
    simulation.

    The resulting signals have very specific spectra and can thus be
    conveniently used for testing.

    """

    def __init__(self, timesteps):
        """
        Initialise ringdown generator with the given timesteps.

        All generated magnetisation data will be based on these timesteps.

        """
        self.timesteps = timesteps

    def make_precession(self, num_cycles, amplitudes=None, damping=0):
        """
        Create precession of a single magnetisation component (e.g. `m_x`).

        The resulting precession is a superposition of pure cosine waves
        whose cycles are specified in the argument `num_cycles`.
        Different amplitudes can optionally be specified through the
        argument `amplitudes` (default: all amplitudes equal to 1).

        For example,

            make_precession(num_cycles=[5, 12, 42], amplitudes=[1, 1, 0.5])

        would create a superposition of three cosine waves with 5, 12
        and 42 oscillation cycles, respectively, where the third one
        has half the amplitude of the other two.

        If damping is zero (the default) then the Fourier transform of
        the resulting signal contains non-zero Fourier coefficients at
        precisely the frequencies corresponding to the given number of
        oscillation cycles.

        *Returns*

        A 1D array containing the magnetisation values at the timesteps
        specified during initialisation.

        """
        if amplitudes is None:
            amplitudes = np.ones_like(num_cycles)

        num_timesteps = len(self.timesteps)
        normalisation_factor = 1. / (num_timesteps // 2)

        result = np.zeros(num_timesteps)
        for N, amplitude in zip(num_cycles, amplitudes):
            result += normalisation_factor * amplitude * \
                 np.cos(N * (2*pi) * self.timesteps / max(self.timesteps)) * \
                 np.exp(damping * self.timesteps * 1e9)

        return result


class FakeDataReader(BaseDataReader):
    """
    Implementation of DataReader which does not read the data from
    files but instead returns generated data with a known spectrum
    that can be used for testing.

    """

    def __init__(self, damping=0.0):
        self.timesteps = np.linspace(5e-12, 20e-9, 4000)
        self.ringdown_generator = FakeRingdownGenerator(self.timesteps)
        self.damping = damping

    def _get_timesteps(self):
        return self.timesteps

    def _get_average_magnetisation(self, component):
        """
        Return 1d numpy array representing a ringdown which is the
        superposition of various oscillations at different frequencies.

        We don't bother inventing different data for the different magnetisation
        components but simply return the same data for `m_x`, `m_y`, `m_z`.

        """
        # Compute the average magnetisation from the spatially resolved
        # data by averaging over the two spatial dimensions.
        m_full = self.get_spatially_resolved_magnetisation(component)
        m_avg = np.mean(m_full, axis=(1, 2))
        return m_avg

    def _get_spatially_resolved_magnetisation(self, component):
        """
        Return 3d numpy array of shape N x 24 x 24 representing a ringdown
        which is the superposition of various oscillations at different
        frequencies. Here `N` is the number of timesteps and 24 x 24 is the
        size of the sampling grid.

        We don't bother inventing different data for the different magnetisation
        components but simply return the same data for `m_x`, `m_y`, `m_z`.

        """
        m1 = self.ringdown_generator.make_precession(num_cycles=[47, 240], amplitudes=[0.27, 0.9], damping=self.damping)
        m2 = self.ringdown_generator.make_precession(num_cycles=[20, 100, 240], amplitudes=[0.8, 0.04, 0.65], damping=self.damping)
        m3 = -m1

        N = len(self.timesteps)
        m = np.zeros((N, 24, 24))

        # Set different oscillation patterns in different parts of the sample
        # (but keep the outside ones symmetric so that they eliminate each other
        # in the average data).
        m[:, :, :8]   = m1[:, np.newaxis, np.newaxis].repeat(24, axis=1).repeat(8, axis=2)
        m[:, :, 8:16] = m2[:, np.newaxis, np.newaxis].repeat(24, axis=1).repeat(8, axis=2)
        m[:, :, 16:]  = m3[:, np.newaxis, np.newaxis].repeat(24, axis=1).repeat(8, axis=2)
        
        return m
