import nmag
from nmag import SI, at

mesh_name = 'meshes/mesh_555.nmesh.h5'
sim_output_name = 'relax'

# Material parameters
Ms = 8e5  # saturation magnetisation (A/m)
A = 13e-12  # exchange energy constant (J/m)
gamma = 2.210173e5  # gyromagnetic ratio (m/As)
alpha = 1  # Gilbert damping

# External magnetic field.
H = 80e3  # A/m
x_direction = 0.813405448449
y_direction = 0.581697151818
z_direction = 0.0

# Total simulation time
T = 5e-9

# Define magnetic material: PermAlloy
Py = nmag.MagMaterial(name="Py",
                      Ms=SI(Ms, 'A/m'),
                      exchange_coupling=SI(A, "J/m"),
                      llg_gamma_G=SI(gamma, 'm/A s'),
                      llg_damping=alpha)

# Create the simulation object
sim = nmag.Simulation()

# Load the mesh
sim.load_mesh(mesh_name, [("Permalloy", Py)], unit_length=SI(1e-9, "m"))

# Set initial magnetization state in positive z direction
sim.set_m([0.0, 0.0, 1.0])

# And set the external field
sim.set_H_ext([x_direction, y_direction, z_direction], SI(H, 'A/m'))

# Set convergence parameters
sim.set_params(stopping_dm_dt=0)

# Save all the information out at the start and at the end
sim.relax(save=[('fields', at('stage_end'))],
          do=[('exit', at('time', SI(T, "s")))])

# Finally, save the system state for the dynamic stage to run from
sim.save_restart_file(sim_output_name + '.h5')
