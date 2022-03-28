"""Test the SimulationSaver class on a simple system.

Author:
    Ilias Bilionis

Date:
    3/15/2022


TODO: Use context to make saving safe.

"""


from cdcm import *


# Make a simple system

@make_system
def sys(
    dt,
    *,
    x=PhysicalStateVariable(0.1, "meters", "x"),
    r=Parameter(1.2, "meters / second", "r")
):
    """A simple system."""
    return x + r * dt


# Make a simulation saver object

saver = SimulationSaver("test.h5", sys)


# Simulate for a while

dt = 0.1
for i in range(10):
    sys.unsafe_step(dt)
    print(f"x: {sys.state['x'].value:{1}.{3}}")
    saver.save(sys)
