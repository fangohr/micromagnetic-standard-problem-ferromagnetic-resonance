import math
import nmag
from nmag import SI,every,at,si
#from nsim.si_units.si import degrees_per_ns
import sys 

h_Strength=80e3 #A/m


alpha = 0.008
meshName = 'mesh_24' + '.nmesh.h5'
relaxName = 'Relax'

xField = 0.819152044289
yField = 0.573576436351

#Define magnetic material: PermAlloy
Py = nmag.MagMaterial(name="Py",                       Ms=SI(0.8e6,'A/m'),                      exchange_coupling = SI(13e-12,"J/m"),                       llg_gamma_G = SI(2.210173e5, 'm/A s'),                       llg_damping = alpha)


#Create the simulation object
sim = nmag.Simulation()

#Load the mesh
sim.load_mesh(meshName, [("Permalloy",Py)] , unit_length = SI(1e-9, "m"))

#Load the initial magnetisation
sim.load_m_from_h5file(relaxName + ".h5")

# Set the applied magnetic field
sim.set_H_ext([xField,yField,0], SI(h_Strength, 'A/m'))

# Set convergence parameters
sim.set_params(stopping_dm_dt = 0.0)

#Save the information ever 5ps, and exit after 20ns. Note that we will never
#meet the convergence parameter that we have set, so we hard exit
sim.relax(save=[('fields', every('time', SI(5.0e-12,"s")))],           do= [('exit',at('time',SI(20000*1e-12,"s")))]) 