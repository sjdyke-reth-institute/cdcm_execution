"""Tests initial conditions.

Author:
    Ilias Bilionis

Date:
    6/16/2022

"""


from cdcm import *
import numpy as np


with System(name="exp_decay", description="A simple oscilator") as sys:
    clock = make_clock(0.01)

    x = State(name="x", value=0.0, units="m",
        description="The position of the oscillator")

    # This sets the transition of the state
    omega = Parameter(name="omega", value=-1.3, units="m/sec",
        description="Decay rate")

    @make_function(x)
    def f(x=x, omega=omega, dt=clock.dt):
        return x - dt * omega * x

print(sys)

# We need a simulator to capture events
simulator = Simulator(sys)

# Let's create some events
# Events are just functions that may change the value
# of some variables

# Event 1:
# This is an event that x at random
@make_function(sys.x)
def random_change_x(t=sys.clock.t):
    new_x = 10 * np.random.rand()
    print(f"*** Event (random_change_x) at time {t:1.2f}, x -> {new_x:1.2f} ***")
    return new_x

# Event 2:
# This is to demonstrate that you can set value
# also in a completly ad hoc manner, i.e., without using the graph
# of CDCM
# Change omega to a given value
def set_omega_to_minus_one():
    print("*** Event (set_omega_to_minus_one ***)")
    sys.omega.value = -1.0

# You can event define event constructors
def change_omega_to(new_value):
    def event():
        print(f"*** Event (change_omega_to({new_value:1.2f})) ***")
        sys.omega.value = new_value
    return event

# It won't do anything, unless you assign it to a specific timestep
# Let's have it run at the first time step
simulator.add_event(0, random_change_x)

simulator.add_event(0.03, set_omega_to_minus_one)

# And also at timestep 10
simulator.add_event(0.05, random_change_x)

simulator.add_event(0.1, change_omega_to(-2.0))

simulator.add_event(0.2, change_omega_to(-3.0))

# Simulate a trajectory
for i in range(30):
    simulator.forward()
    print(f"omega = {sys.omega.value:1.2f}, t = {sys.clock.t.value:1.2f}, "
          + f"x = {sys.x.value:1.2f}, ")
    simulator.transition()
