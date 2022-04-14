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


# This is the fast way to make a transition function
@make_transition(x)
def f(x=x, r=r, dt=dt):
    """A simple transition function."""
    return x + r * dt

# Print the entire computational graph
print(yaml.dump(x.to_yaml(), sort_keys=False))
print(yaml.dump(r.to_yaml(), sort_keys=False))
print(yaml.dump(dt.to_yaml(), sort_keys=False))
print(yaml.dump(f.to_yaml(), sort_keys=False))

# Test the transition
print("State before:")
print(yaml.dump(x.to_yaml(), sort_keys=False))
print("Evaluating the next step.")
f.forward()
x.transition()
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

@make_transition(x1, x2)
def g(x1=x1, x2=x2, r=r, dt=dt):
    """This is another transition function."""
    return (
        x1 + r * dt,
        x2 + x1 * dt
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
g.forward()
x1.transition()
x2.transition()
print("State after:")
print(yaml.dump(x1.to_yaml(), sort_keys=False))
print(yaml.dump(x2.to_yaml(), sort_keys=False))