import matplotlib; matplotlib.use('agg')
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib import cm

from .fft_utils import \
    get_fft_frequencies, get_spectrum_via_method_1, get_spectrum_via_method_2, \
    find_peak_frequency, get_mode_amplitudes_at_freq, get_mode_phases_at_freq


def rescale_cmap(cmap_name, low=0.0, high=1.0, plot=False):
    import matplotlib._cm as _cm
    '''
    Example 1:
    # equivalent scaling to cplot_like(blah, l_bias=0.33, int_exponent=0.0)
    my_hsv = rescale_cmap('hsv', low = 0.3)
    Example 2:
    my_hsv = rescale_cmap(cm.hsv, low = 0.3)
    '''
    if type(cmap_name) is str:
        cmap = eval('_cm._%s_data' % cmap_name)
    else:
        cmap = eval('_cm._%s_data' % cmap_name.name)
    LUTSIZE = plt.rcParams['image.lut']
    r = np.array(cmap['red'])
    g = np.array(cmap['green'])
    b = np.array(cmap['blue'])
    range = high - low
    r[:, 1:] = r[:, 1:] * range + low
    g[:, 1:] = g[:, 1:] * range + low
    b[:, 1:] = b[:, 1:] * range + low
    _my_data = {'red': tuple(map(tuple, r)),
                'green': tuple(map(tuple, g)),
                'blue': tuple(map(tuple, b))
                }
    my_cmap = mpl.colors.LinearSegmentedColormap('my_hsv', _my_data, LUTSIZE)

    if plot:
        print('plotting')
        plt.figure()
        plt.plot(r[:, 0], r[:, 1], 'r', g[:, 0], g[:, 1], 'g', b[:, 0],
                 b[:, 1], 'b', lw=3)
        plt.axis(ymin=-0.2, ymax=1.2)
        plt.show()

    return my_cmap

my_hsv = rescale_cmap(cm.hsv, low=0.3, high=0.8, plot=False)


CMAP_AMPLITUDE = cm.coolwarm
CMAP_PHASE = my_hsv

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
    spectrum_1 = get_spectrum_via_method_1(m_avg)
    spectrum_2 = get_spectrum_via_method_2(m_full)

    # Plot both power spectra into the same figure
    fig = plt.figure(figsize=(7, 5.5))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(freqs, spectrum_1, label='Method 1')
    ax.plot(freqs, spectrum_2, color='g', lw=2, label='Method 2')
    ax.set_xlabel('Frequency (GHz)')
    ax.set_ylabel('Spectral density')
    ax.set_xlim([0.2, 20])
    ax.set_ylim([1e-5, 1e0])
    ax.set_yscale('log')
    ax.legend(frameon=False)

    return fig


def plot_mode_component(ax, data, label, vmin, vmax, cmap):
    ax.imshow(data, cmap=cmap, vmin=vmin, vmax=vmax, origin='lower')
    ax.set_title(label)
    ax.set_xticks([])
    ax.set_yticks([])


def plot_colorbar(ax, label, cmap, vmin, vmax, num_ticks, ticklabels=None):
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    ticks = np.linspace(vmin, vmax, num_ticks)
    cbar = mpl.colorbar.ColorbarBase(
               ax, cmap, norm=norm, orientation='vertical', ticks=ticks)
    cbar.set_label(label)
    if ticklabels:
        cbar.ax.set_yticklabels(ticklabels)


