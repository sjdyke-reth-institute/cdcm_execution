"""Some tests with decorators.

I am trying to figure out if there is a way to use decorators to
simplify the interface.

Author:
    Ilias Bilionis

Date:
    3/27/2022

"""


from cdcm import *


x1 = PhysicalStateVariable(
    value=0.1,
    units="meters",
    name="x1"
)

r1 = Parameter(
    value=1.2,
    units="meters / second",
    name="r1"
)


@make_system
def sys1(dt, *, x1=x1, r1=r1):
    """A simple system."""
    return x1 + r1 * dt


# Can we do the same thing if we have parents?

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


sys = System(name="combined_system", sub_systems=[sys1, sys2])

print(sys)

dt = 0.1
for i in range(10):
    sys.unsafe_step(dt)
    print(f"x1: {sys1.state['x1']}, x2: {sys2.state['x2']}")
