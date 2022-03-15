"""Tests the functionality of the System class for a simple isolated system.

Author:
    Ilias Bilionis

Date:
    3/14/2022

"""


from cdcm import *


class TestIsolatedSystem(System):

    def __init__(self):
        name = "Isolated System"
        state = {"x": PhysicalStateVariable(0.1, "meters", "x", track=True, 
                                            description="The x variable."),
                 "h": HealthStateVariable(0, None, "x", track=True,
                                          description="The h variable.")}
        parameters = {"rate_of_change": Parameter(1.2, "meters / second",
                                                  "rate_of_change",
                                                  description="The rate of change.")}
        super().__init__(name=name, state=state, parameters=parameters,
                         description="A simple isolated system.")

    def _calculate_next_state(self, dt):
        x = self.state['x'].value
        r = self.parameters['rate_of_change'].value
        self._next_state['x'].value = x + r * dt


if __name__ == "__main__":
    system = TestIsolatedSystem()
    print(system.state)
    print(str(system))
    # Run the system a bit into the future manually.
    dt = 0.1
    for i in range(10):
        system._calculate_next_state(dt)
        system._transition()
        print(f"x: {system.state['x'].value:{1}.{3}}")
