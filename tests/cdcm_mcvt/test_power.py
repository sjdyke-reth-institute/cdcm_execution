#!ovn!
"""Test the power-systems model

Author:
    R Murali Krishnan
    
Date:
    03.29.2023
    
"""

from cdcm import *
from cdcm_mcvt import *


with System(name="power") as ps:
    # clock system
    clock = make_clock(dt=1.0, units="hr")

    # make a power converters
    step_up_converter = make_power_converter("step_up_converter_1", "U")

    step_down_converter = make_power_converter("step_down_converter_1", "D")


print(ps)
print("!0vn!")

ps_interactive = make_pyvis_graph(ps, "test_power.html")
print("fin.")