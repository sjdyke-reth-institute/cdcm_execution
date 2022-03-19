"""Test the SimulationSaver class on a simple system.

Author:
    Ilias Bilionis

Date:
    3/15/2022

"""


from cdcm import *


def transition_func(dt, *, x, r):
    """A simple transition function for an isolated system.

    Please do use * in the definition.
    It ensures that the user specifies all the arguments correclty.
    """
    new_x = x + r * dt
    new_state = {'x': new_x}
    return new_state


if __name__ == "__main__":
    sys = SystemFromFunction(
        name="system",
        state=PhysicalStateVariable(0.1, "meters", "x"),
        parameters=Parameter(1.2, "meters / second", "r"),
        transition_func=transition_func
    )
    print(sys)
    saver = SimulationSaver("test.h5", sys)
    dt = 0.1
    for i in range(10):
        sys.unsafe_step(dt)
        print(f"x: {sys.state['x'].value:{1}.{3}}")
        saver.save(sys)
