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
from . import Parameter, StateVariable, PhysicalStateVariable, \
			  HealthStateVariable


class System(ABC):
	"""Describes an abstract System.

	A system has the following characteristics:
		- It has a name.
		- It has a description of what it does.
		- It knows its current_state.
		- It knows which variables from other systems may affect its transition.
		- It knows how to transition its state to the next timestep.

	All specific CDCM systems must inherit from this class.

	Keyword Arguments:
	name         -- A name for the system.
	state		 -- A dictionary with keys that are strings corresponding to
					the state variable names and values that are 
					`StateVariable`.
	parameters   -- A dictionary with keys that are strings corresponding to
				    parameter names and values that are Parameter objects.
					parameters of a system.
	parents      -- A dictionary with keys that are strings corresponding
					to the state variable names and values that are the
					`System` from which this variable must be taken.
	description  --	A long description of the system.
	"""

	def __init__(self, name="System", state={}, parameters={}, parents={}, description=None):
		# Sanity checks
		assert isinstance(name, str)
		assert isinstance(description, str)
		# Sanity check for state variables
		assert isinstance(state, dict)
		for s in state.values():
			assert isinstance(s, StateVariable)
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
		self._name = name
		self._description = description
		self._current_state = state
		self._next_state = deepcopy(state)
		self._parameters = parameters
		self._parents = parents
		self._physical_state = self._get_state_of_type(PhysicalStateVariable)
		self._health_state = self._get_state_of_type(HealthStateVariable)

	def has_state(self, state_name):
		"""Return True if the system has a state called `state_name`.
		"""
		return state_name in self._current_state.keys()

	def has_paremeter(self, param_name):
		"""Return True if the system has a parameter called `param_name`.
		"""
		return param_name in self._parameters.keys()

	def get_state(self, state_name):
		"""Get the state called `state_name`.
		"""
		assert self.has_state(state_name)
		return self._current_state[state_name]

	def get_parameter(self, param_name):
		"""Get the parameter called `param_name`.
		"""
		assert self.has_parameter(param_name)
		return self._parameters[param_name]

	def _get_state_of_type(self, Type):
		"""Return a dictionary with all state components of type `Type`.
		"""
		res = {}
		for n, s in self.state.items():
			if isinstance(s, Type):
				res[n] = s
		return res

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

	@property
	def parents(self):
		return self._parents
	
	
	@abstractmethod
	def _calculate_next_state(self, dt):
		"""Calculate the next sate of the system using the current one.

		Arguments:
		dt -- the time step to use when calculating the next state.

		The function assumes that `self._current_state` already contains
		the current state of the system and that access to all input
		variables is available through `self.parents`.

		This function should not return anything. It should just calculate
		the next state and store the result in `self._next_state`.
		"""
		pass

	def _transition(self):
		"""This function transitions to the next state.

		The function simply swaps the `self._current_state` with 
		`self._next_state`. It is essential for ensuring deterministic
		behavior.
		"""
		self._current_state, self._next_state = self._next_state, self._current_state

	def __str__(self):
		"""Return a readable string representation of the class.

		TODO: Make this pretty.
		TODO: Add verbosity control.
		"""
		res = f"""System name:    {self.name}
		Physical state: {self.physical_state}
		Health state:   {self.health_state}
		Parameters:     {self.parameters}
		Parents:		{self.parents}
		Description:	{self.description}
		"""
		return res

	def __repr__(self):
		"""Return a complete string representation of the class.
		"""
		# TODO: Write me
		pass 
