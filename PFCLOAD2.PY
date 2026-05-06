
it.command("""
model mechanical timestep auto
model config cfd
element cfd ini density {}
element cfd ini visc {}
cfd porosity poly
"""
.format(fluid_density, fluid_viscosity))
element_volume = ca.volume()


it.command("""
cfd interval 10
;cfd porosity centroid

;cfd update
;cfd term gradp on

history interval 200
program call 'post.fis'
fish callback add @history_MASS -1 interval 250
fish callback add @history_CFD_INFO -1 interval 500

fish callback add @history_contactNUM event contact_create

;fish callback add @contactGroup -1 interval 1500

;fish history name '1' MASS
fish history name '11' MASS_residual

history fish id 2 fluid_time
fish history name '3' CFD_Velocity_1
fish history name '4' CFD_pressure_1
fish history name '5' CFD_Velocity_2
fish history name '6' CFD_pressure_2
fish history name '7' BallNumber
fish history name '9' meanf
;fish history name '10' WC_inbox1
;fish history name '12' WC_inbox2
@set_velocity


model orientation-tracking true

""")




dt =5e-5; #it.timestep() 
#saftCOF=25;
#it.command("[saftCOF={}]".format(saftCOF))

cfd_link = p2pLinkServer()
cfd_link.start()

for i in range(40):
  it.command("[i={}]".format(i))
  for j in range(200):
    it.command("[j={}]".format(j))
    #it.command("[dt={}]".format(dt))
    #it.command("@porosityDEC")
    #cfddt=it.fish.get('CFDDT')
    #it.command("solve age {}".format(it.mech_age()+dt))
    it.command("model solve mechanical time {}".format(dt))
    
    cfd_link.send_data(dt) # solve interval
    cfd_link.send_data(ca.porosity())
    cfd_link.send_data((ca.drag().T/element_volume).T/fluid_density)
    ca.set_pressure(cfd_link.read_data())
    ca.set_pressure_gradient(cfd_link.read_data())
    ca.set_velocity(cfd_link.read_data())
    
    
  savename='clump-1-1-13-'+'%d'%i
  it.command("""
  model save "{}"
  """.format(savename))

cfd_link.send_data(0.0) # solve interval
cfd_link.close()
  
del cfd_link
