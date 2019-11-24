import meep as mp
import numpy as np
from matplotlib import pyplot as plt

sz = 100              # size of cell in z direction
fcen = 1 / 3.0        # center frequency of source
df = fcen / 20.0      # frequency width of source
amp = 1               # amplitude of source
k = 10**-5            # Kerr susceptibility
dpml = 1.0            # PML thickness

dimensions = 1
cell = mp.Vector3(0, 0, sz)
pml_layers = mp.PML(dpml)
resolution = 20

default_material = mp.Medium(index=1, chi3=k)

sources = mp.Source(mp.GaussianSource(fcen, fwidth=df), component=mp.Ex,
                    center=mp.Vector3(0, 0, -0.5*sz + dpml), amplitude=amp)

nfreq = 400
fmin = fcen / 2.0
fmax = fcen * 4

sim = mp.Simulation(cell_size=cell,
                    geometry=[],
                    sources=[sources],
                    boundary_layers=[pml_layers],
                    default_material=default_material,
                    resolution=resolution,
                    dimensions=dimensions)

trans = sim.add_flux(0.5 * (fmin + fmax), fmax - fmin, nfreq,
                     mp.FluxRegion(mp.Vector3(0, 0, 0.5*sz - dpml - 0.5)))



sim.run(until_after_sources=mp.stop_when_fields_decayed(
        50, mp.Ex, mp.Vector3(0, 0, 0.5*sz - dpml - 0.5), 1e-6))

freqs = mp.get_flux_freqs(trans)
spectra = mp.get_fluxes(trans)

plt.figure(dpi=150)
plt.semilogy(freqs,spectra)
plt.grid(True)
plt.xlabel('Frequency')
plt.ylabel('Transmitted Power (a.u.)')
#plt.show()
plt.savefig('freq10.png')

def run_chi3(k_pow,amp=1):
    k = 10**k_pow 
    default_material = mp.Medium(index=1, chi3=k)
    
    sources = mp.Source(mp.GaussianSource(fcen, fwidth=df), component=mp.Ex,
                    center=mp.Vector3(0, 0, -0.5*sz + dpml), amplitude=amp)
    
    sim = mp.Simulation(cell_size=cell,
                    geometry=[],
                    sources=[sources],
                    boundary_layers=[pml_layers],
                    default_material=default_material,
                    resolution=resolution,
                    dimensions=dimensions)

    trans = sim.add_flux(0.5 * (fmin + fmax), fmax - fmin, nfreq,
                     mp.FluxRegion(mp.Vector3(0, 0, 0.5*sz - dpml - 0.5)))
    
    # Single frequency point at omega
    trans1 = sim.add_flux(fcen, 0, 1,
                      mp.FluxRegion(mp.Vector3(0, 0, 0.5*sz - dpml - 0.5)))

    # Singel frequency point at 3omega
    trans3 = sim.add_flux(3 * fcen, 0, 1,
                      mp.FluxRegion(mp.Vector3(0, 0, 0.5*sz - dpml - 0.5)))
    
    sim.run(until_after_sources=mp.stop_when_fields_decayed(
        50, mp.Ex, mp.Vector3(0, 0, 0.5*sz - dpml - 0.5), 1e-6))
    
    omega_flux = mp.get_fluxes(trans1)
    omega3_flux = mp.get_fluxes(trans3)
    freqs = mp.get_flux_freqs(trans)
    spectra = mp.get_fluxes(trans)
    
    return freqs, spectra, omega_flux, omega3_flux
k_pow = [-3,-2,-1,0]
freqs = []
spectra = []
for k_iter in k_pow:
    freqs_iter, spectra_iter, omega_flux, omega3_flux = run_chi3(k_iter)
    spectra.append(spectra_iter)
    freqs = freqs_iter # Each iteration will simulate over the same frequencies, so just remember the last set.



plt.figure(dpi=150)
plt.semilogy(freqs,np.array(spectra).T)
plt.grid(True)
plt.xlabel('Frequency')
plt.ylabel('Transmitted Power (a.u.)')
plt.legend(["$\chi^{{(3)}} = 10^{{{}}}$".format(i) for i in k_pow])
plt.show()



_, _, omega_flux_cal, omega3_flux_cal = run_chi3(-16)
print("Omega: {}, 3Omega: {}".format(omega_flux_cal[0],omega3_flux_cal[0]))


pts = np.linspace(-6,0,20)
_, _, omega_psd, omega3_psd = zip(*[run_chi3(k_iter) for k_iter in pts])


quad = (10 ** pts) ** 2

plt.figure(dpi=150)
plt.loglog(10 ** pts,np.array(omega_psd)/omega_flux_cal[0],'o-',label='$\omega$')
plt.loglog(10 ** pts,np.array(omega3_psd)/omega_flux_cal[0],'o-',label='$3\omega$')
plt.loglog(10**pts,quad,'k',label='quadratic line')
plt.grid(True)
plt.xlabel('$\chi^{(3)}$')
plt.ylabel('Transmission/ Incident Power')
plt.legend()
plt.show()

_, _, omega_flux_1, omega3_flux_1 = run_chi3(-3,1)
_, _, omega_flux_2, omega3_flux_2 = run_chi3(-6,10)

print('-------------------------------')
print("Difference between powers: {}%".format(abs(omega3_flux_1[0]-omega3_flux_2[0])/omega3_flux_1[0] * 100))

