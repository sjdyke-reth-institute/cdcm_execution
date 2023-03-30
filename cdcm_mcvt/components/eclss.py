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
from cdcm_diagnostics import *

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
            # inlet_valves.append((inlet_valve_name, inlet_valve))

            relief_valve_name = "relief_valve_zone" + str(izone + 1)
            relief_valve = make_pressure_valve(
                name=relief_valve_name,
                description=f"Status of the relief valve at Zone ({str(izone + 1)})"
            )
            # relief_valves.append((relief_valve_name, relief_valve))
        
        press_control.inlet_valves = press_control.get_subsystems_of_type(InletValve)
        press_control.relief_valves = press_control.get_subsystems_of_type(ReliefValve)

        status_inlet_valves = Test(
            name="status_inlet_valves",
            value=0.,
            description="Status of all inlet valves"
        )
        calc_status_inlet_valves = Function(
            name="fn_status_inlet_valves",
            children=status_inlet_valves,
            parents=[iv.status for iv in press_control.inlet_valves],
            func=lambda *list_of_states: all(s for s in list_of_states),
            description="Calculate the combined status of inlet valves"
        )
        status_outlet_valves = Test(
            name="status_outlet_valves",
            value=0.,
            description="Status of all outlet valves"
        )
        calc_status_outlet_valves = Function(
            name="calc_status_outlet_valves",
            children=status_outlet_valves,
            parents=[rv.status for rv in press_control.relief_valves],
            func=lambda *list_of_states: all(s for s in list_of_states),
            description="Calculate the combined status of outlet valves"
        )
        cost = Variable(
            name="cost",
            value=0.,
            description="Cost of operating pressure control"
        )
        @make_function(cost)
        def calc_cost_function(tank_status=air_tank.status, iv_status=status_inlet_valves, ov_status=status_outlet_valves):
            """Simple cost function"""
            if  all([tank_status, iv_status, ov_status]):
                # All mechanisms are working
                return 100.
            elif ov_status and any([iv_status, tank_status]):
                # Relief mechanism is healthy
                # Pressurizing mechanism has a failure
                return 150.
            else:
                # Problem in relief and pressurizing mechanism
                return 300.
    return press_control

def make_active_cooling_system(
        name_or_system: Union[str, System],
        dt: Node,
        **kwargs
    ) -> System:
    """Make the active cooling system"""

    with maybe_make_system(name_or_system, **kwargs) as atc:

        # Radiator panels for rejecting heat to space
        radiator = make_radiator("radiator")

        # Heat-pump for cooling
        heat_pump = make_heat_pump("heat_pump", dt)

        # Pump for cycling 
        pump = make_pump("pump")

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