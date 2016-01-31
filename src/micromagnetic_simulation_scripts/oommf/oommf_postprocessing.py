import glob
import numpy as np

omf_files = sorted(glob.glob('dynamic*.omf'))

nx = 24
ny = 24

# Read magnetisation snapshots from all .omf files
# and store them in three arrays `mxs`, `mys`, `mzs`
# of shape NUM_TIMESTEPS x NUM_CELLS.
mxs = []
mys = []
mzs = []

for omf_file in omf_files:
    d = np.loadtxt(omf_file)
    mxs.append(d[:, 0])
    mys.append(d[:, 1])
    mzs.append(d[:, 2])

mxs = np.array(mxs)
mys = np.array(mys)
mzs = np.array(mzs)


# Compute the average of the magnetisation values in the
# top and bottom layer of the sample. Note that the way we
# compute this relies on the fact that OOMMF orders the
# magnetisation values such that the z-index is incremented
# last (see [1], section "Data block").
#
# [1] http://math.nist.gov/oommf/doc/userguide12a6/userguide/OVF_1.0_format.html

_, numMags = mxs.shape
numMagsPerLayer = numMags // 2

mxsTop = mxs[:, :numMagsPerLayer]
mysTop = mys[:, :numMagsPerLayer]
mzsTop = mzs[:, :numMagsPerLayer]
mxsBottom = mxs[:, numMagsPerLayer:]
mysBottom = mys[:, numMagsPerLayer:]
mzsBottom = mzs[:, numMagsPerLayer:]

mxs_sampled = 0.5 * (mxsTop + mxsBottom).reshape((-1, nx, ny))
mys_sampled = 0.5 * (mysTop + mysBottom).reshape((-1, nx, ny))
mzs_sampled = 0.5 * (mzsTop + mzsBottom).reshape((-1, nx, ny))

np.save('mxs.npy', mxs_sampled)
np.save('mys.npy', mys_sampled)
np.save('mzs.npy', mzs_sampled)
