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
        state={"x1": PhysicalStateVariable(0.1, "meters", "x1")},
        parameters={"r1": Parameter(1.2, "meters / second", "rate of change")},
        transition_func=trans_func_1)
    sys2 = SystemFromFunction(
        state={"x2": PhysicalStateVariable(0.3, "meters", "x2")},
        parameters={"r2": Parameter(1.2, "meters / second", "rate of change"),
                    "c": Parameter(0.1, "1 / second", "coupling coeff")},
        parents={'x1': sys1},
        transition_func=trans_func_2)
    sys = SystemOfSystems(sub_systems=[sys1, sys2])
    dt = 0.1
    for i in range(10):
        sys.step(dt)
        print(f"x1: {sys.state['x1'].value:{1}.{3}}, x2: {sys.state['x2'].value:{1}.{3}}")