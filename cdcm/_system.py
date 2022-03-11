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
from ._quantity import Parameter, StateVariable, PhysicalStateVariable, \
					   HealthStateVariable


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
		- parents: 		  A dictionary with keys that are strings corresponding
						  to the state variable names and values that are the
						  System from which this variable must be taken.

	TODO: Complete docstring.
	"""

	def __int__(self, name, state={}, parameters={}, parents={}, description=None):
		# TODO: Add sanity cecks for name, description
		assert isinstance(state, dict)
		# Sanity check for state variables
		for s in state.values():
			assert isinstance(p, StateVariable)
		# Sanity check for parameters
		assert isinstance(parameters, dict)
		for p in parameters.values():
			assert isinstance(p, Parameter)
		# Sanity check for parents
		assert isinstance(parents, dict)
		for k, v in parents.items():
			assert isinstance(k, str)
			assert isinstance(v, System)
			assert v.has_state(k)
		# Initialize variables
		self._name = _name 
		self._description = description
		self._current_state = state
		self._next_state = deepcopy(state)
		self._parameters = parameters
		self._parents = parents
		self._physical_state = self._get_state_of_type(PhysicalStateVariable)
		self._health_state = self._get_state_of_type(HealthStateVariable)

	def has_state(self, state_name):
		"""
		Return True if the system has a state called `state_name`.
		"""
		return state_name in self._current_state.keys()

	def has_paremeter(self, param_name):
		"""
		Return True if the system has a parameter called `param_name`.
		"""
		return param_name in self._parameters.keys()

	def get_state(self, state_name):
		"""
		Get the state called `state_name`.
		"""
		assert self.has_state(state_name)
		return self._current_state[state_name]

	def get_parameter(self, param_name):
		"""
		Get the parameter called `param_name`.
		"""
		assert self.has_parameter(param_name)
		return self._parameters[param_name]

	def _get_state_of_type(self, Type):
		"""
		Return a dictionary with all state components of type `Type`.
		"""
		res = {}
		for n, s in self.state.items():
			if isinstance(s, Type):
				res[n] = s
		return s

	@property
	def name(self):
		return self._name
	
	@property
	def description(self):
		return self._description
	
	@property
	def parameters(self):
		return self._parameters

	@property
	def state(self):
		return self._current_state
	
	@property
	def physical_state(self):
		return self._physical_state
	
	@property
	def health_state(self):
		return self._health_state
	
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