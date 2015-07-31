import nmag
from nmag import SI, every, at

mesh_name = 'meshes/mesh_24.nmesh.h5'
relax_name = 'relax'

# Material parameters
Ms = 8e5  # saturation magnetisation (A/m)
A = 13e-12  # exchange energy constant (J/m)
gamma = 2.210173e5  # gyromagnetic ratio (m/As)
alpha = 0.008  # Gilbert damping

# External magnetic field.
H = 80e3  # A/m
x_direction = 0.819152044289
y_direction = 0.573576436351
z_direction = 0

# Sampling parameters
dt = 5e-12  # time step (s)
T = 20e-9  # total simulation time (s)

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

# Load the initial magnetisation
sim.load_m_from_h5file(relax_name + ".h5")

# Set the applied magnetic field
sim.set_H_ext([x_direction, y_direction, z_direction], SI(H, 'A/m'))

# Set convergence parameters
sim.set_params(stopping_dm_dt=0.0)

# Save the information ever 5ps, and exit after 20ns.
sim.relax(save=[('fields', every('time', SI(dt, "s")))],
          do=[('exit', at('time', SI(T, "s")))])
