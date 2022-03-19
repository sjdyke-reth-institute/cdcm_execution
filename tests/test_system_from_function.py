"""Test the SystemFromFunction class.

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
        state=PhysicalStateVariable(
            value=0.1,
            units="meters",
            name="x"
        ),
        parameters=Parameter(
            value=1.2,
            units="meters / second",
            name="r"
        ),
        transition_func=transition_func
    )
    print(sys)
    dt = 0.1
    for i in range(10):
        sys.unsafe_step(dt)
        print(f"x: {sys.state['x']}")
