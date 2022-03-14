"""
Tests the functionality of the System class for a simple isolated system.

Author:
	Ilias Bilionis

Date:
	3/14/2022

"""


from cdcm import *


class TestIsolatedSystem(System):

	def __init__(self):
		name = "Isolated System"
		state = {"x": PhysicalStateVariable(0.0, "meters", "x", track=True, 
											description="The x variable."),
				 "h": HealthStateVariable(0, None, "x", track=True,
				 						  description="The h variable.")}
		parameters = {"rate_of_change": Parameter(0.01, "meters / second",
												 "rate_of_change",
					  							 description="The rate of change.")}
		super().__init__(name=name, state=state, parameters=parameters,
						 description="A simple isolated system.")

	def _calculate_next_state(self, dt):
		pass


if __name__ == "__main__":
	system = TestIsolatedSystem()
	print(system.state)
	print(str(system))
