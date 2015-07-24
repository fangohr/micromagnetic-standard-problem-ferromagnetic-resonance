import generic_tools as gnt
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib.colors as colors
from matplotlib import cm
import matplotlib._cm as _cm


def find_freq_index(f):
    data = np.loadtxt(txyzFileLoc)

    # nmag includes the t=0 data, which we discard:
    if simTool == 'nmag':
        data = data[1:, :]

    ts = data[:, 0]
    n = len(ts)
    dt = ts[1]-ts[0]

    freqs = np.fft.fftfreq(n, dt)

    df = freqs[1]-freqs[0]
    for i in range(n):
        if abs(f-freqs[i]) < 1e-5*df:
            return i

    raise Exception("Failed to find the index of given frequency!")


def rescale_cmap(cmap_name, low=0.0, high=1.0, plot=False):
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
    r[:, 1:] = r[:, 1:]*range+low
    g[:, 1:] = g[:, 1:]*range+low
    b[:, 1:] = b[:, 1:]*range+low
    _my_data = {'red':   tuple(map(tuple, r)),
                'green': tuple(map(tuple, g)),
                'blue':  tuple(map(tuple, b))
                }
    my_cmap = colors.LinearSegmentedColormap('my_hsv', _my_data, LUTSIZE)

    if plot:
        print 'plotting'
        plt.figure()
        plt.plot(r[:, 0], r[:, 1], 'r', g[:, 0], g[:, 1], 'g', b[:, 0],
                 b[:, 1], 'b', lw=3)
        plt.axis(ymin=-0.2,  ymax=1.2)
        plt.show()

    return my_cmap


# Different simulation tools produce slightly different peaks:
simTool = "OOMMF"
peaks = [8.25e9, 11.25e9]

txyzFileLoc = os.path.join(gnt.OOMMF_cached_data, 'Dynamic_txyz.txt')
nx = 24
ny = 24

mxs_ft_absLoc = os.path.join(gnt.OOMMF_cached_data, 'mxs_ft_abs.npy')
mys_ft_absLoc = os.path.join(gnt.OOMMF_cached_data, 'mys_ft_abs.npy')
mzs_ft_absLoc = os.path.join(gnt.OOMMF_cached_data, 'mzs_ft_abs.npy')

mxs_ft_phaseLoc = os.path.join(gnt.OOMMF_cached_data, 'mxs_ft_phase.npy')
mys_ft_phaseLoc = os.path.join(gnt.OOMMF_cached_data, 'mys_ft_phase.npy')
mzs_ft_phaseLoc = os.path.join(gnt.OOMMF_cached_data, 'mzs_ft_phase.npy')


mx_abs = np.load(mxs_ft_absLoc)
my_abs = np.load(mys_ft_absLoc)
mz_abs = np.load(mzs_ft_absLoc)

mx_phase = np.load(mxs_ft_phaseLoc)
my_phase = np.load(mys_ft_phaseLoc)
mz_phase = np.load(mzs_ft_phaseLoc)

for peak, figname in zip(peaks, ['figure4.pdf', 'figure5.pdf']):
    index = find_freq_index(peak)

    peakGHz = str(round((peak * 1e-9), 4))

    amp_x = mx_abs[:, index].reshape((ny, nx))
    amp_y = my_abs[:, index].reshape((ny, nx))
    amp_z = mz_abs[:, index].reshape((ny, nx))

    phase_x = mx_phase[:, index].reshape((ny, nx))
    phase_y = my_phase[:, index].reshape((ny, nx))
    phase_z = mz_phase[:, index].reshape((ny, nx))

    # Ensure that all three amplitude plots are on the same scale:
    max_X = np.amax(amp_x)
    max_Y = np.amax(amp_y)
    max_Z = np.amax(amp_z)
    maxVal = max([max_X, max_Y, max_Z])

    min_X = np.amin(amp_x)
    min_Y = np.amin(amp_y)
    min_Z = np.amin(amp_z)
    minVal = min([min_X, min_Y, min_Z])

    fig = plt.figure(figsize=(8, 6))
    gs = gridspec.GridSpec(2, 4, width_ratios=[4, 4, 4, 0.5],
                           height_ratios=[4, 4])
    plt.subplot(gs[0])
    ax = plt.gca()
    plt.imshow(amp_x, cmap=plt.cm.coolwarm, vmin=minVal, vmax=maxVal,
               origin='lower')
    plt.title('x')
    plt.xticks([])
    plt.yticks([])

    plt.subplot(gs[1])
    ax = plt.gca()
    plt.imshow(amp_y, cmap=plt.cm.coolwarm, vmin=minVal, vmax=maxVal,
               origin='lower')
    plt.title('y')
    plt.xticks([])
    plt.yticks([])

    plt.subplot(gs[2])
    ax = plt.gca()
    plt.imshow(amp_z, cmap=plt.cm.coolwarm, vmin=minVal, vmax=maxVal,
               origin='lower')
    plt.xticks([])
    plt.yticks([])
    plt.title('z')

    plt.subplot(gs[3])
    ax = plt.gca()
    norm = mpl.colors.Normalize(vmin=minVal, vmax=maxVal)
    cb1 = mpl.colorbar.ColorbarBase(ax, plt.cm.coolwarm, norm=norm,
                                    orientation='vertical',
                                    ticks=[0, maxVal*0.25, maxVal*0.5,
                                           maxVal*0.75, maxVal])
    cb1.set_label('Amplitude')

    my_hsv = rescale_cmap(cm.hsv, low=0.3, high=0.8, plot=False)

    plt.subplot(gs[4])
    ax = plt.gca()
    plt.imshow(phase_x, cmap=my_hsv, vmin=-np.pi, vmax=np.pi, origin='lower')
    plt.title('x')
    plt.xticks([])
    plt.yticks([])

    plt.subplot(gs[5])
    ax = plt.gca()
    plt.imshow(phase_y, cmap=my_hsv, vmin=-np.pi, vmax=np.pi, origin='lower')
    plt.title('y')
    plt.xticks([])
    plt.yticks([])

    plt.subplot(gs[6])
    ax = plt.gca()
    plt.imshow(phase_z, cmap=my_hsv, vmin=-np.pi, vmax=np.pi)
    plt.xticks([])
    plt.yticks([])
    plt.title('z')

    plt.subplot(gs[7])
    ax = plt.gca()

    norm = mpl.colors.Normalize(vmin=-np.pi, vmax=np.pi)
    cb1 = mpl.colorbar.ColorbarBase(ax, my_hsv, norm=norm,
                                    orientation='vertical',
                                    ticks=[-3.14, 0, 3.14])
    cb1.set_label('Phase')

    fig.subplots_adjust(left=0.1, bottom=0.1, right=0.95, wspace=0.1)
    fig.suptitle('%s GHz' % peakGHz, fontsize=20)
    fig.tight_layout()
    fig.savefig(figname)

    # Save the data for Fig. 8
    np.save('spatial_'+peakGHz+'.npy', amp_y)
