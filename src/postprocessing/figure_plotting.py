import matplotlib.pyplot as plt

from .fft_utils import get_fft_frequencies, get_spectrum_via_method_1


def make_figure_2(data_reader, component='y',
                  xlim_upper=[0, 2.5], ylim_upper=None,
                  xlim_lower=[0.1, 20], ylim_lower=[1e-5, 1.]):
    """
    Reproduce Figure 2 in the paper.

    Returns a matplotlib figure with two sub-figures showing (a) the ringdown
    dynamics of the spatially averaged y-component of the magnetisation, m_y,
    and (b) the power spectrum obtained from a Fourier transform of m_y.

    You can set the argument `component` to "x" or "z" to plot the ringdown
    dynamics and power spectrum for m_x or m_z, respectively.

    The extra arguments `xlim_upper`, `ylim_upper`, `xlim_lower`,`ylim_lower`
    can be used to set specific axis limit for the top/bottom subplot. This
    is useful when comparing figures generated from different data (for
    example OOMMF, Nmag).

    """

    # Read timesteps and spatially averaged magnetisation
    ts = data_reader.get_timesteps(unit='ns')
    mys = data_reader.get_average_magnetisation(component)

    # Compute power spectrum from averaged magnetisation
    ts_seconds = data_reader.get_timesteps(unit='s')
    freqs = get_fft_frequencies(ts_seconds, unit='GHz')
    spectrum = get_spectrum_via_method_1(mys)

    # Create two subplots into which we can draw magnetisation dynamics
    # and power spectrum, respectively.
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(8, 6))

    # Plot ringdown dynamics into first subplot.
    ax1.plot(ts, mys)
    ax1.set_xlabel('Time (ns)')
    ax1.set_ylabel('Magnetisation in {}'.format(component.upper()))
    ax1.set_xlim(xlim_upper)
    ax1.set_ylim(ylim_upper)

    # Plot power spectrum into second subplot.
    ax2.plot(freqs, spectrum, '-', label='Real')
    ax2.set_xlabel('Frequency (GHz)')
    ax2.set_ylabel('Spectral density')
    ax2.set_xlim(xlim_lower)
    ax2.set_ylim(ylim_lower)
    ax2.set_yscale('log')

    fig.tight_layout()
    return fig
