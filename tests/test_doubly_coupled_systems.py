"""Test the case of doubly coupled systems.

Author:
    Ilias Bilionis

Date:
    3/15/2022

"""


from cdcm import *


def trans_func_1(dt, *, x1, x2, r1, c1):
    """A simple transition function for an isolated system."""
    new_x1 = x1 + r1 * dt + c1 * x2 * dt
    new_state = {'x1': new_x1}
    return new_state

def trans_func_2(dt, *, x2, x1, r2, c2):
    """Another simple transition function."""
    new_x2 = x2 + r2 * dt + c2 * x1 * dt
    return {'x2': new_x2}


if __name__ == "__main__":
    # Notice that I do not have the parent of sys1 ready when I am making it:
    sys1 = SystemFromFunction(
        name="system_1",
        state={"x1": PhysicalStateVariable(0.1, "meters", "x1")},
        parameters={"r1": Parameter(1.2, "meters / second", "rate of change"),
                    "c1": Parameter(0.1, "1 / second", "coupling coef 1")},
        transition_func=trans_func_1)
    # So, I have to make the parent:
    sys2 = SystemFromFunction(
        name="system_2",
        state={"x2": PhysicalStateVariable(0.1, "meters", "x2")},
        parameters={"r2": Parameter(0.2, "meters / second", "rate of change"),
                    "c2": Parameter(0.1, "1 / second", "coupling coeff")},
        parents={'x1': sys1},
        transition_func=trans_func_2)
    # and then connect them
    sys1.parents["x2"] = sys2
    # now everything is okay
    sys = SystemOfSystems(name="combined_system", sub_systems=[sys1, sys2])
    print(sys)
    # Run it for a while
    dt = 0.1
    for i in range(10):
        sys.unsafe_step(dt)
        print(f"x1: {sys.state['x1'].value:{1}.{3}}, x2: {sys.state['x2'].value:{1}.{3}}")