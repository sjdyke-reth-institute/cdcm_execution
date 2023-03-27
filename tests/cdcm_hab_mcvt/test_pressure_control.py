#ovn!
"""Tests constructors and selectors of pressure control

Author:
    R Murali Krishnan
    
Date:
    03.25.2023
    
"""

from cdcm import *
from cdcm_hab_mcvt import *

from pprint import pprint


with System(name="system") as sys:

    clock = make_clock(dt=1., units="hr")

    # AirTank
    tank = make_air_tank("supplementary_tank")
    # Valve
    valve = make_pressure_valve("generic_valve")
    
    # MCVT's Pressure controller's model
    pres_control = make_active_pressure_control("pres_control", 2)

    




sys.forward()
print("!0vn!")
# print(pres_control)

# pprint(vars(pres_control))

## -- Sub-systems within the pressure-control

nrh_interactive = show_interactive_graph(sys, "test_pressure_control.html")


# Events with value change
