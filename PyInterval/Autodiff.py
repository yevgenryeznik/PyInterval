#!/usr/local/bin/python3
from numbers import Number

class AD(object):
	# class constructor
	def __init__(self, val, der = 1):
		self.val = float(val)
		if der == None: 
			der = 0.0
		if der == "variable":
			der = 1.0
		self.der = float(der)

	# string representation of the object of class AD      
	def __str__(self):
		return "[value = % 17.17f, derivative = % 17.17f]" % (self.val, self.der)

	# addition operator overloading      
	def __add__(self, other):
		if isinstance(other, Number):
			other = AD(other)
		
		val = self.val + other.val
		der = self.der + other.der
		return(AD(val, der))

	# addition operator overloading (used in the case 'number' + 'AD' by converting 'number' to 'AD')     
	def __radd__(self, other):
		if isinstance(other, Number):
			other = AD(other)
		
		return(other+self)
		
	# subtraction operator overloading
	def __sub__(self, other):
		if isinstance(other, Number):
			other = AD(other)

		val = self.val - other.val
		der = self.der - other.der
		return(AD(val, der))
		
	# subtraction operator overloading (used in the case 'number' - 'AD' by converting 'number' to 'AD')     
	def __rsub__(self, other):
		if isinstance(other, Number):
			other = AD(other)
		
		return(other-self)

	# multipication operator overloading
	def __mul__(self, other):
		if isinstance(other, Number):
			other = AD(other)
			
		val = self.val * other.val
		der = self.val * other.der + self.der*other.val
		return(AD(val, der))
		
	# multipication operator overloading (used in the case 'number' * 'interval' by converting 'number' to 'interval')     
	def __rmul__(self, other):
		if isinstance(other, Number):
			other = AD(other)
		
		return(other*self)
		
	# division operator overloading (self is in numerator)      
	def __div__(self, other):
		if isinstance(other, Number):
			other = AD(other)
		
		val = self.val/other.val
		der = (self.der - val*other.der)/other.val
		return(AD(val, der))
			
		
	# division operator overloading (self is in denomenator)     
	def __rdiv__(self, other):
		if isinstance(other, Number):
			other = AD(other)

		return(other/self)

	# unary minus operator overloading      
	def __pos__(self):
		return(self)
		
	# unary minus operator overloading      
	def __neg__(self):
		return(Ad(-self.val, -self.der))
		
