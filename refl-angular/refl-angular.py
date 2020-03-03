import meep as mp
import math
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt

resolution = 50                 # pixels/um

dpml = 1.0                      # PML thickness
sz = 10 + 2*dpml
cell_size = mp.Vector3(z=sz)
pml_layers = [mp.PML(dpml)]

wvl_min = 0.4                   # min wavelength
wvl_max = 0.8                   # max wavelength
fmin = 1/wvl_max                # min frequency
fmax = 1/wvl_min                # max frequency
fcen = 0.5*(fmin+fmax)          # center frequency
df = fmax-fmin                  # frequency width
nfreq = 50                      # number of frequency bins

def planar_reflectance(theta):    
    # rotation angle (in degrees) of source: CCW around Y axis, 0 degrees along +Z axis
    theta_r = math.radians(theta)

    # plane of incidence is XZ; rotate counter clockwise (CCW) about y-axis
    k = mp.Vector3(z=fmin).rotate(mp.Vector3(y=1), theta_r)
    
    # if normal incidence, force number of dimensions to be 1
    if theta_r == 0:
        dimensions = 1
    else:
        dimensions = 3
    
    sources = [mp.Source(mp.GaussianSource(fcen,fwidth=df), component=mp.Ex, center=mp.Vector3(z=-0.5*sz+dpml))]

    sim = mp.Simulation(cell_size=cell_size,
                        boundary_layers=pml_layers,
                        sources=sources,
                        k_point=k,
                        dimensions=dimensions,
                        resolution=resolution)

    refl_fr = mp.FluxRegion(center=mp.Vector3(z=-0.25*sz))
    refl = sim.add_flux(fcen, df, nfreq, refl_fr)
    
    sim.run(until_after_sources=mp.stop_when_fields_decayed(50, mp.Ex, mp.Vector3(z=-0.5*sz+dpml), 1e-9))

    empty_flux = mp.get_fluxes(refl)
    empty_data = sim.get_flux_data(refl)

    sim.reset_meep()

    # add a block with n=3.5 for the air-dielectric interface
    geometry = [mp.Block(mp.Vector3(mp.inf,mp.inf,0.5*sz), center=mp.Vector3(z=0.25*sz), material=mp.Medium(index=3.5))]

    sim = mp.Simulation(cell_size=cell_size,
                        geometry=geometry,
                        boundary_layers=pml_layers,
                        sources=sources,
                        k_point=k,
                        dimensions=dimensions,
                        resolution=resolution)

    refl = sim.add_flux(fcen, df, nfreq, refl_fr)
    sim.load_minus_flux_data(refl, empty_data)

    sim.run(until_after_sources=mp.stop_when_fields_decayed(50, mp.Ex, mp.Vector3(z=-0.5*sz+dpml), 1e-9))

    refl_flux = mp.get_fluxes(refl)
    freqs = mp.get_flux_freqs(refl)

    wvls = np.empty(nfreq)
    theta_out = np.empty(nfreq)
    R = np.empty(nfreq)
    for i in range(nfreq):
        wvls[i] = 1/freqs[i]
        theta_out[i] = math.degrees(math.asin(k.x/freqs[i]))
        R[i] = -refl_flux[i]/empty_flux[i]
        print("refl:, {}, {}, {}, {}".format(k.x,wvls[i],theta_out[i],R[i]))
        
    return k.x*np.ones(nfreq), wvls, theta_out, R



theta_in = np.arange(0,85,5)
wvl = np.empty(nfreq)
kxs = np.empty((nfreq,theta_in.size))
thetas = np.empty((nfreq,theta_in.size))
Rmeep = np.empty((nfreq,theta_in.size))

for j in range(theta_in.size):
  kxs[:,j], wvl, thetas[:,j], Rmeep[:,j] = planar_reflectance(theta_in[j])

# create a 2d matrix for the wavelength by repeating the column vector for each angle
wvls = np.transpose(np.matlib.repmat(wvl,theta_in.size,1))

plt.figure(dpi=200)
plt.pcolormesh(kxs, wvls, Rmeep, cmap='inferno', shading='gouraud', vmin=0, vmax=Rmeep.max())
plt.axis([kxs[0,0], kxs[0,-1], wvl_min, wvl_max])
plt.yticks([t for t in np.linspace(0.4,0.8,5)])
plt.xlabel(r"Bloch-periodic wavevector (k$_x$/2π)")
plt.ylabel("wavelength (μm)")
plt.title("reflectance (meep)")
cbar = plt.colorbar()
cbar.set_ticks([t for t in np.linspace(0,0.4,5)])
cbar.set_ticklabels(["{:.1f}".format(t) for t in np.linspace(0,0.4,5)])
plt.savefig('MEEP-Reflectance-Wavevector.png')

plt.figure(dpi=200)
plt.pcolormesh(thetas, wvls, Rmeep, cmap='inferno', shading='gouraud', vmin=0, vmax=Rmeep.max())
plt.axis([thetas.min(), thetas.max(), wvl_min, wvl_max])
plt.xticks([t for t in range(0,100,20)])
plt.yticks([t for t in np.linspace(0.4,0.8,5)])
plt.xlabel("angle of incident planewave (degrees)")
plt.ylabel("wavelength (μm)")
plt.title("reflectance (meep)")
cbar = plt.colorbar()
cbar.set_ticks([t for t in np.linspace(0,0.4,5)])
cbar.set_ticklabels(["{:.1f}".format(t) for t in np.linspace(0,0.4,5)])
plt.savefig('MEEP-Reflectance.png')

n1=1
n2=3.5

# compute angle of refracted planewave in medium n2
# for incident planewave in medium n1 at angle theta_in
theta_out = lambda theta_in: math.asin(n1*math.sin(theta_in)/n2)

# compute Fresnel reflectance for P-polarization in medium n2
# for incident planewave in medium n1 at angle theta_in
Rfresnel = lambda theta_in: math.fabs((n1*math.cos(theta_out(theta_in))-n2*math.cos(theta_in))/(n1*math.cos(theta_out(theta_in))+n2*math.cos(theta_in)))**2

Ranalytic = np.empty((nfreq, theta_in.size))
for m in range(wvl.size):
    for n in range(theta_in.size):
        Ranalytic[m,n] = Rfresnel(math.radians(thetas[m,n]))

plt.figure(dpi=200)
plt.pcolormesh(thetas, wvls, Ranalytic, cmap='inferno', shading='gouraud', vmin=0, vmax=Ranalytic.max())
plt.axis([thetas.min(), thetas.max(), wvl_min, wvl_max])
plt.xticks([t for t in range(0,100,20)])
plt.yticks([t for t in np.linspace(0.4,0.8,5)])
plt.xlabel("angle of incident planewave (degrees)")
plt.ylabel("wavelength (μm)")
plt.title("reflectance (analytic)")
cbar = plt.colorbar()
cbar.set_ticks([t for t in np.linspace(0,0.4,5)])
cbar.set_ticklabels(["{:.1f}".format(t) for t in np.linspace(0,0.4,5)])
plt.savefig('Analytic-Reflectance.png')
