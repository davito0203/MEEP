# -*- coding: utf-8 -*-

# From the Meep tutorial: plotting permittivity and fields of a bent waveguide
from __future__ import division

import meep as mp
from matplotlib import pyplot as plt
import numpy as np
from IPython.display import Video

cell = mp.Vector3(16,16,0)
geometry = [mp.Block(mp.Vector3(12,1,mp.inf),
                     center=mp.Vector3(-2.5,-3.5),
                     material=mp.Medium(epsilon=12)),
            mp.Block(mp.Vector3(1,12,mp.inf),
                     center=mp.Vector3(3.5,2),
                     material=mp.Medium(epsilon=12))]
pml_layers = [mp.PML(1.0)]
resolution = 10

sources = [mp.Source(mp.ContinuousSource(wavelength=2*(11**0.5), width=20),
                     component=mp.Ez,
                     center=mp.Vector3(-7,-3.5),
                     size=mp.Vector3(0,1))]

sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)

f = plt.figure(dpi=150)
sim.plot2D(ax = f.gca())
# plt.show()
plt.savefig('2Dstructure.png')


f = plt.figure(dpi=150)
Animate = mp.Animate2D(sim, fields=mp.Ez, f=f, realtime=False, normalize=True)
sim.run(mp.at_every(0.5,Animate),until=100)
plt.close()

filename = "mbent_waveguide.mp4"
fps = 10
Animate.to_mp4(fps,filename)
Video(filename)

#sim.reset_meep()
#cell = mp.Vector3(16,40,0)
#geometry = [mp.Block(mp.Vector3(12,1,mp.inf),
#                     center=mp.Vector3(-2.5,-3.5),
#                     material=mp.Medium(epsilon=12)),
#            mp.Block(mp.Vector3(1,42,mp.inf),
#                     center=mp.Vector3(3.5,17),
#                     material=mp.Medium(epsilon=12))]
#sim.cell_size = cell
#sim.geometry = geometry
#sim.geometry_center = mp.Vector3(0,12,0)

#sim.run(until=400)

#plt.figure(dpi=150)
#sim.plot2D(fields=mp.Ez)
# plt.show()
#plt.savefig('Large2Dstructure.png')

vals = []

def get_slice(sim):
    vals.append(sim.get_array(center=mp.Vector3(0,-3.5), size=mp.Vector3(16,0), component=mp.Ez))

sim.reset_meep()
sim.run(mp.at_beginning(mp.output_epsilon),
        mp.at_every(0.6, get_slice),
        until=200)

plt.figure(dpi=150)
plt.imshow(vals, interpolation='spline36', cmap='RdBu')
plt.axis('off')
#plt.show()
plt.savefig('Slice.png')

sim.run(mp.at_beginning(mp.output_epsilon),
        mp.to_appended("ez", mp.at_every(0.6, mp.output_efield_z)),
        until=200)


