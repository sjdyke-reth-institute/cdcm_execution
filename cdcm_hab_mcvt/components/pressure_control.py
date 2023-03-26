"""Digital-twin of MCVT-ECLSS' Pressure Control in CxLang

Author:
    R Murali Krishnan

Date:
    03.25.2023


"""



from typing import Union

from cdcm import *
from cdcm_diagnostics import *

from ..abstractions import *


# Sub-system types in ECLSS
class AirTank(System):
    pass
class Valve(System):
    pass

class InletValve(Valve):
    pass

class ReliefValve(Valve):
    pass

def make_air_tank(name: str, **kwargs) -> AirTank:
    """Make an air tank"""

    with AirTank(name=name) as tank:
        status = make_health_status(
            name="status",
            value=0,
            support=(0, 1),
            description=f"Status of {tank.absname}"
        )

    return tank


def make_pressure_valve(name: str, **kwargs) -> Valve:
    """Make models of pressurizing/relief valves in habitat"""

    if "inlet" in name:
        _Valve = InletValve
    elif "relief" in name:
        _Valve = ReliefValve
    else:
        _Valve = Valve

    with _Valve(name=name, **kwargs) as valve:
        status = make_health_status(
            name="status",
            value=0,
            support=(0, 1, 2),
            description=f"Status of :{valve.absname}"
        )
    return valve


def make_active_pressure_control(
        name_or_system: Union[str, System], 
        num_zones: int,
        **kwargs) -> System:
    """Make an active pressure control module"""

    with maybe_make_system(name_or_system, **kwargs) as press_control:
        # Air tank
        air_tank = make_air_tank("air_tank")

        # Valves 
        # press_control.inlet_valves = []
        # press_control.relief_valves = []

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
        def calc_cost_function(iv_status=status_inlet_valves, ov_status=status_outlet_valves):
            """Simple cost function"""
            if all([iv_status, ov_status]):
                return 100.
            elif any([iv_status, ov_status]):
                return 150.
            else:
                return 300.
    return press_control


def make_active_thermal_control():
    """Active thermal control module"""
    raise NotImplementedError("Implement me..")