import os

from postprocessing import DataReader

TOL = 0

# Get absolute path to the current directory (to avoid problems if
# this script is invoked from somewhere else).
this_directory = os.path.abspath(os.path.dirname(__file__))

REFERENCE_DATA_DIR_OOMMF = os.path.join(this_directory, '../../micromagnetic_simulation_data/reference_data/oommf/')
GENERATED_DATA_DIR_OOMMF = os.path.join(this_directory, '../../micromagnetic_simulation_data/recomputed_data/oommf/')

ref_data_reader = DataReader(REFERENCE_DATA_DIR_OOMMF, data_format='OOMMF')
gen_data_reader = DataReader(GENERATED_DATA_DIR_OOMMF, data_format='OOMMF')


def test__compare_average_magnetisation():
    """
    Check that maximum difference in average magnetisation between
    reference data and recomputed data is below threshold.

    """

    print("\nComparing average magnetisation between reference data and recomputed data.")

    TOL = 1e-14

    for component in ['x', 'y', 'z']:
        m_avg_ref = ref_data_reader.get_average_magnetisation(component)
        m_avg_gen = gen_data_reader.get_average_magnetisation(component)

        max_diff = abs(m_avg_ref - m_avg_gen).max()

        print("Maximum difference in {} component: {}".format(component, max_diff))
        assert max_diff < TOL


def test__compare_spatially_resolved_magnetisation():
    """
    Check that maximum difference in spatially resolved magnetisation
    between reference data and recomputed data is below threshold.

    """

    print("\nComparing spatially resolved magnetisation between reference data and recomputed data.")

    TOL = 1e-14

    for component in ['x', 'y', 'z']:
        m_ref = ref_data_reader.get_spatially_resolved_magnetisation(component)
        m_gen = gen_data_reader.get_spatially_resolved_magnetisation(component)

        max_diff = abs(m_ref - m_gen).max()

        print("Maximum difference in {} component: {}".format(component, max_diff))
        assert max_diff < TOL
