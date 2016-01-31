#!/bin/bash

# This script runs two OOMMF scripts: one for the "relaxation" stage
# and one for the "dynamic" stage of the simulation, respectively.
#
# This generates various data files containing the dynamics of the
# spatially averaged and spatially resolved magnetisation which are
# used in the visualiation and reproducibility tests.
#
# The output directory for the generated data can be provided as a
# command line argument. If it is not specified then the default value
# '../../../micromagnetic_simulation_data/generated_data/oommf/' is
# used.


#
# Raise error when a variable is not set, and exit as soon as any
# error occurs in the script.
#
set -o nounset
set -o errexit

OOMMF_SCRIPTS="01_relaxation_stage.mif 02_dynamic_stage.mif oommf_postprocessing.py"

#
# Check if the variable OOMMFTCL points to a valid OOMMF installation,
# otherwise raise an error.
#
if [ -z "${OOMMFTCL+1}" ]; then
    echo "Please set the environment variable OOMMFTCL to point"
    echo "to the file 'oommf.tcl' in your OOMMF installation."
    exit
fi

#
# Determine output directory (use first command line argument if
# provided, otherwise use default).
#
if [ "$#" -ge 1 ]; then
    OUTPUT_DIR=$1
else
    OUTPUT_DIR='../../../micromagnetic_simulation_data/generated_data/oommf/'
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
# Copy OOMMF scripts from source directory to a temporary directory
# where we will run the scripts to generate the data.
#
TMPDIR=$(mktemp -d)

for FILENAME in $OOMMF_SCRIPTS; do
    cp ./$FILENAME $TMPDIR/$FILENAME;
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
by the script 'src/micromagnetic_simulations/oommf/generate_data.sh' in the
repository [1]. It can safely be deleted if it is no longer needed.

[1] https://github.com/fangohr/micromagnetic-standard-problem-ferromagnetic-resonance
" > README.txt

#
# Run the relaxation stage.
#
tclsh $OOMMFTCL boxsi +fg 01_relaxation_stage.mif -exitondone 1
mv relax-*omf relax.omf

#
# Run the dynamic stage.
#
tclsh $OOMMFTCL boxsi +fg 02_dynamic_stage.mif -exitondone 1

#
# Extract the columns for time, mx, my, mz and store them in the file "dynamic_txyz.txt".
#
tclsh $OOMMFTCL odtcols < "dynamic.odt" 18 14 15 16 > "dynamic_txyz.txt"

#
# Extract the spatial magnetisation data (sampled on a 24 x 24 grid)
# and store it in three numpy arrays 'mxs.npy', 'mys.npy' and 'mzs.npy'
#
python oommf_postprocessing.py

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
echo "Successfully generated OOMMF data in directory: '$OUTPUT_DIR'"
echo
