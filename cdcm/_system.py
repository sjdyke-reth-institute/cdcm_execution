"""
Defines an abstract system class.


Author:
	Ilias Bilionis

Date:
	3/11/2022

"""


__all__ = ['System']


from abc import ABC, abstractmethod
from copy import deepcopy
from ._quantity import Parameter, StateVariable


class System(ABC):
	"""
	Describes an abstract System.

	A system has the following characteristics:
		- It has a name.
		- It has a description of what it does.
		- It knows its current_state.
		- It knows which variables from other systems may affect its transition.
		- It knows how to transition its state to the next timestep.

	All specific CDCM systems must inherit from this class.

	Arguments:
		- name:
		- state:		  A dictionary with keys that are strings corresponding to
						  the state variable names and values that are StateVariable.
		- parameters:     A dictionary with keys that are strings corresponding to
						  parameter names and values that are Parameter objects.
						  parameters of a system.
		- description: 	  
		- parents: 		  ???

	TODO: Complete docstring.
	TODO: Think about the parents.
	"""

	def __int__(self, name, state={}, parameters={}, parents={}, description=None):
		# TODO: Add sanity cecks for name, description
		assert isinstance(state, dict)
		for s in state.values():
			assert isinstance(p, StateVariable)
		assert isinstance(parameters, dict)
		for p in parameters.values():
			assert isinstance(p, Parameter)
		self._name = _name 
		self._description = description
		self._current_state = state
		self._next_state = deepcopy(state)
		self._parameter = parameters

	@property
	def name(self):
		return self._name
	
	@property
	def description(self):
		return self._description
	
	@property
	def parameters(self):
		return self._parameters
	
	@abstractmethod
	def step(self, dt):
		pass

	def _transition(self):
		"""
		This function must be called after the step() function has been called
		for all Systems.

		Absolutely essential to ensure deterministic behavior.
		"""
		self._current_state, self._next_state = self._next_state, self._current_state


# TMP TESTING - TO BE DELETED
if __name__ == "__main__":
	# TMP 
	pass