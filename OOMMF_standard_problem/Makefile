.PHONY: figure_clean
.PHONY: data_clean

transform_data = mxs_ft_abs.npy mys_ft_abs.npy mzs_ft_abs.npy\
	             mxs_ft_phase.npy mys_ft_phase.npy mzs_ft_phase.npy\

figures: ${transform_data}
	python ../micromagnetic_standard_problem_FMR.py --figures --software OOMMF

${transform_data}:
	python ../micromagnetic_standard_problem_FMR.py --transform --software OOMMF

figure_clean:
	rm -f *pdf
	rm -f m*_*npy

data: dynamic.mif relax.omf
	rm -f Dynamic.odt

	tclsh $(OOMMFTCL) boxsi +fg dynamic.mif -exitondone 1

	#extract the txyz file
	tclsh $(OOMMFTCL) odtcols < "Dynamic.odt" 18 14 15 16 > "Dynamic_txyz.txt"

	#extract the spatial magnetisation data to 'mxs.npy', 'mys.npy' and 'mzs.npy'
	python merge_omf.py

	#And tidy away all of the .omf files
	rm Dynamic-*.omf

relax.omf: relax.mif
	tclsh $(OOMMFTCL) boxsi +fg relax.mif -exitondone 1
	mv relax-*omf relax.omf

data_clean:
	rm -f *.omf
	rm -f *.odt

clean_all:
	rm -f *.omf
	rm -f *.odt
	rm -f *.pdf
	rm -f *.npy
	rm -f *.txt
