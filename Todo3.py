import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

OOMMF_data = np.loadtxt("src/oommf_scripts/dynamic_txyz.txt")
Nmag_data = np.loadtxt("src/nmag_scripts/dynamic_txyz.txt")
time = OOMMF_data[:, 0]

fig, axes = plt.subplots(nrows=3, sharex=True)
ylabels = ["M_x", "M_y", "M_z"]

for i, (ax, ylabel) in enumerate(zip(axes, ylabels)):
    ax.plot(time, OOMMF_data[:, i+1], label="OOMMF")
    ax.plot(time, Nmag_data[:, i+1], label="Nmag")
    ax.set_ylabel(ylabel)

ax.set_xlabel("time")
plt.savefig('comparison.pdf')
