import meep as mp
import numpy as np
import math

cell_size = mp.Vector3(2,2,2)

# A hexagon is defined as a prism with six vertices centered on the origin
vertices = [mp.Vector3(-1,0),
            mp.Vector3(-0.5,math.sqrt(3)/2),
            mp.Vector3(0.5,math.sqrt(3)/2),
            mp.Vector3(1,0),
            mp.Vector3(0.5,-math.sqrt(3)/2),
            mp.Vector3(-0.5,-math.sqrt(3)/2)]


geometry=[#mp.Block(center=mp.Vector3(0,0,0), size=cell_size, material=mp.air),
	  mp.Prism(vertices, height=1.9, material=mp.metal, center=mp.Vector3(0,0,0))]


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
mlab.savefig('Prism3D.pdf')
