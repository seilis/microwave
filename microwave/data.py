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
import numpy
import csv
import re
import numpy as np
import cmath
import math
from math import pi

# Class for working with data output from an Agilent VNA.
class vna:

	# Read a CSV saved by the VNA.
	@staticmethod
	def read_data(fn):
		data_raw = []
		file_read = csv.reader(open(fn),delimiter=',')
	
		# This part will do something more useful in the future 
		# (such as reading in information about the dataset).
		# Right now, this skips lines in the file until it reaches a line that reads
		# "BEGIN CH1_DATA". This is the line immediately before the actual data
		# begins.
		header = True
		while header:
			line = file_read.next()
			if line == ['BEGIN CH1_DATA']:
				header = False
		
		# The line after "BEGIN CH1_DATA" contains the format for the data.
		# This is used to determine which processing should be done on
		# the data before output.
		format_line = file_read.next()
	
		# Create the data format dictionary. This dictionary stores the columns
		# and the format of those columns.
		# Format:
		#   key => (Complement column type, column number, complement column number)
		data_format = {}
		for col in format_line:
			# Split the format line into colums and formats.
			Name_Match = re.match('(S[0-9]+)\((\w+)\)',col)
		
			# Agilent VNAs store complex data as pairs of columns
			# which are one of "dB-degrees", "Magnitude-degrees" or
			# "Real-Imaginary". This processes the first data column
			# and determines the complement, column number and
			# column number of the complement data. 
			if Name_Match:
				if Name_Match.group(2) in ['DB','MAG','REAL']:
					if Name_Match.group(2) == 'REAL':
						Complement = 'IMAG'
					else:
						Complement = 'DEG'
					data_format[Name_Match.group(1)] = \
						(
							Name_Match.group(2),
							format_line.index(col),
							format_line.index(Name_Match.group(1)+'('+Complement+')')
						)
	
		# Read first line of data
		cur_line = file_read.next()
		
		# Loop through all of the data and copy to the raw data array
		while len(cur_line) == len(format_line): 
			data_raw.extend([cur_line])
			cur_line = file_read.next()
	
		# Sort the dictionary keys into the correct order
		keys = sorted(data_format.keys())
	
		# Populate the output data array with the frequency data
		data = [np.array(data_raw,dtype=float)[:,0]]
	
		# For each key
		for i in keys:
			# Get the form and the columns
			form = data_format[i][0]
			col1 = data_format[i][1]
			col2 = data_format[i][2]
	
			# The column data vector (all data in the single column)
			col_dat = []
	
			# Depending on the format, convert all of the data
			if form == 'DB':
				# Convert to Re/Im
				for line in data_raw:
					col_dat.extend([complex(cmath.rect(10**(float(line[col1])/20.0),
						float(line[col2])/180*math.pi))])
			elif form == 'MAG':
				# Convert to Re/Im
				for line in data_raw:
					col_dat.extend([complex(cmath.rect(float(line[col1]),float(line[col2]/180*math.pi)))])
			else: # Already in components, but should be combined to Re+j*Im
				# Convert to Re/Im
				for line in data_raw:
					col_dat.extend([complex(float(line[col1])+1j*float(line[col2]))])
		
			# Put the column data into the output data vector
			data.extend([col_dat])
	
		# Make sure the output data vector is a complex numpy array
		data_cpx = np.array(data,dtype=complex) 
		
		# Output final data array as a numpy array (transpose to row-major format)
		return np.transpose(data_cpx)


############################################################################
# Some utility functions for working with data.

# Interpolate complex data to a new set of measurement points
# by interpolating the real and imaginary parts separately. Uses a linear
# interpolation. The np.interp() function will attempt to extrapolate values 
# that lie outside of the original data range.
def cpxInterp(x_new,x_orig,y_orig):
	y_new_real = np.interp(x_new,x_orig,y_orig.real)
	y_new_imag = np.interp(x_new,x_orig,y_orig.imag)
	return y_new_real+1.0j*y_new_imag

# Smoothing function
# Note: following example adapted from http://www.scipy.org/Cookbook/SignalSmooth
# and http://glowingpython.blogspot.ca/2012/02/convolution-with-numpy.html
def smooth(data,window):
	# Extend the data array
	data_extended = np.r_[data[window-1:0:-1],data,data[-1:-window:-1]]

	# Create a kaiser smoother function. The magic number 2 is the weighting of
	# the kaiser function
	kaiser = np.kaiser(window,2)
	
	# Apply the convolution
	smoothed = np.convolve(kaiser/kaiser.sum(),data_extended,mode='valid')
	
	# Find the number valid for
	num_valid = np.floor(window/2)

	return smoothed[num_valid:len(smoothed)-num_valid]
	
