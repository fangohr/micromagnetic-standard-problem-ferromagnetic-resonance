import numpy as np
import scipy.signal

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


def get_spectrum_via_method_2(m_vals):
    """
    Compute power spectrum from spatially resolved magnetisation dynamics.

    The returned array contains the power spectral densities `\tilde{S}_y(f)`
    as defined in Eq. (5) of the paper.

    Parameters
    ----------
    m_vals :  2D or 3D numpy array

        Time series representing dynamics of a single component of
        the spatially resolved magnetisation, sampled on a regular
        grid. It is assumed that time is along the first dimension.
        That is, `data[k, i, j]` contains the magnetisation at
        timestep `t_k` for the grid point `r_{i,j}`.

    dt :  float

        Size of the timestep at which the magnetisation was sampled
        during the simulation (e.g. `dt=5e-12` for every 5 ps).

    Returns
    -------
    Pair of `numpy.array`s

        Frequencies and power spectral densities of the magnetisation
        data. Note that the frequencies are returned in GHz (not Hz).

    """
    assert m_vals.ndim == 3

    N, nx, ny = m_vals.shape
    m_vals = m_vals.reshape(N, -1)

    fft_data_full = np.fft.rfft(m_vals, axis=0)
    spectrum_full = np.abs(fft_data_full)**2
    spectrum_avg = np.mean(spectrum_full, axis=1)

    # FIXME: We ignore the last element for now so that we can compare with the existing data.
    return spectrum_avg[:-1]


def find_peak_frequency(freqs, spectrum, approx_freq):
    """
    Find the peak in the spectrum that is closest to the given
    approximate frequency. Returns the exact frequency of the peak
    extracted from the spectrum of the given magnetisation data.

    *Arguments*

    freqs:  1d numpy array

        The FFT sample frequencies of the spectrum.

    spectrum: 1d numpy array

        The spectrum in which to search for a peak.

    approx_freq: float

        Approximate frequency for the peak to be determined.

    """
    # Find indices of peaks in the signal
    widths = np.linspace(0.1, 1.0, 10)
    peak_indices = scipy.signal.find_peaks_cwt(spectrum, widths)

    # Find and return the peak frequency that is closest to `approx_freq`.
    idx = abs(freqs[peak_indices] - approx_freq).argmin()
    peak_freq = freqs[peak_indices[idx]]

    return peak_freq


def get_mode_amplitudes_at_freq(timesteps, m_vals, peak_freq):
    """
    """
    freqs = get_fft_frequencies(timesteps, unit='GHz')
    spectrum = get_spectrum_via_method_2(m_vals)

    fft_coeffs = np.fft.rfft(m_vals, axis=0)

    idx_peak_freq = abs(freqs - peak_freq).argmin()

    return np.absolute(fft_coeffs[idx_peak_freq, :, :])


def get_mode_phases_at_freq(timesteps, m_vals, peak_freq):
    """
    """
    freqs = get_fft_frequencies(timesteps, unit='GHz')
    spectrum = get_spectrum_via_method_2(m_vals)

    fft_coeffs = np.fft.rfft(m_vals, axis=0)

    idx_peak_freq = abs(freqs - peak_freq).argmin()

    return np.angle(fft_coeffs[idx_peak_freq, :, :])
