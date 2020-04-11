#!/usr/bin/env python3

import matplotlib.pyplot as plt
from software.analyse.mulliken import parse_mulliken_file, get_graph_linetype, get_indices_of_elements

# Read in atoms information
output_file = "data/Fe-CO/fe-co_light.log"
from ase.io import read
atoms = read(output_file)

# Read in Mulliken data from file
mulliken_file = "data/Fe-CO/Mulliken.out"
with open(mulliken_file, 'r') as read_stream:
    lines = read_stream.readlines()

# Parse data from Mulliken file
mulliken_data = parse_mulliken_file(lines)

#### Assertion statements ####
assert(mulliken_data.get_natoms() == 3)
assert(mulliken_data.get_nspin() == 2)
assert(mulliken_data.get_nkpts() == 1)
assert(mulliken_data.get_nstates() == 32)
assert(mulliken_data.get_data_integrity())
#####

#TODO: homo, lumo = atoms.get_homo_lumo_data()
# Collect all the density of states data to plot
x, all_data = mulliken_data.get_all_plot_data()

# Collect the indices for each element we are interested in
fe_indices = get_indices_of_elements(atoms.get_chemical_symbols(), 'fe')
c_indices = get_indices_of_elements(atoms.get_chemical_symbols(), 'c')
o_indices = get_indices_of_elements(atoms.get_chemical_symbols(), 'o')

# Collect the density of states data to plot as a function of atomic label
x, fe = mulliken_data.get_plot_data(fe_indices, range(mulliken_data.get_nspin()),
                                    range(mulliken_data.get_nkpts()), 'all')
x, c = mulliken_data.get_plot_data(c_indices, range(mulliken_data.get_nspin()),
                                    range(mulliken_data.get_nkpts()), 'all')
x, o = mulliken_data.get_plot_data(o_indices, range(mulliken_data.get_nspin()),
                                    range(mulliken_data.get_nkpts()), 'all')

# Put this at the end so it covers everything else and shows the outline of the DOS correctly
for sp in range(len(all_data)):
    if sp == 0:
        plt.plot(x, fe[sp], lw=2, color='red', ls=get_graph_linetype())
        plt.plot(x, fe[sp]+c[sp], lw=2, color='green', ls=get_graph_linetype())
        plt.plot(x, fe[sp]+c[sp]+o[sp], lw=2, color='blue', ls=get_graph_linetype())
        plt.plot(x, all_data[sp], lw=2, color='black', ls=get_graph_linetype())
    else: # (sp == 1)
        plt.plot(x, -(fe[sp]), lw=2, color='red', ls=get_graph_linetype())
        plt.plot(x, -(fe[sp]+c[sp]), lw=2, color='green', ls=get_graph_linetype())
        plt.plot(x, -(fe[sp]+c[sp]+o[sp]), lw=2, color='blue', ls=get_graph_linetype())
        plt.plot(x, -(all_data[sp]), lw=2, color='black', ls=get_graph_linetype())

# Work to rescale axes. Extracts the maximum y-value
ymax = max(map(max, all_data))*1.1
ymin = 0
if len(all_data) > 1:
    ymin = -ymax
    plt.axhline(y=0, xmin=min(x), xmax=max(x), color='black', lw=2)
plt.ylim(ymin, ymax)
plt.yticks([])
plt.ylabel('Density of States (1/eV)')

# Organise x-axis
#plt.xlim(min_point+10, max_point-10)
plt.xlabel(mulliken_data.get_graph_xlabel())

# HOMO
#plt.axvline(x=homo, ymin=-100, ymax=100, color='black', lw=2, ls=line_types[k]) # MFI

# Display the graphs
#plt.show()