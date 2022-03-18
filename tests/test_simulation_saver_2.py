"""Tests the functionality of the SystemOfSystems class for a simple isolated system.

Author:
    Ilias Bilionis

Date:
    3/14/2022

"""


from cdcm import *


class Sys1(System):

    def __init__(self):
        name = "system_1"
        state = [PhysicalStateVariable(
                    value=0.1,
                    units="meters",
                    name="x",
                    track=True, 
                    description="The x variable."
                 ),
                 HealthStateVariable(
                    value=0,
                    units="", 
                    name="h",
                    track=True,
                    description="The h variable.")
                ]
        parameters = Parameter(
                        value=1.2,
                        units="meters / second",
                        name="rate_of_change",
                        description="The rate of change."
                     )
        super().__init__(name=name, state=state, parameters=parameters,
                         description="A simple system.")

    def _calculate_next_state(self, dt):
        x = self.state['x1'].value
        r = self.parameters['rate_of_change'].value
        self._next_state['x1'].value = x + r * dt


class Sys2(System):

    def __init__(self, sys_1):
        name = "system_2"
        state = PhysicalStateVariable(
                    value=0.3, 
                    units="meters",
                    name="x2",
                    track=True, 
                    description="The x2 variable."
                )
        parameters = [Parameter(
                        value=1.2,
                        units="meters / second",
                        name="rate_of_change_2",
                        description="The rate of change 2."
                      ),
                      Parameter(
                        value=0.1, 
                        units="1 / second", 
                        name="coupling_coeff",
                        description="Coupling coeff."
                      )
                     ]
        parents = {'x1': sys_1}
        super().__init__(name=name, state=state, parameters=parameters, parents=parents,
                         description="Another simple system.")

    def _calculate_next_state(self, dt):
        # Get the parent variable
        x1 = self.get_parent_state('x1').value
        # Get the variables form here
        x2 = self.state['x2'].value
        r2 = self.parameters['rate_of_change_2'].value
        c = self.parameters['coupling_coeff'].value
        self._next_state['x2'].value = x2 + r2 * dt + c * x1 * dt


if __name__ == "__main__":
    # Create the systems
    sys1 = Sys1()
    sys2 = Sys2(sys1)
    # Put them in a system of system container
    sys = SystemOfSystems(
            name="combined_system", 
            sub_systems=[sys1, sys2]
          )
    print(sys)
    saver = SimulationSaver("test_2.h5", sys)
    # Run the system a bit into the future manually.
    dt = 0.1
    for i in range(10):
        sys.unsafe_step(dt)
        print(f"x1: {sys.state['x1'].value:{1}.{3}}, x2: {sys.state['x2'].value:{1}.{3}}")
        saver.save(sys)