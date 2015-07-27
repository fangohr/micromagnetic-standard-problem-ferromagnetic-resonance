.PHONY: clean

figures = figure2_Nmag.pdf figure3_Nmag.pdf figure4_Nmag.pdf figure5_Nmag.pdf 

${figures}: transformed_data
	python generate_figures.py

transformed_data: Dynamic_spatYMag.nmagProbe
	python convertNmagProbe_2.py Dynamic_spatYMag.nmagProbe
	python transform_data.py

Dynamic_spatYMag.nmagProbe: Dynamic_dat.h5
	nmagprobe  Dynamic_dat.h5 --field=m_Py 	--time=0,20e-9,4000 --space=0,120,24/0,120,24/5 	--out=Dynamic_spatYMag.nmagProbe

Dynamic_dat.h5: Dynamic.py Relax_dat.h5
	nsim Dynamic.py --clean
	ncol Dynamic time m_Py_0 m_Py_1 m_Py_2 >Dynamic_txyz.txt
	# Drop the first row for compatibility
	echo "$(tail -n +2 Dynamic_txyz.txt") > Dynamic_txyz.txt

Relax_dat.h5: Relax.py
	nsim Relax.py --clean
	mv relax-*omf relax.omf

clean:
	rm -f Dynamic_txyz.txt
	rm -f *npy
	rm -f *pdf
	rm *.omf


