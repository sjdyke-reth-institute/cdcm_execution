#ovn!
"""Test constructors and selectors of thermal control

author:
    R Murali Krishnan

date:
    03.25.2023

"""


from pprint import pprint

from cdcm import *
from cdcm_hab_mcvt import *


with System(name="sys") as sys:

    clock = make_clock(dt=0.1, units="hr")

    # compressor
    compressor = make_compressor("compressor", clock.dt)

    # Evaporating heat-exchanger
    evaporator = make_evaporator("evaporator")

    # Condensing heat-exchanger
    condenser = make_condenser("condenser")

    # Thermo-static expansion valve
    tx_valve = make_expansion_valve("tx_valve")

    # Heat pump
    heat_pump = make_heat_pump("heat_pump", clock.dt) 

    # Radiator
    radiator = make_radiator("rediator")

    # Pump
    pump = make_pump("pump")

    # Fan
    fan = make_fan("fan")

    # Active thermal control
    atc = make_active_thermal_control("thermal_control")


print("!ovn!")
sys.forward()

pprint(vars(sys))

sys = show_interactive_graph(sys, "test_thermal_control.html")

print("fin.")