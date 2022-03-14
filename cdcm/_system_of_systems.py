"""
A class representing a system of systems.

Author:
	Ilias Bilionis

Date:
	3/14/2022

"""


__all__ = ["SystemOfSystems"]



from collections import Iterable


from . import System


class SystemOfSystems(System):
	"""A class representing a system of systems.

	Keyword Arguments
	name        -- A name for the system.
	systems     -- A list of systems.
	description -- A description for the system.
	"""

	def __init__(self, name="SystemOfSystems", sub_systems=[], description=None):
		# Sanity check
		assert isinstance(sub_systems, Iterable)
		for s in sub_systems:
			assert isinstance(s, System)
		# Gather the parents and parameters
		parents = {}
		parameters = {}
		for s in sub_systems:
			parents.update(s.parents)
			parameters.update(s.parameters)
		self._sub_systems = sub_systems
		super().__init__(name=name, parents=parents, description=description)

	@property
	def sub_systems(self):
		return self._sub_systems

	@property
	def state(self):
		state = {}
		for s in self._sub_systems:
			state.update(s.state)
		return state

	def _calculate_next_state(self, dt):
		for s in self.sub_systems:
			s._calculate_next_state(dt)

	def _transition(self):
		for s in self.sub_systems:
			s._transition()

	@property
	def can_transition(self):
		"""
		Return True if the system can transition independently.

		TODO: Write this.
		"""
		raise NotImplementedError("TODO: Implement the `can_transition` for SystemOfSystems`.")
	