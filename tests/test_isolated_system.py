"""Tests the functionality of the System class for a simple isolated system.

Author:
    Ilias Bilionis
    Murali Krishnan R

Date:
    3/14/2022

"""


from cdcm import *


x = PhysicalStateVariable(
    value=0.1,
    units="meters",
    name="x",
    track=True,
    description="The x variable."
)

r = Parameter(
    value=1.2,
    units="meters / second",
    name="r",
    description="The rate of change."
)


@make_system
def sys(dt, *, x=x, r=r):
    return x + r * dt


print(sys)


dt = 0.1
for i in range(10):
    sys.unsafe_step(dt)
    print(f"x: {sys.state['x']}")
