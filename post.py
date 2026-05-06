import itasca as it
it.command("python-reset-state false")
import numpy as np


number=16
size=29+1
data = np.empty([size,2])#, dtype = float) 
print (data)

for i in range(0,size):
  filename='test-'+str(number)+'-4-'+str(i)
  print(filename)
  comandstr='model restore \''+filename+'\''
  it.command(comandstr)
  
  it.command("""
  def contactGroup
  f=0
  loop foreach cp contact.list
    
    fx=contact.force.global.x(cp)
    fy=contact.force.global.y(cp)
    fz=contact.force.global.z(cp)
    f2=fx^2+fy^2+fz^2
    contact.extra(cp,1)=f2
    f+=f2
  endloop
  meanf=f/contact.num
  
  loop foreach cp contact.list('ball-ball')
    if contact.extra(cp,1)>meanf
      contact.group(cp,1) = 'ok'
      b1=contact.end1(cp)
      ball.group(b1,1)='ok'
      b1=contact.end2(cp)
      ball.group(b1,1)='ok'
    endif
  endloop
  end
  
  @contactGroup
  """)
  
  it.command('[a=fluid_time]')
  data[i,0]=it.fish.get('a')
  data[i,1]=it.fish.get('meanf')
  
  it.command("[filename='{}']".format(filename))
  it.command("""
  plot 'Plot01' export bitmap dpi 300 filename @filename size 4096 3032
  """)
  
filename=str(number)+'-1contactMeanF.txt'
np.savetxt(filename,data)