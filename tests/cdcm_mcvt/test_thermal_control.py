#ovn!
"""Test constructors and selectors of thermal control

author:
    R Murali Krishnan

date:
    03.25.2023

"""


from pprint import pprint

from cdcm import *
from cdcm_mcvt import *
from cdcm_utils import *


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

    # Pump
    pump = make_pump("pump")

    # Radiator Panels
    radiator_panels = make_radiator_panels("panels")

    # Radiator
    radiator = make_radiator("radiator")

    # Fan
    fan = make_fan("fan")

    # Heater
    heater = make_heater("heater")

print("!ovn!")
sys.forward()

pprint(vars(sys))

sys = make_pyvis_graph(sys, "test_thermal_control.html")

print("fin.")