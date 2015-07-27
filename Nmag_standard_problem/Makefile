.PHONY: figure_clean
.PHONY: data_clean

transform_data = mxs_ft_abs.npy mys_ft_abs.npy mzs_ft_abs.npy\
	             mxs_ft_phase.npy mys_ft_phase.npy mzs_ft_phase.npy\

figures: ${transform_data}
	python ../micromagnetic_standard_problem_FMR.py --figures --software Nmag

${transform_data}:
	python ../micromagnetic_standard_problem_FMR.py --transform --software Nmag

figure_clean:
	rm -f *pdf
	rm -f m*_*npy

data: Dynamic_dat.h5
	ncol Dynamic time m_Py_0 m_Py_1 m_Py_2 > Dynamic_txyz.txt
	# Drop the first row for compatibility
	tail -n +2 Dynamic_txyz.txt > temp.txt
	mv temp.txt Dynamic_txyz.txt

	nmagprobe  Dynamic_dat.h5 --field=m_Py 	--time=0,20e-9,4000\
	       	--space=0,120,24/0,120,24/5 	--out=Dynamic_spatYMag.nmagProbe
	python convertNmagProbe_2.py Dynamic_spatYMag.nmagProbe

dynamic Dynamic_dat.h5 Dynamic_dat.ndt: Dynamic.py Relax_dat.h5
	nsim Dynamic.py --clean

relax Relax_dat.h5: Relax.py
	nsim Relax.py --clean

data_clean:
	rm -f *.h5
	rm -f *log
	rm -f Dynamic_spatYMag.nmagProbe


