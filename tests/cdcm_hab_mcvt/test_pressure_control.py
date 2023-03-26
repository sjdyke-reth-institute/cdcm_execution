"""Tests for pressure control

Author:
    R Murali Krishnan
    
Date:
    03.25.2023
    
"""

from cdcm import *
from cdcm_hab_mcvt import *

from pprint import pprint


with System(name="nrh") as nrh:
    clock = make_clock(dt=1., units="hr")

    pres_control = make_active_pressure_control("pres_control", 2)

nrh.forward()
print("!0vn!")
# print(pres_control)

# pprint(vars(pres_control))

## -- Sub-systems within the pressure-control

nrh_interactive = show_interactive_graph(nrh, "test_pressure_control.html")

