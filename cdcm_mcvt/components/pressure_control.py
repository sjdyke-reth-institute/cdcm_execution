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
        test = Test(
            name="test_air_tank",
            value=0.,
            description=f"Test for of air tank {tank.absname}"
        )
        @make_function(test)
        def calc_status_air_tank(s=status):
            """Status of the air tank"""
            if s == 0:
                return 1.
            else:
                return 0.
    return tank


def make_pressure_valve(name: str, **kwargs) -> Valve:
    """Make models of pressurizing/relief valves in habitat"""

    if "inlet" in name:
        _Valve = InletValve
    elif "relief" in name:
        _Valve = ReliefValve
    else:
        _Valve = Valve

    with maybe_make_system(name, _Valve, **kwargs) as valve:
        status = make_health_status(
            name="status_valve",
            value=0,
            support=(0, 1, 2),
            description=f"Status of :{valve.absname}"
        )
        test = Test(
            name="test_valve",
            value=0.,
            description=f"Test for the pressure value"
        )
        @make_function(test)
        def test_status_air_tank(s=status):
            """Status of the pressure valve"""
            if s == 0:
                return 1.
            else:
                return 0.

    return valve


