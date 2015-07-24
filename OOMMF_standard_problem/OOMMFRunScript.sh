#OOMMFTCL=/usr/local/bin/oommf-1.2a5/oommf.tcl

#OOMMFTCL=/home/fangohr/oommf/oommf.tcl

#OOMMFTCL=C:\Program Files\oommf-1.2a5

#The right line to run this on aleph0.kk.soton.ac.uk in July 2013
#OOMMFTCL=/usr/local/software/oommf/oommf/oommf.tcl

#The right line to run this on the MBE group's simulation computer, July 2013
#OOMMFTCL=/usr/local/bin/oommf-1.2a5/oommf.tcl

if [ ! -e relax.omf ]; then

    #run the relaxation stage
    tclsh $OOMMFTCL boxsi +fg relax.mif -exitondone 1

    #save the relaxed data in an appropiate format
    mv relax-*.omf relax.omf
fi;


if [ ! -e "Dynamic_txyz.txt" ]; then
    
    if [ -e "Dynamic.odt" ]; then
        rm Dynamic.odt
    fi;

    #run the dunamic stage
    tclsh $OOMMFTCL boxsi +fg dynamic.mif -exitondone 1

    #extract the txyz file 
    tclsh $OOMMFTCL odtcols < "Dynamic.odt" 18 14 15 16 > "Dynamic_txyz.txt"
    
    #extract the spatial magnetisation data to 'mxs.npy', 'mys.npy' and 'mzs.npy'
    python merge_omf.py

    #And tidy away all of the .omf files
    rm Dynamic-*.omf

fi;

python ../../ffts.py  OOMMF
