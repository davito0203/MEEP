# -*- coding: utf-8 -*-

# From the Meep tutorial: plotting permittivity and fields of a straight waveguide
from __future__ import division

import meep as mp
import numpy as np
import matplotlib.pyplot as plt

cell = mp.Vector3(16,8,0)

geometry = [mp.Block(mp.Vector3(mp.inf,1,mp.inf),
                     center=mp.Vector3(),
                     material=mp.Medium(epsilon=12))]

sources = [mp.Source(mp.ContinuousSource(frequency=0.15),
                     component=mp.Ez,
                     center=mp.Vector3(-7,0))]

pml_layers = [mp.PML(1.0)]

resolution = 10

sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)

sim.run(until=200)

eps_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)
plt.figure(dpi=100)
sim.plot2D()
#plt.show()
plt.savefig('PLM-Box.png')

ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
plt.figure(dpi=100)
sim.plot2D(fields=mp.Ez)
#plt.show()
plt.savefig('EzComponent.png')

#sim.reset_meep()
f = plt.figure(dpi=100)
Animate = mp.Animate2D(sim, fields=mp.Ez, f=f, realtime=False, normalize=True)
plt.close()



sim.run(mp.at_every(1,Animate),until=100)
plt.close()



filename = "straight_waveguide.mp4"
Animate.to_mp4(20,filename)

from IPython.display import Video
Video(filename)
