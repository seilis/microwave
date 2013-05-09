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
import csv
import numpy as np
import matplotlib.pyplot as plt
import re
from math import log

# readCSV
# This function imports CSV files that have been written by HFSS.
def readCSV(fn): # fn = file name
	# Open reader instance
	fread = csv.reader(open(fn),delimiter=',')

	# Initialize the data set in this scope.
	data = []
	
	# Read every row and split the columns into an array.
	# Once a row has been split into columns, append to the "data"
	# array.
	for row in fread:
		newCol = []
		for col in row:
			try:
				if (col == ""):
					newCol.extend([0.0])
				else:
					newCol.extend([float(col)])
			except:
				# Sometimes data from HFSS has blanks. These are caused by errors in
				# the simulation that results in incomplete data sets. It is still
				# useful to import these pieces of data, but they are not imported
				# correctly by the "try" statement. The correct behaviour is to test
				# if an empty cell is found and then represent it as not-a-number.
				if (col == ""):
					newCol.extend([float('nan')])
				else:
					pass
		# Ignore lines which are completely empty.
		if (newCol != []):
			data.extend([newCol])
	# Return the data array as a NumPy ndArray.
	return np.array(data)

# This function is a helper function to change the variable names and titles
# from the canonical form in HFSS to something prettier.
def fixString(s):
	# Change underscores to spaces
	s = re.sub('_',' ',s)	
	
	# Remove empty unit indicators are removed
	s = re.sub('\[\]','',s)

	# Remove extra whitespace
	s = s.strip()
	return s

# Calculates the number of valid data values
def numValid(A):
	Valid = 0 # number of valid entries
	for i in A:
		if (i != ''):
			Valid += 1
	return Valid

# Return the valid value
def getValid(A):
	for i in A:
		if (i != ''):
			return float(i)

# collapseArray(A)
# This function takes an array that has redundant columns that contain
# non-contradictory data and merges the redundant columns. It does this by
# finding the unique column names and then creating a mapping between the
# column name and the redundant column numbers.
# 
# This function is very useful for processing arrays from HFSS simulations
# that contain multiple frequency ranges in the same simulation. HFSS outputs
# the information in different columns and it is typically useful to merge
# these columns into a single column when the frequency ranges don't overlap.
def collapseArray(A):
	# Initialize the collapsed array.
	Out = []

	# Find Unique Columns
	Cols = []
	for val in set(A[0,:]):
		Cols.extend([str(val)])
	Out.extend([Cols])

	# The map dictionary maps the column name to the column number.
	Map = {}
	
	# For each column name
	for val in Cols:
		# create a mapping list
		mapping = []
		for i in range(len(A[0,:])): 
			# If the top row is the current unique value
			# add the column number to the map.
			if (A[0,i] == val):
				mapping.extend([i])
		# store the complete mapping in the dictionary
		Map[val]=mapping
	
	# Copy correct values from A to Out
	for row in range(1,len(A[:,0])): # for each row in the input vector
		newRow = []
		# for each unique column
		for col in Cols:
			# Create temp data vector
			data = []
			
			# copy data in to data vector
			for d in Map[col]:
				data.extend([A[row,d]])

			# Debugging print statement.
			#print(str(data))	
			
			# Copy the condensed data to the new row.
			newRow.extend([getValid(data)])
		# Save the condensed row to the output array.
		Out.extend([newRow])
	# Return the condensed array as a NumPy array.
	return np.array(Out)
