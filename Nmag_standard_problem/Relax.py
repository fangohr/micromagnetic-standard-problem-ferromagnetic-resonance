import math
import nmag
from nmag import SI,every,at,si
from nsim.si_units.si import degrees_per_ns
import sys
import getopt


mSat = 0.8e6
exchange_Strength = 13e-12
meshName = 'mesh_24' + '.nmesh.h5'

xField = 0.813405448449
yField = 0.581697151818
h_Strength=80e3 #A/m

stoppingTime = 5000

simOutputName = 'Relax'



#Define magnetic material: PermAlloy
Py = nmag.MagMaterial(name="Py",                       Ms=SI(mSat,'A/m'),                      exchange_coupling = SI(exchange_Strength,"J/m"),                       llg_gamma_G = SI(2.210173e5, 'm/A s'),                        llg_damping = 1.0)

#Create the simulation object
sim = nmag.Simulation()

#Load the mesh
sim.load_mesh(meshName,[("Permalloy",Py)],unit_length = SI(1e-9,"m"))

# Set initial magnetization
sim.set_m([0.0,0.0,1.0])

#And set the external field
sim.set_H_ext([xField,yField,0],SI(h_Strength,'A/m'))

# Set convergence parameters
sim.set_params(stopping_dm_dt = 0)

#Save all the information out at the start and at the end
sim.relax(save=[('fields',at('stage_end'))],\
    do= [('exit',at('time',SI(stoppingTime * 1e-12,"s")))])

#Finally, save the system state for the dynamic stage to run from
sim.save_restart_file(simOutputName + '.h5')