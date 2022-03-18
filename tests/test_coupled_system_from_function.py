"""Test a coupled system made out of functions.

Author:
    Ilias Bilionis

Date:
    3/15/2022
"""


from cdcm import *


def trans_func_1(dt, *, x1, r1):
    """A simple transition function for an isolated system."""
    new_x1 = x1 + r1 * dt
    new_state = {'x1': new_x1}
    return new_state


def trans_func_2(dt, *, x2, x1, r2, c):
    """Another simple transition function."""
    new_x2 = x2 + r2 * dt + c * x1 * dt
    return {'x2': new_x2}


if __name__ == "__main__":
    sys1 = SystemFromFunction(
        name="system_1",
        state=PhysicalStateVariable(value=0.1, units="meters", name="x1"),
        parameters=Parameter(value=1.2,
                             units="meters / second",
                             name="r1",
                             description="The rate of change."),
        transition_func=trans_func_1
    )
    sys2 = SystemFromFunction(
        name="system_2",
        state=PhysicalStateVariable(value=0.3, units="meters", name="x2"),
        parameters=[Parameter(value=1.2,
                              units="meters / second",
                              name="r2",
                              description="The rate of change."),
                    Parameter(value=0.1,
                              units="1 / second",
                              name="c",
                              description="The coupling coefficient.")],
        parents={'x1': sys1},
        transition_func=trans_func_2
    )
    sys = SystemOfSystems(name="combined_system", sub_systems=[sys1, sys2])
    print(sys)
    dt = 0.1
    for i in range(10):
        sys.unsafe_step(dt)
        print(f"x1: {sys.state['x1'].value:{1}.{3}},"
              + f"x2: {sys.state['x2'].value:{1}.{3}}")
