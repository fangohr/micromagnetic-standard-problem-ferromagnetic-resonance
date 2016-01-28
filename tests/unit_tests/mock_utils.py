import numpy as np
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

    def make_m_avg(self, oscillation_cycles, amplitudes=None, damping=0):
        """
        Create precession of a single magnetisation component (e.g. `m_x`).

        The resulting precession is a superposition of pure cosine waves
        whose cycles are specified in the argument `oscillation_cycles`.
        Different amplitudes can optionally be specified through the
        argument `amplitudes` (default: all amplitudes equal to 1).

        For example,

            make_m_avg(oscillation_cycles=[5, 12, 42], amplitudes=[1, 1, 0.5])

        would create a superposition of three cosine waves with 5, 12
        and 42 oscillation cycles, respectively, where the third one
        has half the amplitude of the other two.

        If damping is zero (the default) then the Fourier transform of
        the resulting signal contains non-zero Fourier coefficients at
        precisely the frequencies corresponding to the given oscillation
        cycles.

        *Returns*

        A 1D array containing the magnetisation values at the timesteps
        specified during initialisation.

        """
        if amplitudes is None:
            amplitudes = np.ones_like(oscillation_cycles)

        num_timesteps = len(self.timesteps)
        normalisation_factor = 1. / (num_timesteps // 2)

        m = np.zeros(num_timesteps)
        for num_oscillations, amplitude in zip(oscillation_cycles, amplitudes):
            m += normalisation_factor * amplitude * \
                 np.cos(num_oscillations * (2*np.pi) * self.timesteps / max(self.timesteps)) * \
                 np.exp(damping * self.timesteps * 1e9)

        return np.vstack([self.timesteps, m, m, m]).transpose()


class FakeDataReader(BaseDataReader):
    """
    Implementation of DataReader which does not read the data from
    files but instead returns generated data with a known spectrum
    that can be used for testing.

    """

    def __init__(self):
        self.oscillation_cycles = [20, 47, 100, 240]
        self.amplitudes = [0.8, 0.27, 0.04, 0.65]
        self.damping = 0.0

        timesteps = np.linspace(5e-12, 20e-9, 4000)
        self.ringdown_generator = FakeRingdownGenerator(timesteps)

        self.data_avg = self._read_average_magnetisation_data()

    def _read_average_magnetisation_data(self):
        """
        Return 1d numpy array representing a ringdown which is the
        superposition of various oscillations at different frequencies.

        We don't bother inventing different data for the different magnetisation
        components but simply return the same data for `m_x`, `m_y`, `m_z`.

        """
        return self.ringdown_generator.make_m_avg(self.oscillation_cycles, self.amplitudes, self.damping)

    def _read_spatially_resolved_magnetisation_data(self, component):
        """
        Return 3d numpy array of shape N x 24 x 24 representing a ringdown
        which is the superposition of various oscillations at different
        frequencies. Here `N` is the number of timesteps and 24 x 24 is the
        size of the sampling grid.

        We don't bother inventing different data for the different magnetisation
        components but simply return the same data for `m_x`, `m_y`, `m_z`.

        """
        # We don't bother inventing different data for the different magnetisation components.
        # Extend m_avg on a 24 x 24 grid to pretend it's spatially resolved
        m_avg_x = self.get_average_magnetisation(component)
        self.m_x = m_avg_x[:, np.newaxis, np.newaxis].repeat(24, axis=1).repeat(24, axis=2)

        m_avg = self.get_average_magnetisation(component)
        return m_avg.reshape(-1, 24, 24)
