import meep as mp
import argparse
import matplotlib.pyplot as plt

def main(args):

    resolution = 20   # pixels/um

    eps = 13          # dielectric constant of waveguide
    w = 1.2           # width of waveguide
    r = 0.36          # radius of holes
    d = 1.4           # defect spacing (ordinary spacing = 1)
    N = args.N        # number of holes on either side of defect

    sy = args.sy      # size of cell in y direction (perpendicular to wvg.)
    pad = 2           # padding between last hole and PML edge
    dpml = 1          # PML thickness

    sx = 2*(pad+dpml+N)+d-1  # size of cell in x direction

    cell = mp.Vector3(sx,sy,0)

    blk = mp.Block(size=mp.Vector3(mp.inf,w,mp.inf), material=mp.Medium(epsilon=eps))
    geometry = [blk]

    for i in range(N):
            geometry.append(mp.Cylinder(r, center=mp.Vector3(d/2+i)))
            geometry.append(mp.Cylinder(r, center=mp.Vector3(-(d/2+i))))

    pml_layers = [mp.PML(1.0)]

    fcen = args.fcen   # pulse center frequency
    df = args.df       # pulse frequency width

    src = [mp.Source(mp.GaussianSource(fcen, fwidth=df),
                     component=mp.Ey,
                     center=mp.Vector3(-0.5*sx+dpml),
                     size=mp.Vector3(0,w))]

    sym = [mp.Mirror(mp.Y, phase=-1)]

    sim = mp.Simulation(cell_size=cell,
                        geometry=geometry,
                        boundary_layers=pml_layers,
                        sources=src,
                        symmetries=sym,
                        resolution=resolution)
    freg = mp.FluxRegion(center=mp.Vector3(0.5*sx-dpml-0.5),
                         size=mp.Vector3(0,2*w))

    nfreq = 500 # number of frequencies at which to compute flux

    # transmitted flux
    trans = sim.add_flux(fcen, df, nfreq, freg)

    vol = mp.Volume(mp.Vector3(0), size=mp.Vector3(sx))

    plt.figure(dpi=150)
    sim.plot2D()
    #plt.show()
    plt.savefig('2Dstructure.png')

    sim.run(mp.at_beginning(mp.output_epsilon),
                mp.during_sources(mp.in_volume(vol, mp.to_appended("hz-slice", mp.at_every(0.4, mp.output_hfield_z)))),
                until_after_sources=mp.stop_when_fields_decayed(50, mp.Ey, mp.Vector3(0.5*sx-dpml-0.5), 1e-3))

    sim.display_fluxes(trans)  # print out the flux spectrum
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-N', type=int, default=3, help='number of holes on either side of defect')
    parser.add_argument('-sy', type=int, default=6, help='size of cell in y direction (perpendicular to wvg.)')
    parser.add_argument('-fcen', type=float, default=0.25, help='pulse center frequency')
    parser.add_argument('-df', type=float, default=0.2, help='pulse frequency width')
    args = parser.parse_args()
    main(args)
