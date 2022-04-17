"""Test the case of doubly coupled systems.

Author:
    Ilias Bilionis

Date:
    3/15/2022

"""


from cdcm import *
import numpy as np
from pyvis.network import Network


# ****************************
# System 0
# ****************************
clock = make_clock(0.1)


# ****************************
#       SYSTEM 1
# ****************************

# Notice how this system has a parent that we haven't defined yet
#@make_system
#def sys1(dt, *, x1=x1, x2=None, r1=r1, c1=c1):
#    """A system that has a parent that hasn't yet been defined."""
#   return x1 + r1 * dt + c1 * x2 * dt

x1 = make_node("S:x1:0.1:meters", description="State of sys1.")
r1 = make_node("P:r1:1.2:meters/second", description="Rate parameter for sys1.")
c1 = make_node("P:c1:0.1:1/meters/second", description="Coupling coefficient.")
s1 = make_node(
    "P:s1:0.01:meters",
    description="Standard deviation of measurement noise"
)
y1 = make_node("V:y1", units="meters", description="Sensor measurement sys1.")

# This is a placeholder node useed to establish the connection between
# the two systems:
placeholder = make_node("V:placeholder", units="meters", description="Input from sys2.")

@make_function(x1)
def f1(x1=x1, r1=r1, c1=c1, x2=placeholder, dt=clock.dt):
    """Transition function for sys1."""
    return x1 + r1 * dt + c1 * x2 * dt

@make_function(y1)
def g1(x1=x1, s1=s1):
    """Emission function for sys1."""
    return x1 + s1 * np.random.randn()

# You do not have to put the placeholder node in the system nodes
sys1 = System(
    name="sys1",
    nodes=[x1, r1, c1, f1, s1, y1, g1]
)

# ****************************
#       SYSTEM 2
# ****************************

x2 = make_node("S:x2:0.3:meters")
r2 = make_node("P:r2:1.2:meters/second",)
c2 = make_node("P:c2:20.1:1/second")
s2 = make_node(
    "P:s2:0.01:meters",
    description="Standard deviation of measurement noise"
)
y2 = make_node("V:y2", units="meters", description="Sensor measurement sys2.")


@make_function(x2)
def f2(x2=x2, x1=sys1.x1, r2=r2, c2=c2, dt=clock.dt):
    """Another simple system."""
    return x2 + r2 * dt + c2 * x1 * dt

@make_function(y2)
def g2(x2=x2, s2=s2):
    """Emission function for sys2."""
    return x2 + s2 * np.random.randn()

sys2 = System(
    name="sys2",
    nodes=[x2, r2, c2, f2, s2, y2, g2]
)

# ****************************
#   CONNECT SYSTEMS
# ****************************
replace_node(placeholder, x2)

# ****************************
#       COMBINED SYSTEM
# ****************************

sys = System(
    name="combined_system",
    nodes=[clock, sys1, sys2]
)

print(sys)

# ****************************
#       DRAW THE DAG
# ****************************
g = sys.dag
net = Network(notebook=True, directed=True)
net.from_nx(g)
net.show("double_coupled.html")

# ****************************
#       RUN FORWARD
# ****************************

for i in range(10):
    sys.forward()
    print(f"y1: {sys1.y1.value:1.2f}, y2: {sys2.y2.value:1.2f}")
    sys.transition()
