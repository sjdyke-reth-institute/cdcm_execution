"""
Defies a Quantify class.

Author:
	Ilias Bilionis
	Roman Ibrahimov

Date:
	3/10/2022

TODO:
	Figure out how to enforce SI units.
"""


__all__ = ['Quantity', 'Parameter', 
		   'StateVariable', 'PhysicalStateVariable', 'HealthStateVariable']


import numpy as np
import pint


ureg = pint.UnitRegistry()


class Quantity(object):

	"""
	Defines a CDCM quantity. The quantity knows its units.
	It has a decscription that explains what it is.
	It has a name. And it has a value.

	Arguments:

		value:      The value of the quantity. Must be an int, a double or a 
				    numpy array of ints or floating point numbers.
		units:      Must be a string or a pint object that describes an SI
				    physical unit.
		name:       A string. The name of the quantity. Please be expressive.
		desciption: A desciption of the quantity. Please be expressive.

	"""

	def __init__(self, value, units, name, description=None):
		# Sanity checks
		assert isinstance(value, int) or isinstance(value, float) or \
			(isinstance(value, np.ndarray) and value.dtype == float)
		ureg.check(units)
		assert isinstance(name, str)
		assert description is None or isinstance(description, str)
		# Assign values
		self._value = value
		self._units = units 
		self._name = name
		self._description = description

	@property
	def value(self):
		return self._value

	@property
	def units(self):
		return self._units

	@property
	def name(self):
		return self._name
	
	@property
	def description(self):
		return self._description

	@property
	def type(self):
		return type(self).__name__
	
	def __str__(self):
		# TODO: Fix this so that it prints the name of the clas
		return self.type + '(value=' + str(self.value) + \
			', units="' + self.units + '"' + \
			', name="' + self.name + '"' + \
			', description="' + self.description + '")'


class Parameter(Quantity):

	"""
	A class representing a parameter of a system.
	"""

	pass 


class StateVariable(Quantity):

	"""
	A class representing a system state variable.
	"""

	pass


class PhysicalStateVariable(StateVariable):

	"""
	A class representing a physical system state variable.
	"""

	pass 


class HealthStateVariable(StateVariable):

	"""
	A class representing a health state variable.
	"""

	pass


if __name__ == '__main__':
	p = PhysicalStateVariable(10.0, "meters", "length")
	print(type(p).__name__)
	print(p.type)
	print(str(p))