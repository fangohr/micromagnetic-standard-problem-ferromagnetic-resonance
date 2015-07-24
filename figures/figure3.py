import generic_tools
import os
import numpy as np
import matplotlib.pyplot as plt

mys_ft_absLoc = os.path.join(generic_tools.OOMMF_cached_data, 'mys_ft_abs.npy')
txyzFileLoc = os.path.join(generic_tools.OOMMF_cached_data, 'Dynamic_txyz.txt')

data = np.loadtxt(txyzFileLoc)

ts = data[:, 0]
my = data[:, 2]

dt = ts[1]-ts[0]

freq, ft_abs, phase = generic_tools.fft(my,  dt)
ft_power = ft_abs**2

length = len(freq)/2

mys = np.load(mys_ft_absLoc)
averaged = np.average(mys**2, axis=0)

fig = plt.figure(figsize=(7, 5.5))
ax = fig.add_subplot(1, 1, 1)
ax.plot(freq[0:length]*1e-9, ft_power[0:length], label='Spatially Resolved')
ax.plot(freq[0:length]*1e-9, averaged[0:length], label='Spatially Averaged')
ax.set_xlabel('Frequency (GHz)')
ax.set_ylabel('Spectral density')
ax.set_xlim([0.2, 20])
ax.set_ylim([1e-5, 1e0])
ax.set_yscale('log')
ax.legend()
ax.grid()

fig.savefig('figure3.pdf')
