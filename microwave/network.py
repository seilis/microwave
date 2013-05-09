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
import numpy as np
from numpy import sqrt,log10

# Converts a dataset to dB from real/imaginary
# Assumes first column is Frequency
# TODO: Change to remove frequency from input data. This will likely require
# changing the VNA read_CSV function.
def reim_to_dB(Dat):
	lx = 2*(len(Dat[0])-1)+1
	ly = len(Dat)
	print(lx)
	dbDat = np.array(np.zeros((lx,ly)),dtype=complex)
	for i in range(0,ly-1):
		dbDat[i,0] = Dat[i,0]
		for j in range(1,len(Dat[0,:])-2):
			print(j)
			data = point_re_im_to_dB(Dat[i,j])
			dbDat[i,2*j-1] = data[0]
			dbDat[i,2*j] = data[1]
	
	return dbDat

# TODO: Finish this.
#def dB_to_reim(Dat):
#	raise NotImplementedError

# Convert a S-parameters array into a Z-parameters array
def S_to_Z(S,Z0=50.0):
	# P is the number of frequency points
	# M is the matrix component length
	if S.ndim == 1:
		P = S.shape
		M = 1
	elif S.ndim == 2:
		(P,M) = S.shape
	else:
		raise ValueError('You can only have 1 or 2-dimensional arrays for this function.')

	# Calculate the linear dimension of the matrix
	Mlin = int(sqrt(M).real)

	# Create the output array
	Z = []
	U = np.eye(Mlin)

	for line in S:
		# Unpack the line into a square form
		Matrix = np.reshape(line,(Mlin,Mlin))	

		# Compute Z-parameters in square form
		# Formula from Pozar (pg. 117)
		Ztmp = Z0*np.dot((U+Matrix),np.linalg.inv(U-Matrix))

		#	Pack back into a line and copy to Z
		Z.extend([np.reshape(Ztmp,M)])
	
	return np.array(Z)


#def S_to_Y(S,Y0=0.02):

def Z_to_S(Z,Z0=50.0):
	# P is the number of frequency points
	# M is the matrix component length
	(P,M) = Z.shape

	# Calculate the linear dimension of the matrix
	Mlin = int(sqrt(M).real)
	
	# Create the output array
	S = []
	U = np.eye(Mlin)

	for line in Z:
#		Unpack the matrix into a square form
		Matrix = np.reshape(line,(Mlin,Mlin))/Z0
		
#		Compute the S-parameters in a square form
		# Formula from Pozar (pg. 117)
		Stmp = np.dot(np.linalg.inv(Matrix+U),Matrix-U)

#		Put back into a line and copy to S
		S.extend([np.reshape(Stmp,M)])
	
	return np.array(S)

# Convert S parameters to ABCD parameters. Default assumes Z0=50 ohms.
def S_to_ABCD(dat,Z0=50.0):
	# Initialize A,B,C,D lists.
	A = []
	B = []
	C = []
	D = []
	# For each row calculate A, B, C, D.
	for i in dat:
		# S-matrix names look nicer than indices.
		S11 = i[0]
		S12 = i[1]
		S21 = i[2]
		S22 = i[3]

		# Calculate A, B, C, D using formulas from Pozar p. 187.
		A.extend([((1+S11)*(1-S22)+S12*S21)/(2*S21)])
		B.extend([Z0*((1+S11)*(1+S22)-S12*S21)/(2*S21)])
		C.extend([((1-S11)*(1-S22)-S12*S21)/(Z0*2*S21)])
		D.extend([((1-S11)*(1+S22)+S12*S21)/(2*S21)])

	# Condense into ABCD parameter list.	
	abcd = np.transpose(np.array([A,B,C,D]))
	return abcd

