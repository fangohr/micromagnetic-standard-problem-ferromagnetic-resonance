#!/bin/bash

# This script runs two Nmag scripts: one for the "relaxation" stage
# and one for the "dynamic" stage of the simulation, respectively.
#
# This generates various data files containing the dynamics of the
# spatially averaged and spatially resolved magnetisation which are
# used in the visualiation and reproducibility tests.
#
# The output directory for the generated data can be provided as a
# command line argument. If it is not specified then the default value
# '../../../micromagnetic_simulation_data/generated_data/nmag/' is
# used.


#
# Raise error when a variable is not set, and exit as soon as any
# error occurs in the script.
#
set -o nounset
set -o errexit

NMAG_SCRIPTS="01_relaxation_stage.py 02_dynamic_stage.py nmag_postprocessing.py meshes"

#
# Determine output directory (use first command line argument if
# provided, otherwise use default).
#
if [ "$#" -ge 1 ]; then
    OUTPUT_DIR=$1
else
    OUTPUT_DIR='../../../micromagnetic_simulation_data/generated_data/nmag/'
fi
echo "Data will be generated in output directory: '$OUTPUT_DIR'"

#
# Abort if output directory already exists to avoid overwriting existing data
#
if [ -d "$OUTPUT_DIR" ]; then
    echo "Warning: Output directory already exists: '$OUTPUT_DIR'"
    echo "         Please delete it or specify a different directory"
    echo "         by setting the environment variable OUTPUT_DIR."
    exit
fi

#
# Copy Nmag scripts from source directory to a temporary directory
# where we will run the scripts to generate the data.
#
TMPDIR=$(mktemp -d)

for FILENAME in $NMAG_SCRIPTS; do
    cp -r ./$FILENAME $TMPDIR/$FILENAME;
done

#
# Change into the temporary directory and run all subsequent commands there.
#
pushd $TMPDIR
echo "Working in temporary directory '$TMPDIR'."
echo "If something goes wrong you may want to delete this manually."

#
# Generate a README.txt file to inform the user how the data in this
# directory was created.
#
TIMESTAMP=$(date)

echo "The data in this directory was automatically generated on $TIMESTAMP
by the script 'src/micromagnetic_simulations/nmag/generate_data.sh' in the
repository [1]. It can safely be deleted if it is no longer needed.

[1] https://github.com/fangohr/micromagnetic-standard-problem-ferromagnetic-resonance
" > README.txt

#
# Run the relaxation stage.
#
nsim 01_relaxation_stage.py --clean

#
# Run the dynamic stage.
#
nsim 02_dynamic_stage.py --clean

#
# Extract the columns for time, mx, my, mz and store them in the file "dynamic_txyz.txt".
#
ncol 02_dynamic_stage time m_Py_0 m_Py_1 m_Py_2 > dynamic_txyz.txt

# Drop the first row for compatibility
tail -n +2 dynamic_txyz.txt > temp.txt
mv temp.txt dynamic_txyz.txt

#
# Extract the spatial magnetisation data (sampled on a 24 x 24 grid)
# and store it in three numpy arrays 'mxs.npy', 'mys.npy' and 'mzs.npy'
#
nmagprobe 02_dynamic_stage_dat.h5 --field=m_Py    --time=0,20e-9,4000\
        --space=0,120,24/0,120,24/5     --out=dynamic_spatYMag.nmagProbe
python nmag_postprocessing.py dynamic_spatYMag.nmagProbe

#
# Create output directory, copy the generated data there and remove
# temporay directory.
#
popd
mkdir -p $OUTPUT_DIR
cp $TMPDIR/dynamic_txyz.txt $OUTPUT_DIR
cp $TMPDIR/mxs.npy $OUTPUT_DIR
cp $TMPDIR/mys.npy $OUTPUT_DIR
cp $TMPDIR/mzs.npy $OUTPUT_DIR
rm -rf $TMPDIR

echo
echo "Successfully generated Nmag data in directory: '$OUTPUT_DIR'"
echo
