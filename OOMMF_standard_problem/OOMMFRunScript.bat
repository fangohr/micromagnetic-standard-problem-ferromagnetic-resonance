

rem run the relaxation stage
tclsh "C:\Program Files\oommf-1.2a5\oommf.tcl" boxsi +fg relax.mif -exitondone 1

rem save the relaxed data in an appropriate format
move relax-*.omf relax.omf


rem run the dynamic stage
tclsh "C:\Program Files\oommf-1.2a5\oommf.tcl" boxsi +fg dynamic.mif -exitondone 1

rem extract the txyz file 
tclsh "C:\Program Files\oommf-1.2a5\oommf.tcl" odtcols < "Dynamic.odt" 18 14 15 16 > "Dynamic_txyz.txt"

rem extract the spatial magnetisation data to 'mxs.npy', 'mys.npy' and 'mzs.npy'
python merge_omf.py

rem And tidy away all of the .omf files
del Dynamic-*.omf

rem Perform the fourier transform
python ..\..\ffts.py OOMMF
