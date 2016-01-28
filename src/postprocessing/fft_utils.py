import numpy as np

from . import util


def get_fft_frequencies(timesteps, unit='Hz'):
    """
    Return the FFT sample frequencies for the given timesteps.

    The argument `unit` determines the unit of the returned
    frequencies. It can be either 'Hz' or 'GHz'.

    Note: The timesteps passed into this function must be given
          in units of second (not nanosecond)!
    """
    n = len(timesteps)
    dt = timesteps[1] - timesteps[0]
    freqs = np.fft.rfftfreq(n, dt)

    # FIXME: We ignore the last element for now so that we can compare with the existing data.
    return freqs[:-1] * util.get_conversion_factor('Hz', unit)


def get_spectrum_via_method_1(m_avg):
    """Compute power spectrum from spatially averaged magnetisation dynamics.

    The returned array contains the power spectral densities `S_y(f)` as
    defined in Eq. (1) of the paper.

    Parameters
    ----------
    m_avg :  1D numpy array

        Time series representing dynamics of a single component of
        the spatially averaged magnetisation (for example `m_y`).

    Returns
    -------
    numpy.array

        Power spectral densities of the Fourier-transformed magnetisation data.

    """
    fft_m_avg = np.fft.rfft(m_avg, axis=0)
    spectrum_m_avg = np.abs(fft_m_avg)**2
    # FIXME: We ignore the last element for now so that we can
    #        compare with the existing reference data.
    return spectrum_m_avg[:-1]
