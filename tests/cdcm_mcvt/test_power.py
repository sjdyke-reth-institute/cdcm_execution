#!ovn!
"""Test a model of the power-systems in MCVT

Author:
    R Murali Krishnan
    
Date:
    03.30.2023
    
"""

from cdcm import *
from cdcm_mcvt import *
from cdcm_utils import *


with System(name="power") as ps:
    # clock system
    clock = make_clock(dt=1.0, units="hr")

    # Step-up converters
    step_up_converter = make_power_converter("step_up_converter")

    # Step-down converters
    step_down_converter = make_power_converter("step_down_converter")

    # Generation bus
    gen_bus = make_generation_bus("gen_bus")

    # Energy storage/Batteries
    batteries = make_energy_storage("batteries")

    # Solar power generation
    solar = make_power_generator("solar")

    # Nuclear power generation
    nuclear = make_power_generator("nuclear")

    # Make the whole power system
    power_system = make_power_system("power_system")


print(ps)
print("!0vn!")

ps_interactive = make_pyvis_graph(ps, "test_power.html")
print("fin.")
