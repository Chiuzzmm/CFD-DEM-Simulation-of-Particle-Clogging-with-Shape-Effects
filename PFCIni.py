import numpy as np
from itasca.util import p2pLinkServer
from itasca import cfdarray as ca
import itasca as it
it.command("python-reset-state false")


#particle Inlets
#it.command("""
#program call 'Particle Inlets.dat'
#""")





# ---------------------------------------------
cfd_link = p2pLinkServer()
cfd_link.start()

nodes = cfd_link.read_data()
elements = cfd_link.read_data()
fluid_density = cfd_link.read_data()
fluid_viscosity = cfd_link.read_data()
print("density & viscosity")
print(fluid_density, fluid_viscosity)
nmin, nmax = np.amin(nodes, axis=0), np.amax(nodes, axis=0)
diag = np.linalg.norm(nmin-nmax)
dmin, dmax = nmin - 0.005*diag, nmax+0.005*diag
print("domain min and max")
print(dmin, dmax)

it.command("""
model new
MODEL LARGE-STRAIN on
ball delete
domain extent {} {} {} {} {} {}
domain condition periodic destroy destroy
""".format(-dmax[0]/50, dmax[0],
           dmin[1], dmax[1],
           dmin[2], dmax[2]))
# need to fix the c++ side, this is a work around for a platform type size issue.
elements = elements.astype(np.longlong)
ca.create_mesh(nodes, elements)

cfd_link.close()


it.command("model save 'create_mesh'")

it.command("""
program call 'gen_wall.dat'
""")
