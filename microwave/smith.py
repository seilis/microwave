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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MicrowaveEngineering.  If not, see 
# <http://www.gnu.org/licenses/>.
############################################################################
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from matplotlib.lines import Line2D

# Create a MPL figure object that has an axis instance formatted as a simple
# Smith chart. This figure object is returned, and the axis can be accessed
# by "axis" member of the "fig" object.
def create_smith():
	# Create the figure object
	fig = plt.figure(facecolor='white')

	# Add a single plot to the figure
	ax = fig.add_subplot(1,1,1,aspect='equal')
#	fig.add_axes([0.05, 0.05, 1.1, 1.1])
#	ax = fig.axes[0]
	
	# Remove the figure boundaries
	ax.get_xaxis().set_visible(False)
	ax.get_yaxis().set_visible(False)
	
	ax.spines['top'].set_visible(False)
	ax.spines['bottom'].set_visible(False)
	ax.spines['left'].set_visible(False)
	ax.spines['right'].set_visible(False)

	# Add Smith-chart impedance circles
	Circ_zero = plt.Circle((0,0),radius=1.0,linestyle='solid',
									linewidth=2,color='black',fill=False)
	Circ_unity = plt.Circle((0.5,0),radius=0.5,linestyle='solid',
									linewidth=1,color='grey',fill=False)
	Circ_imag_low = Arc((1,-1),2,2,angle=0.0,theta1=90.0,theta2=180.0,
								linestyle='solid',linewidth=1,color='grey',fill=False)
	Circ_imag_high = Arc((1,1),2,2,angle=0.0,theta1=180.0,theta2=270.0,
								linestyle='solid',linewidth=1,color='grey',fill=False)

	Real_Line = Line2D((-1,1),(0,0),linestyle='solid',linewidth=1,color='grey')
	#ax.axhline(0,xmin=-1,xmax=1,linestyle='solid',linewidth=1,color='grey')

	ax.add_patch(Circ_imag_high)
	ax.add_patch(Circ_imag_low)
	ax.add_patch(Circ_unity)
	ax.add_patch(Circ_zero)
	ax.add_line(Real_Line)

	return fig
	
