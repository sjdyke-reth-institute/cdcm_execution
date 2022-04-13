"""Test the transition function.


Author:
    Ilias Bilionis

Date:
    4/12/2022

"""


from cdcm import *
import yaml


# We will make a simple system with one state first
x = State(
    name="x",
    value=1.0,
    units="m"
)
r = Parameter(
    name="r",
    value=0.1,
    units="1/s"
)
dt = Parameter(
    name="time_step",
    value=0.1,
    units="s"
)

# This is the fully descriptive way to make the transition function.
f = TransitionFunction(
    name="f",
    parents=[x, r, dt],
    children=x,
    transition_func=lambda *, x, r, time_step: x + r * time_step
)

# Print the entire computational graph
print(yaml.dump(x.to_yaml(), sort_keys=False))
print(yaml.dump(r.to_yaml(), sort_keys=False))
print(yaml.dump(dt.to_yaml(), sort_keys=False))
print(yaml.dump(f.to_yaml(), sort_keys=False))

# Test the transition
print("State before:")
print(yaml.dump(x.to_yaml(), sort_keys=False))
print("Evaluating the next step.")
f()
x._transition()
print("State after:")
print(yaml.dump(x.to_yaml(), sort_keys=False))
