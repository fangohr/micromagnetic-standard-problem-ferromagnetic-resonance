import glob
import numpy as np

files = glob.glob('Dynamic*.omf')
files.sort()

mxs = []
mys = []
mzs = []


for f in files:
    d = np.loadtxt(f)
    mxs.append(d[:, 0])
    mys.append(d[:, 1])
    mzs.append(d[:, 2])

mxs = np.array(mxs, dtype=np.float16)
mys = np.array(mys, dtype=np.float16)
mzs = np.array(mzs, dtype=np.float16)

numMags = mxs.shape[1] / 2.

mxs = 0.5 * (mxs[:, :numMags] + mxs[:, numMags:])
mys = 0.5 * (mys[:, :numMags] + mys[:, numMags:])
mzs = 0.5 * (mzs[:, :numMags] + mzs[:, numMags:])

np.save('mxs.npy', mxs)
np.save('mys.npy', mys)
np.save('mzs.npy', mzs)
