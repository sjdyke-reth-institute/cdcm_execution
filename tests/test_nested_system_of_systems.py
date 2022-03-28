"""Test a nested system of systems.

Author:
    Ilias Bilionis

Date:
    3/15/2022

"""


from cdcm import *

# SYS 1

x1 = PhysicalStateVariable(0.1, "meters", "x1")
r1 = Parameter(1.2, "meters / second", "r1")


@make_system
def sys1(dt, *, x1=x1, r1=r1):
    """A simple system."""
    return x1 + r1 * dt


# SYS 2

x2 = PhysicalStateVariable(0.1, "meters", "x2")
r2 = Parameter(0.2, "meters / second", "r2")
c = Parameter(0.1, "1 / second", "c")


@make_system
def sys2(dt, *, x2=x2, x1=(sys1, "x1"), r2=r2, c=c):
    """Another simple system."""
    return x2 + r2 * dt + c * x1 * dt


# COMBINED SYS 1 & 2
sos1 = System(
    name="combined_system_1",
    sub_systems=[sys1, sys2]
)


# SYS 3

x3 = PhysicalStateVariable(0.1, "meters", "x3")
r3 = Parameter(1.2, "meters / second", "r3")


@make_system
def sys3(dt, *, x3=x3, r3=r3):
    """A third simple system."""
    return x3 + r3 * dt


# SYS 4
x4 = PhysicalStateVariable(0.1, "meters", "x4")
r4 = Parameter(0.2, "meters / second", "r4")
c24 = Parameter(0.1, "1 / second", "c24")


@make_system
def sys4(dt, *, x4=x4, x2=(sys2, "x2"), r4=r4, c24=c24):
    """A forth simple system."""
    return x4 + r4 * dt + c24 * x2 * dt


# COMBINED SYS 3 & 4

sos2 = System(
    name="combined_system_2",
    sub_systems=[sys3, sys4]
)


# All the systems combined
sys = System(
    name="super_system",
    sub_systems=[sos1, sos2]
)


# Print some info

print(sys)


# Simulate for a while

dt = 0.1
for i in range(10):
    sys.unsafe_step(dt)
    print(f"x1: {sys1.state['x1']}, x2: {sys2.state['x2']}"
        + f"x3: {sys3.state['x3']}, x4: {sys4.state['x4']}")
