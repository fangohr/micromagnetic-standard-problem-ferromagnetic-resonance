import micromagnetic_standard_problem_FMR as MSP

MSP.figure2("./Dynamic_txyz.txt", "Nmag")

MSP.figure3("./Dynamic_txyz.txt", "mys_ft_abs.npy", "Nmag")

MSP.figure4_and_5("./Dynamic_txyz.txt",
            "mxs_ft_abs.npy", "mys_ft_abs.npy", "mzs_ft_abs.npy",
            "mxs_ft_phase.npy", "mys_ft_phase.npy", "mzs_ft_phase.npy",
            "Nmag")
