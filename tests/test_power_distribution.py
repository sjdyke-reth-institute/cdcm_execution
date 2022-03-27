"""Test the power distribution system.

Author:
    Ilias Bilionis

Date:
    3/27/2022

"""


from cdcm import *


g1 = DummyPowerGenerator(
    name="solar",
    nominal_power_output=5.0
)
g2 = DummyPowerGenerator(
    name="nuclear",
    nominal_power_output=10.0
)

c1 = DummyPowerConsumer(
    name="pressure_system",
    nominal_required_power=12.0
)
c2 = DummyPowerConsumer(
    name="thermal_control_system",
    nominal_required_power=3.0
)

d = PowerDistributionSystem()
d.connect_generator(g1)
d.connect_generator(g2)
d.connect_consumer(c1)
d.connect_consumer(c2)

ps = System(
    name="power_system",
    sub_systems=[d, g1, g2]
)

hs = System(
    name="habitat_system",
    sub_systems=[ps, c1, c2]
)

print("*** HABITAT SYSTEM ***")
print(hs)
print("*" * 20)

# Do a few steps:
dt = 1.0
for i in range(5):
    hs.unsafe_step(dt)
    print(f"generated power {d.generated_power},"
          + f" required power {d.required_power}")
