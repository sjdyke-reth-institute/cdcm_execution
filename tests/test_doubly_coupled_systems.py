"""Test the case of doubly coupled systems.

Author:
    Ilias Bilionis

Date:
    3/15/2022

"""


from cdcm import *

# ****************************
#       SYSTEM 1
# ****************************

x1 = PhysicalStateVariable(0.1, "meters", "r1")
r1 = Parameter(1.2, "meters / second", "r1")
c1 = Parameter(0.1, "1 / second", "c1")


# Notice how this system has a parent that we haven't defined yet
@make_system
def sys1(dt, *, x1=x1, x2=None, r1=r1, c1=c1):
    """A system that has a parent that hasn't yet been defined."""
    return x1 + r1 * dt + c1 * x2 * dt


# ****************************
#       SYSTEM 2
# ****************************

x2 = PhysicalStateVariable(0.1, "meters", "x2")
r2 = Parameter(0.2, "meters / second", "r2")
c2 = Parameter(0.1, "1 / second", "c2")


@make_system
def sys2(dt, *, x2=x2, x1=(sys1, "x1"), r2=r2, c2=c2):
    """A system all the parents of which have been defined."""
    return x2 + r2 * dt + c2 * x1 * dt


# ****************************
#       COMBINED SYSTEM
# ****************************

# Now that awe have coupled the systems, we can establish the
# connection between the parents
sys1.add_parent("x2", sys2)

# Nowe we can make the combined system
sys = System(
    name="combined_system",
    sub_systems=[sys1, sys2]
)

print(sys)

# Run it for a while
dt = 0.1
for i in range(10):
    sys.unsafe_step(dt)
    print(f"x1: {sys1.state['x1']}, x2: {sys2.state['x2']}")
