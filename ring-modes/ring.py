import meep as mp
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Video

n = 3.4                 # index of waveguide
w = 1                   # width of waveguide
r = 1                   # inner radius of ring
pad = 4                 # padding between waveguide and edge of PML
dpml = 2                # thickness of PML
sxy = 2*(r+w+pad+dpml)  # cell size

c1 = mp.Cylinder(radius=r+w, material=mp.Medium(index=n))
c2 = mp.Cylinder(radius=r)


fcen = 0.15              # pulse center frequency
df = 0.1                 # pulse frequency width
src = mp.Source(mp.GaussianSource(fcen, fwidth=df), mp.Ez, mp.Vector3(r+0.1))



sim = mp.Simulation(cell_size=mp.Vector3(sxy, sxy),
                    geometry=[c1, c2],
                    sources=[src],
                    resolution=10,                    
                    boundary_layers=[mp.PML(dpml)])
plt.figure(dpi=150)
sim.plot2D()
plt.savefig('structureBox.png')

sim.run(mp.at_beginning(mp.output_epsilon),
        mp.after_sources(mp.Harminv(mp.Ez, mp.Vector3(r+0.1), fcen, df)),
        until_after_sources=300)

sim.reset_meep()
fcen=0.118
df = 0.1
sim.sources = [mp.Source(mp.GaussianSource(fcen, fwidth=df), mp.Ez, mp.Vector3(r+0.1))]

# Start the simulation and get into steady state
sim.run(until=600) 

# Prepare the animator and record the steady state response
f = plt.figure(dpi=150)
Animate = mp.Animate2D(sim, fields=mp.Ez, f=f, realtime=False, normalize=True)
sim.run(mp.at_every(0.5,Animate),until=25)

# Close the animator's working frame
plt.close()

# Process the animation and view it
filename = "ring_simple.mp4"
Animate.to_mp4(5,filename)
Video(filename)

sim.reset_meep()
fcen=0.147
df = 0.1
sim.sources = [mp.Source(mp.GaussianSource(fcen, fwidth=df), mp.Ez, mp.Vector3(r+0.1))]
sim.init_sim()

# Start the simulation and get into steady state
sim.run(until=500) 

# Prepare the animator and record the steady state response
f = plt.figure(dpi=150)
Animate = mp.Animate2D(sim, fields=mp.Ez, f=f, realtime=False, normalize=True)
sim.run(mp.at_every(0.5,Animate),until=25)

# Close the animator's working frame
plt.close()

# Process the animation and view it
filename = "ring_mid.mp4"
Animate.to_mp4(5,filename)
Video(filename)

sim.reset_meep()
fcen=0.175
df = 0.1
sim.sources = [mp.Source(mp.GaussianSource(fcen, fwidth=df), mp.Ez, mp.Vector3(r+0.1))]

# Start the simulation and get into steady state
sim.run(until=500) 

# Prepare the animator and record the steady state response
f = plt.figure(dpi=150)
Animate = mp.Animate2D(sim, fields=mp.Ez, f=f, realtime=False, normalize=True)
sim.run(mp.at_every(0.5,Animate),until=25)

# Close the animator's working frame
plt.close()

# Process the animation and view it
filename = "ring_large.mp4"
Animate.to_mp4(5,filename)
Video(filename)
