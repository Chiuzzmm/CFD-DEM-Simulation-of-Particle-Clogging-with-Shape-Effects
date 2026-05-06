

it.command("""
;model mechanical timestep auto
model mechanical timestep scale 1e-2
model config cfd
element cfd ini density {}
element cfd ini visc {}
cfd porosity poly


;cfd buoyancy on
;cfd update
cfd interval 10

"""
.format(fluid_density, fluid_viscosity))

element_volume = ca.volume()

dt =2e-4; #it.timestep() 
saveTime = 1e3
saveIndex = 0


cfd_link = p2pLinkServer()
cfd_link.start()

for i in range(2000):
  #it.command("solve age {}".format(it.mech_age()+dt))
  it.command("model solve mechanical time {}".format(dt))

  it.command("[i={}]".format(i))
  cfd_link.send_data(dt) # solve interval
  cfd_link.send_data(ca.porosity())
  cfd_link.send_data((ca.drag().T/element_volume).T/fluid_density)
  ca.set_pressure(cfd_link.read_data())
  ca.set_pressure_gradient(cfd_link.read_data())
  ca.set_velocity(cfd_link.read_data())
  

  if i%saveTime==0:
    saveIndex+=1
    savename='save3load_re'+'%d'%saveIndex
    it.command("""
    model save "{}"
    """.format(savename))

cfd_link.send_data(0.0) # solve interval
cfd_link.close()
  
del cfd_link


