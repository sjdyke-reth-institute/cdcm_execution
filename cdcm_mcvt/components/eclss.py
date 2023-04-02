#~ovn!
"""Model of the ECLSS in MCVT-NRH

Author:
    R Murali Krishnan

Date:
    03.30.2023

"""


__all__ = [
    "make_active_pressure_control", 
    "make_active_cooling_system", 
    "make_environment_control_system"
]

from typing import Union

from cdcm import *
from cdcm_abstractions import *

from ..abstractions import *
from .types import *
from .pressure_control import *
from .thermal_control import *


def make_active_pressure_control(
        name_or_system: Union[str, System], 
        num_zones: int,
        **kwargs) -> System:
    """Make an active pressure control module"""

    with maybe_make_system(name_or_system, **kwargs) as press_control:
        
        # Air tank
        air_tank = make_air_tank("air_tank")


        for izone in range(num_zones):
            inlet_valve_name = "inlet_valve_zone" + str(izone + 1)
            inlet_valve = make_pressure_valve(
                name=inlet_valve_name,
                description=f"Status of the inlet valve at Zone ({str(izone + 1)})"
            )

            relief_valve_name = "relief_valve_zone" + str(izone + 1)
            relief_valve = make_pressure_valve(
                name=relief_valve_name,
                description=f"Status of the relief valve at Zone ({str(izone + 1)})"
            )
        
        inlet_valves = press_control.get_subsystems_of_type(InletValve)
        relief_valves = press_control.get_subsystems_of_type(ReliefValve)

        inlet_valve_statuses = [iv.status_valve for iv in inlet_valves]
        relief_valve_statuses = [rv.status_valve for rv in relief_valves]

        # How do we address the following with decorator patterns?
        # @make_functionality("func_pressurizing", _map=True)
        # def fn_func_pressurizing(ivs=inlet_valve_statuses):
        #     """Functionality of pressurizing the habitat"""
        #     return all(ivs)
        #     pass
        func_pressurize = Functionality(
            name="func_pressurize",
            value=0.,
            description="Functionality to pressurize the dome structure"
        )
        fn_func_pressurize = Function(
            name="fn_func_pressurize",
            parents=inlet_valve_statuses,
            children=func_pressurize,
            func=lambda *args: all([arg > 0.5 for arg in args]),
            description="Functionality of pressurizing the habitat"
        )
        func_depresssurize = Functionality(
            name="func_depressurize",
            value=0.,
            description="Functionality to de-pressurize the dome structure"
        )
        fn_func_depressurize = Function(
            name="fn_func_depressurize",
            parents=relief_valve_statuses,
            children=func_depresssurize,
            func=lambda *args: all([arg > 0.5 for arg in args]),
            description="Functionality of de-pressurizing the habitat"
        )

    return press_control

def make_active_cooling_system(
        name_or_system: Union[str, System],
        dt: Node,
        **kwargs
    ) -> System:
    """Make the active cooling system"""

    with maybe_make_system(name_or_system, **kwargs) as atc:


        # Primary heat-exchange loop
        heat_pump = make_heat_pump("heat_pump", dt)

        # Pump for cycling 
        radiator = make_radiator("radiator")

        # fans and filters for active thermal control
        fan_status = make_health_status(
            name="status_fan",
            value=0,
            support=(0, 1, 2),
            description="Status of operation of the fan"
        )
        filter_status = make_health_status(
            name="status_filter",
            value=0,
            support=(0, 1, 2),
            description="Status of filter of active thermal control"
        )
    return atc

def make_environment_control_system(name: str, dt: Node, num_zones: int, **kwargs) -> System:
    """Make model for the ECLSS"""

    with maybe_make_system(name, **kwargs) as eclss:

        pressure_control =  make_active_pressure_control("pressure_control", num_zones)

        cooling_system = make_active_cooling_system("cooling_system", dt)

        heater = make_heater("heater")

    return eclss