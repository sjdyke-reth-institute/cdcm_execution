"""Tests the functionality of the System class for a simple isolated system.

Author:
    Ilias Bilionis
    Murali Krishnan R

Date:
    3/14/2022

"""


from cdcm import (System,
                  Parameter,
                  PhysicalStateVariable,
                  HealthStateVariable)


class IsolatedSystem(System):

    def __init__(self):
        name = "Isolated System"
        state = [
            PhysicalStateVariable(value=0.1,
                                  units="meters",
                                  name="x",
                                  track=True,
                                  description="The x variable."),
            HealthStateVariable(value=0,
                                units="",
                                name="h",
                                track=True,
                                description="The h variable.")
        ]
        parameters = Parameter(value=1.2,
                               units="meters / second",
                               name="rate_of_change",
                               description="The rate of change.")
        super().__init__(
            name=name,
            state=state,
            parameters=parameters,
            description="A simple isolated system."
        )

    def _calculate_my_next_state(self, dt):
        x = self.state['x'].value
        r = self.parameters['rate_of_change'].value
        self._next_state['x'].value = x + r * dt


if __name__ == "__main__":
    system = IsolatedSystem()
    print(system.state)
    print(str(system))
    # Run the system a bit into the future manually.
    dt = 0.1
    for i in range(10):
        system.unsafe_step(dt)
        print(f"x: {system.state['x']}")
