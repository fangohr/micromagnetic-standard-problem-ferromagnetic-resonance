import os
from micromagnetic_standard_problem_FMR import spatial_fft

for direction in ["x", "y", "z"]:
    source = 'm{}s.npy'.format(direction)
    target = 'm{}s_ft_abs.npy'.format(direction)

    if not os.path.isfile(source):
        raise IOError(("Source file {} does not exist try running the "
                      "Makefile").format(source))
    if not os.path.isfile(target):
        spatial_fft(source)
