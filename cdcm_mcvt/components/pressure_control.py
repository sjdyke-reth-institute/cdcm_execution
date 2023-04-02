#~ovn!
"""Digital-twin of MCVT-ECLSS' Pressure Control in CxLang

Author:
    R Murali Krishnan

Date:
    03.30.2023


"""



__all__ = [
    "AirTank",
    "Valve",
    "InletValve",
    "ReliefValve",
    "make_air_tank",
    "make_pressure_valve",
]

from typing import Union

from cdcm import *
from cdcm_abstractions import *

from .types import *




def make_air_tank(name: str, **kwargs) -> AirTank:
    """Make an air tank"""

    with maybe_make_system(name, AirTank, **kwargs) as tank:
        status = make_health_status(
            name="status_air_tank",
            value=0,
            support=(0, 1, 2),
            description=f"Status of {tank.absname}"
        )

        @make_functionality("func_air_tank")
        def fn_func_air_tank(s=status):
            """Functionality of the air tank"""
            if s == 0:
                return 1.
            elif s == 1:
                return 0.5
            else:
                return 0.25

        @make_test("test_status_air_tank")
        def fn_test_status_air_leak(s=status):
            """Test the health status of air tank"""
            if s < 1:
                return 0.
            else:
                return 1.
        
    return tank


def make_pressure_valve(name: str, **kwargs) -> Valve:
    """Make models of pressurizing/relief valves in habitat"""

    if "inlet" in name:
        ValveType = InletValve
    elif "relief" in name:
        ValveType = ReliefValve
    else:
        ValveType = Valve

    with maybe_make_system(name, ValveType, **kwargs) as valve:
        status = make_health_status(
            name="status_valve",
            value=0,
            support=(0, 1, 2),
            description=f"Status of :{valve.absname}"
        )

        @make_functionality("func_valve")
        def fn_func_valve(s=status):
            if s in [0, 1]:
                return 1.0
            else:
                return 0.0
            
        @make_test("test_status_valve")
        def test_status_air_tank(s=status):
            """Status of the pressure valve"""
            if s == 0:
                return 1.
            else:
                return 0.

    return valve


