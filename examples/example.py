#! /usr/bin/env python2
############################################################################
# Copyright 2012-2013 Aaron Seilis
#
# This file is part of MicrowaveEngineering.
#
# MicrowaveEngineering is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MicrowaveEngineering is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MicrowaveEngineering. If not, see
# <http://www.gnu.org/licenses/>.
############################################################################

import microwave as mw
import matplotlib.pyplot as plt


# Load example S-parameter data from "Agilent_VNA_Example.csv"
Data = mw.vna.read_data('Agilent_VNA_Example.csv')

# Unpack frequency (first column), scale to GHz
F = Data[:,0].real*1e-9

# Unpack S-parameters (all columns after first)
S = Data[:,1:]


############################################################################
# Create a Smith-chart plot
smith = mw.smith.create_smith().axes[0]

# Plot S-parameter
smith.plot(S.real,S.imag)

plt.title('Smith Chart of 1-port example data')
plt.savefig('Example_Smith_Plot.png')
plt.clf()

############################################################################
# Convert to impedance (Z)

# Here, S is a 1-port measurement, but this function can take an array of 
# any number of ports. There is also an optional characteristic impedance
# parameter that defaults to 50 Ohms.
Z = mw.network.S_to_Z(S)

# Plot impedance using standard MatPlotLib commands.
plt.plot(F,Z.real,label='Resistance',color='b',marker='h',markevery=20)
plt.plot(F,Z.imag,label='Reactance',color='b',linestyle='--',marker='*',markevery=20)

plt.grid(True)
plt.legend(ncol=2,loc='lower right')

plt.title('Example plot of a measured impedance')
plt.xlabel('Frequency (GHz)')
plt.ylabel('Impedance ($\Omega$)')

plt.savefig('Example_Rect_Plot.png')
plt.clf()
