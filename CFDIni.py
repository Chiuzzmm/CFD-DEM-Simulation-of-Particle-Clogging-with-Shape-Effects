from itasca import p2pLinkClient
import numpy as np
from pyDemFoam import pyDemIcoFoam

solver = pyDemIcoFoam()

pfc_link = p2pLinkClient()
pfc_link.connect("172.20.48.1")  # pfc_link.connect("127.0.0.1")
pfc_link.send_data(solver.nodes())
pfc_link.send_data(solver.elements())
pfc_link.send_data(solver.rho())
pfc_link.send_data(solver.mu())

pfc_link.close()

