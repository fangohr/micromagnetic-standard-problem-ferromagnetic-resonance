#Run the relaxation stage creating a "relaxed configuration"
nsim Relax.py --clean

#Run the dynamic stage over 20ns 
nsim Dynamic.py --clean

#Extract the time and magnetizations of the averaged data
ncol Dynamic time m_Py_0 m_Py_1 m_Py_2 >Dynamic_txyz.txt

#Probes the spatial field fourier transforming, this will results in an amplitude, as a 
# function of frequency and space.

nmagprobe  Dynamic_dat.h5 --field=m_Py 	--time=0,20e-9,4000 --space=0,120,24/0,120,24/5 	--out=Dynamic_spatYMag.nmagProbe

#Then we extract the data from this:
python convertNmagProbe_2.py Dynamic_spatYMag.nmagProbe

#Perform the spatial FT:
python ../../ffts.py nmag



