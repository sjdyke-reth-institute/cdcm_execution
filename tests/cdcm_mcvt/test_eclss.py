#~ovn!
"""Test the model of the ECLSS in MCVT-NRH

Author:
    R Murali Krishnan

Date:
    03.30.2023

"""

from cdcm import *
from cdcm_mcvt import *
from cdcm_utils import *



with System(name="nrh") as nrh:

    # Make clock
    clock = make_clock(dt=1., units="hr")

    # Make active pressure control
    press_control = make_active_pressure_control("press_control", 2)

    # Make active cooling system
    cooling_system = make_active_cooling_system("cooling_system", clock.dt)

    # Modularized environment control
    env_control = make_environment_control_system("eclss", clock.dt, 2)


print("!ovn!")

print(nrh)

nrh_interactive = make_pyvis_graph(nrh, "test_eclss.html")

print("fin.")

