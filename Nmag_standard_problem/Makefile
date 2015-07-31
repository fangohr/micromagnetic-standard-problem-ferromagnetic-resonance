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
	ncol dynamic time m_Py_0 m_Py_1 m_Py_2 > dynamic_txyz.txt
	# Drop the first row for compatibility
	tail -n +2 dynamic_txyz.txt > temp.txt
	mv temp.txt dynamic_txyz.txt

	nmagprobe  dynamic_dat.h5 --field=m_Py 	--time=0,20e-9,4000\
	       	--space=0,120,24/0,120,24/5 	--out=dynamic_spatYMag.nmagProbe
	python convertNmagProbe_2.py dynamic_spatYMag.nmagProbe

dynamic Dynamic_dat.h5 Dynamic_dat.ndt: dynamic_stage.py Relax_dat.h5
	nsim dynamic_stage.py --clean

relax Relax_dat.h5: Relax.py
	nsim relaxation_stage.py --clean

data_clean:
	rm -f *.h5
	rm -f *log
	rm -f dynamic_spatYMag.nmagProbe


