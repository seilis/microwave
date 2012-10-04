from math import pi

class Inductor:
	@staticmethod
	def quality(dat):
		return dat.real/dat.imag
	
	@staticmethod
	def Z_to_Inductance(dat,freq):
		return dat.imag/2/pi/freq