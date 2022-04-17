"""Test a coupled system made out of functions.

Author:
    Ilias Bilionis

Date:
    3/15/2022
"""


from cdcm import *

# ****************************
# System 0
# ****************************
clock =

# ****************************
#       SYSTEM 1
# ****************************

x1 = make_node("S:x1:0.1:meters")
r1 = make_node("P:r1:1.2:meters/second")

@make_function
def f1(x1=x1, r1=r1, dt=dt):
    """A simple system."""
    return x1 + r1 * dt

# ****************************
#       SYSTEM 2
# ****************************

x2 = PhysicalStateVariable(
    value=0.3,
    units="meters",
    name="x2"
)

r2 = Parameter(
    value=1.2,
    units="meters / second",
    name="r2",
    description="The rate of change."
)

c = Parameter(
    value=0.1,
    units="1 / second",
    name="c",
    description="The coupling coefficient."
)


@make_system
def sys2(dt, *, x2=x2, x1=(sys1, "x1"), r2=r2, c=c):
    """Another simple system."""
    return x2 + r2 * dt + c * x1 * dt


# ****************************
#       COMBINED SYSTEM
# ****************************

sys = System(name="combined_system", sub_systems=[sys1, sys2])

print(sys)

# ****************************
#       RUN FORWARD
# ****************************

dt = 0.1
for i in range(10):
    sys.unsafe_step(dt)
    print(f"x1: {sys1.state['x1']}, x2: {sys2.state['x2']}")
