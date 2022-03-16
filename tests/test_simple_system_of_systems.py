"""Tests the functionality of the SimulationSaver on SystemOfSystems.

Author:
    Ilias Bilionis

Date:
    3/15/2022

"""


from cdcm import *


class Sys1(System):

    def __init__(self):
        name = "system_1"
        state = {"x1": PhysicalStateVariable(0.1, "meters", "x1", track=True, 
                                            description="The x1 variable."),
                 "h": HealthStateVariable(0, None, "x", track=True,
                                          description="The h variable.")}
        parameters = {"rate_of_change": Parameter(1.2, "meters / second",
                                                 "rate_of_change",
                                                 description="The rate of change.")}
        super().__init__(name=name, state=state, parameters=parameters,
                         description="A simple system.")

    def _calculate_next_state(self, dt):
        x = self.state['x1'].value
        r = self.parameters['rate_of_change'].value
        self._next_state['x1'].value = x + r * dt


class Sys2(System):

    def __init__(self, sys_1):
        name = "system_2"
        state = {"x2": PhysicalStateVariable(0.3, "meters", "x2", track=True, 
                                             description="The x2 variable.")}
        parameters = {"rate_of_change_2": Parameter(1.2, "meters / second",
                                                 "rate_of_change_2",
                                                 description="The rate of change 2."),
                      "coupling_coeff": Parameter(0.1, "1 / second", "coupling_coeff",
                                                  description="Coupling coeff.")}
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
    sys = SystemOfSystems(name="combined_system", sub_systems=[sys1, sys2])
    print(sys)
    # Run the system a bit into the future manually.
    dt = 0.1
    for i in range(10):
        sys._calculate_next_state(dt)
        sys._transition()
        print(f"x1: {sys.state['x1'].value:{1}.{3}}, x2: {sys.state['x2'].value:{1}.{3}}")
    # This system of system is closed.
    # So, we can also do this:
    sys1.state['x1'].value = 0.1
    sys2.state['x2'].value = 0.3
    for i in range(10):
        sys.unsafe_step(dt)
        print(f"x1: {sys.state['x1'].value:{1}.{3}}, x2: {sys.state['x2'].value:{1}.{3}}")