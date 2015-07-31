import glob
import numpy as np

omf_files = glob.glob('dynamic*.omf')
omf_files.sort()

mxs = []
mys = []
mzs = []
for omf_file in omf_files:
    d = np.loadtxt(omf_file)
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

np.savez('ms.npz', mxs=mxs, mys=mys, mzs=mzs)
