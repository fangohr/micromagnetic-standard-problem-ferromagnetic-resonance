import generic_tools
import os
import numpy as np
import matplotlib.pyplot as plt

txyzFileLoc = os.path.join(generic_tools.OOMMF_cached_data, "Dynamic_txyz.txt")

data = np.loadtxt(txyzFileLoc)

ts = data[:, 0]
my = data[:, 2]

dt = ts[1]-ts[0]

freq, ft_abs, phase = generic_tools.fft(my, dt)

# We plot the log of the power spectrum, for clarity
ft_power = ft_abs**2
length = len(freq)/2
log_ft_power = np.log10(ft_power[0:length])

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(2, 1, 1)
ax.plot(ts*1e9, my, label='Real')
ax.set_xlabel('Time (ns)')
ax.set_ylabel('Magnetisation in Y')
ax.set_xlim([0, 2.5])

ax = fig.add_subplot(2, 1, 2)
ax.plot(freq[0:length]*1e-9, ft_power[0:length], '-', label='Real')
ax.set_xlabel('Frequency (GHz)')
ax.set_ylabel('Spectral density')
ax.set_xlim([0.1, 20])
ax.set_ylim([1e-5, 1e-0])
ax.set_yscale('log')

plt.tight_layout()
fig.savefig('figure2.pdf')