def plot_mode_at_frequency(data_reader, freq):
    """
    Plot mode at the given frequency (in Hz).
    """
    m_x = data_reader.get_spatially_resolved_magnetisation('x')
    m_y = data_reader.get_spatially_resolved_magnetisation('y')
    m_z = data_reader.get_spatially_resolved_magnetisation('z')

    timesteps = data_reader.get_timesteps(unit='s')

    amp_x = get_mode_amplitudes_at_freq(timesteps, m_x, freq)
    amp_y = get_mode_amplitudes_at_freq(timesteps, m_y, freq)
    amp_z = get_mode_amplitudes_at_freq(timesteps, m_z, freq)

    phase_x = get_mode_phases_at_freq(timesteps, m_x, freq)
    phase_y = get_mode_phases_at_freq(timesteps, m_y, freq)
    phase_z = get_mode_phases_at_freq(timesteps, m_z, freq)

    # Ensure that all three amplitude plots are on the same scale:
    minVal = np.min([amp_x, amp_y, amp_z])
    maxVal = np.max([amp_x, amp_y, amp_z])

    fig = plt.figure(figsize=(8, 6))
    gs = gridspec.GridSpec(2, 4, width_ratios=[4, 4, 4, 0.5],
                                 height_ratios=[4, 4])
    axes = [fig.add_subplot(g) for g in gs]

    plot_mode_component(axes[0], amp_x, label='x', cmap=CMAP_AMPLITUDE, vmin=minVal, vmax=maxVal)
    plot_mode_component(axes[1], amp_y, label='y', cmap=CMAP_AMPLITUDE, vmin=minVal, vmax=maxVal)
    plot_mode_component(axes[2], amp_z, label='z', cmap=CMAP_AMPLITUDE, vmin=minVal, vmax=maxVal)
    plot_colorbar(axes[3], label='Amplitude', cmap=CMAP_AMPLITUDE, vmin=0, vmax=maxVal, num_ticks=5)

    plot_mode_component(axes[4], phase_x, label='x', cmap=CMAP_PHASE, vmin=-np.pi, vmax=+np.pi)
    plot_mode_component(axes[5], phase_y, label='y', cmap=CMAP_PHASE, vmin=-np.pi, vmax=+np.pi)
    plot_mode_component(axes[6], phase_z, label='z', cmap=CMAP_PHASE, vmin=-np.pi, vmax=+np.pi)
    plot_colorbar(axes[7], label='Phase', cmap=CMAP_PHASE, vmin=-np.pi, vmax=np.pi, num_ticks=3,
                  ticklabels=['-3.14', '0', '-3.14'])

    fig.subplots_adjust(left=0.1, bottom=0.1, right=0.95, wspace=0.1)
    fig.suptitle('{:.2f} GHz'.format(freq), fontsize=20)
    fig.tight_layout()

    return fig


def make_figure_4(data_reader):
    """
    Create Fig. 4 in the paper.

    Returns a matplotlib figure with 2 x 3 panels displaying, respectively, the
    amplitude and phase of the x/y/z component of the eigenmode at 8.25 GHz.

    """
    approx_freq = 8.25

    # We use the spectrum of the y-component to find the peak
    timesteps = data_reader.get_timesteps(unit='s')
    freqs = get_fft_frequencies(timesteps, unit='GHz')
    m_y = data_reader.get_spatially_resolved_magnetisation('y')
    spectrum_y = get_spectrum_via_method_2(m_y)
    peak_freq = find_peak_frequency(freqs, spectrum_y, approx_freq=approx_freq)

    return plot_mode_at_frequency(data_reader, peak_freq)


def make_figure_5(data_reader):
    """
    Create Fig. 5 in the paper.

    Returns a matplotlib figure with 2 x 3 panels displaying, respectively, the
    amplitude and phase of the x/y/z component of the eigenmode at 11.25 GHz.

    """
    approx_freq = 11.25

    # We use the spectrum of the y-component to find the peak
    timesteps = data_reader.get_timesteps(unit='s')
    freqs = get_fft_frequencies(timesteps, unit='GHz')
    m_y = data_reader.get_spatially_resolved_magnetisation('y')
    spectrum_y = get_spectrum_via_method_2(m_y)
    peak_freq = find_peak_frequency(freqs, spectrum_y, approx_freq=approx_freq)

    return plot_mode_at_frequency(data_reader, peak_freq)
