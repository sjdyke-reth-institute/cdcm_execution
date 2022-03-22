"""Test the power generator class.

Author:
    Ilias Bilionis

Date:
    3/21/2022

"""


from cdcm import *


power_gen = DummyPowerGenerator()
print(power_gen)

dt = 0.1
for i in range(10):
    power_gen.unsafe_step(dt)
    print(f"generated power: {power_gen.state['power_output']}")
