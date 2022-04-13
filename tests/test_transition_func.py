"""Test the transition function.


Author:
    Ilias Bilionis

Date:
    4/12/2022

"""


from cdcm import *
import yaml


print("TEST 1")
print("*" * 80)

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

# Now let's test a transition function that updates two states at the
# same time
print("TEST 2")
print("*" * 80)
x1 = State(
    name="x1",
    value=1.0,
    units="m"
)
x2 = State(
    name="x2",
    value=2.0,
    units="m"
)
g = TransitionFunction(
    name="g",
    parents=[x1, x2, r, dt],
    children=[x1, x2],
    transition_func=lambda *, x1, x2, r, time_step: (
        x1 + r * time_step,
        x2 + x1 * time_step
    )
)
# Print the entire computational graph
print(yaml.dump(x1.to_yaml(), sort_keys=False))
print(yaml.dump(x2.to_yaml(), sort_keys=False))
print(yaml.dump(r.to_yaml(), sort_keys=False))
print(yaml.dump(dt.to_yaml(), sort_keys=False))
print(yaml.dump(g.to_yaml(), sort_keys=False))

# Test the transition
print("State before:")
print(yaml.dump(x1.to_yaml(), sort_keys=False))
print(yaml.dump(x2.to_yaml(), sort_keys=False))
print("Evaluating the next step.")
g()
x1._transition()
x2._transition()
print("State after:")
print(yaml.dump(x1.to_yaml(), sort_keys=False))
print(yaml.dump(x2.to_yaml(), sort_keys=False))