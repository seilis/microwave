############################################################################
# Copyright 2012 Aaron Seilis
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
class vna:
	def read_data(fn):
		data_raw = []
		file_read = csv.reader(open(fn),delimiter=',')
	
		# This part will do something more useful in the future 
		# (such as reading in information about the dataset
		header = True
		while header:
			line = file_read.next()
			if line == ['BEGIN CH1_DATA']:
				header = False
		
		# This line contains the format for the data. This is used 
		# to determine which processing should be done on
		# the data before output.
		format_line = file_read.next()
	
		data_format = {}
		for col in format_line:
			Name_Match = re.match('(S[0-9]+)\((\w+)\)',col)
		
			if Name_Match:
				if Name_Match.group(2) in ['DB','MAG','REAL']:
					if Name_Match.group(2) == 'REAL':
						Complement = 'IMAG'
					else:
						Complement = 'DEG'
					data_format[Name_Match.group(1)]=(Name_Match.group(2),format_line.index(col),format_line.index(Name_Match.group(1)+'('+Complement+')'))
		
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
					col_dat.extend([complex(rect(10**(float(line[col1]))/20,
						float(line[col2])/180*pi))])
			elif form == 'MAG':
				# Convert to Re/Im
				for line in data_raw:
					col_dat.extend([complex(rect(float(line[col1]),float(line[col2]/180*pi)))])
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
