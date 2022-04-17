"""Tests the functionality of the System class for a simple isolated system.

Author:
    Ilias Bilionis
    Murali Krishnan R

Date:
    3/14/2022

"""


from cdcm import *


x = make_node("S:x:0.1:meters", description="The state of the system.")
r = make_node("P:r:1.2:meters/second", description="The rate of change.")
dt = make_node("P:dt:0.1:second", description="The timestep.")

@make_function(x)
def f(x=x, r=r, dt=dt):
    """The transition function."""
    return x + r * dt

sys = System(
    name="sys",
    nodes=[x, r, dt, f],
    description="An isolated system."
)

print(sys)

print("Run this forward:")
for i in range(10):
    sys.forward()
    sys.transition()
    print(f"x: {sys.x.value:1.2f}")

# Another way to do exactly the same thing is this:
x = make_node("S:x:0.1:meters", description="The state of the system.")
r = make_node("P:r:1.2:meters/second", description="The rate of change.")
dt = make_node("P:dt:0.1:second", description="The timestep.")

@make_system
def sys(x=x, r=r, dt=dt):
    """A simple system."""
    return x + r * dt

print(sys)

print("Run this forward:")
for i in range(10):
    sys.forward()
    sys.transition()
    print(f"x: {sys.x.value:1.2f}")