import meep as mp
import numpy as np
import math

cell_size = mp.Vector3(2,2,2)

geometry = [#mp.Prism(vertices, height=2.0, material=mp.Medium(index=3.5))]
            mp.Cone(radius=0.1, radius2=1.0, height=2.0, material=mp.metal, center=mp.Vector3(0,0,0))]

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
mlab.show()
#mlab.savefig('Cone3D.pdf')
