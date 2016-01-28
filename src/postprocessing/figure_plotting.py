import matplotlib.pyplot as plt

from .fft_utils import get_fft_frequencies, get_spectrum_via_method_1, get_spectrum_via_method_2


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


def make_figure_3(data_reader, component='y'):
    """
    Create Fig. 3 in the paper.

    Returns a matplotlib figure with two curves for the power
    spectral densities of the magnetisation dynamics computed
    via method 1 and 2 (as described in section C1 and C2).

    """
    timesteps = data_reader.get_timesteps()
    dt = data_reader.get_dt()

    # Read average and spatially resolved magnetisation (y-component).
    m_avg = data_reader.get_average_magnetisation(component)
    m_full = data_reader.get_spatially_resolved_magnetisation(component)

    # Compute frequencies and power spectrum via the two different methods.
    freqs = get_fft_frequencies(timesteps, unit='GHz')
    psd1 = get_spectrum_via_method_1(m_avg)
    psd2 = get_spectrum_via_method_2(m_full)

    # Plot both power spectra into the same figure
    fig = plt.figure(figsize=(7, 5.5))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(freqs, psd1, label='Method 1')
    ax.plot(freqs, psd2, color='g', lw=2, label='Method 2')
    ax.set_xlabel('Frequency (GHz)')
    ax.set_ylabel('Spectral density')
    ax.set_xlim([0.2, 20])
    ax.set_ylim([1e-5, 1e0])
    ax.set_yscale('log')
    ax.legend(frameon=False)

    return fig
