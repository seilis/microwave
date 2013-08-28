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

from math import pi

# Class for working with inductor data.
class Inductor:
	# Calculates the quality factor of an inductor from a 1-port set
	# of measurements.
	@staticmethod
	def quality(dat):
		return dat.imag/dat.real
	
	# Calculates the inductance of an inductor from a 1-port set of
	# measurements and the frequency (in Hz)
	@staticmethod
	def Z_to_Inductance(dat,freq):
		return dat.imag/2/pi/freq

# Class for working with capacitor data.
class Capacitor:
	# Calculates the quality factor of a capacitor from a 1-port set
	# of measurements
	@staticmethod
	def quality(dat):
		return -dat.imag/dat.real

	# Calculates the capacitance of a capacitor from a 1-port set
	# of measurements and the frequency (in Hz)
	@staticmethod
	def Z_to_Capacitance(dat,freq):
		return -1/2/pi/dat.imag