# Convert ABCD parameters to S-parameters, default assumes Z0=50 ohms.
def ABCD_to_S(dat,Z0=50.0):
	# Initialize S-parameter lists.
	S11 = []
	S12 = []
	S21 = []
	S22 = []
	# For each row calculate S-parameters.
	for i in dat:
		# ABCD names look nicer than indices.
		A = i[0]
		B = i[1]
		C = i[2]
		D = i[3]
	
		# Calculate denominator once, it is the same for all.
		denom = A+B/Z0+C*Z0+D

		# Calculate S-parameters using formulas from Pozar P. 187.
		S11.extend([(A+B/Z0-C*Z0-D)/denom])
		S12.extend([2*(A*D-B*C)/denom])
		S21.extend([2/denom])
		S22.extend([(-A+B/Z0-C*Z0+D)/denom])

	# Condense into S-parameter list
	S = np.transpose(np.array([S11,S12,S21,S22]))
	return S

# This function converts from Z parameters to Y parameters
def Z_to_Y(Z):
	# P is the number of frequency points
	# M is the matrix component length
	if Z.ndim == 1:
		P = Z.shape
		M = 1
	elif Z.ndim == 2:
		(P,M) = Z.shape
	else:
		raise ValueError('You can only have 1 or 2-dimensional arrays for this function.')

	# Calculate the linear dimension of the matrix
	Mlin = int(sqrt(M).real)

	# Create the output array
	Y = []

	for line in Z:
		# Unpack the line into a square form
		Matrix = np.reshape(line,(Mlin,Mlin))	

		# Compute Y-parameters in square form
		# Formula from Pozar (pg. 117)
		Ytmp = np.linalg.inv(Matrix)

		#	Pack back into a line and copy to Y
		Y.extend([np.reshape(Ytmp,M)])
	
	return np.array(Y)

# This function converts from Z parameters to Y parameters
def Y_to_Z(Y):
	# P is the number of frequency points
	# M is the matrix component length
	if Y.ndim == 1:
		P = Y.shape
		M = 1
	elif Y.ndim == 2:
		(P,M) = Y.shape
	else:
		raise ValueError('You can only have 1 or 2-dimensional arrays for this function.')

	# Calculate the linear dimension of the matrix
	Mlin = int(sqrt(M).real)

	# Create the output array
	Z = []

	for line in Y:
		# Unpack the line into a square form
		Matrix = np.reshape(line,(Mlin,Mlin))	

		# Compute Z-parameters in square form
		# Formula from Pozar (pg. 117)
		Ztmp = np.linalg.inv(Matrix)

		#	Pack back into a line and copy to Z
		Z.extend([np.reshape(Ztmp,M)])
	
	return np.array(Z)

# Cascades two 2-port networks using the ABCD matrix multiplication
# method of cascading networks. The output is the resulting ABCD
# array of the total network.
def cascade_ABCD(ABCD1,ABCD2):
	# Initialize the output list.
	Output = []

	Num = len(ABCD1)

	# For each frequency point, convert the input data into
	# the equivalent matrices and perform matrix multiplication.
	for i in range(Num):
		# Convert to 2x2 matrices.
		dev1 = np.reshape(ABCD1[i],(2,2))
		dev2 = np.reshape(ABCD2[i],(2,2))
		
		# Calculate the matrix dot (inner) product.
		total = np.dot(dev1,dev2)

		# Reshape the calculated ABCD matrix into a list
		# and append to the output.
		Output.extend([np.reshape(total,4)])

	# Return the output as a NumPy array.
	return np.array(Output)
		

# Subtract two impedances that are in parallel. This is useful for
# component value extraction. The output is the value of "sub" subtracted
# from "dat" following the impedance rules for parallel components.
def subtract_Z_parallel(dat,sub):
	# Convert impedance values to admittance to simplify math.
	dat_Y = 1.0/dat
	sub_Y = 1.0/sub

	# Perform admittance subtraction.
	res_Y = dat_Y - sub_Y

	# Convert result to impedance
	res = 1.0/res_Y

	return res
