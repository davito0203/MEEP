import meep as mp
import numpy as np
import math

cell_size = mp.Vector3(2,2,2)


geometry=[#mp.Block(center=mp.Vector3(0,0,0), size=cell_size, material=mp.air),
          mp.Sphere(center=mp.Vector3(0,0,0), radius=1, material=mp.metal)]


sim = mp.Simulation(resolution=50, cell_size=cell_size, geometry=geometry)

sim.init_sim()

eps_data = sim.get_epsilon()
#eps_data = sim.get_array()


#sim.plot3D(eps_data)

#from mayavi import mlab
#s = mlab.contour3d()
#mlab.show()
#mlab.savefig(filename='test2.png')

from mayavi import mlab
s = mlab.contour3d(eps_data, colormap="hsv")
#mlab.show()
mlab.savefig('Sphere3D.pdf')
