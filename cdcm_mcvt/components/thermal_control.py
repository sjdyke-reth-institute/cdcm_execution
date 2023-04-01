#!ovn!
"""Digital-twin of MCVT-ECLSS' Thermal Comfort controller in CxLang

Describes multi-stage vapor-compression cycle: 
    https://en.wikipedia.org/wiki/Vapor-compression_refrigeration

author:
    R Murali Krishnan

date:
    03.30.2023

"""

__all__ = [
    "make_compressor", 
    "make_condenser",
    "make_evaporator",
    "make_expansion_valve",
    "make_heat_pump",
    "make_radiator",
    "make_pump",
    "make_fan",
    "make_heater",
]

import numpy as np
from typing import Optional, Union

from cdcm import *
from cdcm_abstractions import *

from .types import *

Scalar = Union[int, float]

# Let us first make models of systems to think about "value"
# Let us first make models of cost
def make_controlleable_zone(name: str,
                            /,
                            pressure_setpoint: Scalar,
                            temperature_setpoint: Scalar,
                            *,
                            pressure_setpoint_units: str="bar",
                            temperature_units: str="degC",
                            **kwargs) -> System:
    """A model of a controlleable zone"""


    with maybe_make_system(name, **kwargs) as zone:
          press_setpoint = Parameter(
               name="pressure_setpoint",
               value=pressure_setpoint,
               units=pressure_setpoint_units,
               description="User-defined set-points"
          )

          pass

    # return zone
    raise NotImplementedError("Implement me..")


def make_compressor(name: str, 
                    dt: Node, 
                    operating_cost=100,
                    oil_life: Scalar=1.*365*24, 
                    time_units: str="hr", 
                    **kwargs
    ) -> Compressor:
    """Make a compressor module"""

    # _Compressor = Compressor if isinstance(name, str) else maybe_make_system
    with maybe_make_system(name, Compressor, **kwargs) as compressor:
        status = make_health_status(
            name="status_compressor",
            value=0,
            support=(0, 1)
        )
        test = Test(
            name="test_status_compressor",
            value=0.,
            description="Test for the compressor"
        )
        @make_function(test)
        def calc_test_status_compressor(s=status):
            if s == 0:
                return 0.
            else:
                return 1.
        # life_of_oil = State(
        #     name="life_of_oil",
        #     value=0.,
        #     units=time_units,
        #     description="Life of the oil"
        # )
        # @make_function(life_of_oil)
        # def calc_life_of_oil(lo=life_of_oil, step_time=dt):
        #     """Calculate the life of oil"""
        #     return lo + step_time
        
        # # virtual logical operation
        # pr_breakdown = Variable(
        #     name="pr_breakdown",
        #     value=0.1,
        #     description="Probability of breaking down | status, and life_of_oil"
        # )
        # @make_function(pr_breakdown)
        # def calc_probability_of_breakdown(_status=status, _loil=life_of_oil):
        #     """Calculate probability of breakdown"""
        #     if _loil > oil_life or (not (_status == 0)):
        #         return 0.9
        #     else:
        #         return 0.1
            
        # cost = Variable(
        #     name="cost",
        #     value=0.,
        #     description="Cost of operating asset"
        # )
        # @make_function(cost)
        # def calc_cost_function(pr=pr_breakdown):
        #     """Calculate the operational cost"""
        #     rnd = np.random.rand()
        #     if rnd < pr:
        #         return 100. * operating_cost
        #     else:
        #         return operating_cost
    return compressor

def make_condenser(name: str, **kwargs) -> Condenser:
    """Make the model of MCVT's condensing heat-exchanger in ECLSS"""

    with maybe_make_system(name, Condenser, **kwargs) as chx:
        status_coil = make_health_status(
            name="status_coil",
            value=0,
            support=(0, 1, 2),
            description="Status of heat-exchanging coils in Condenser"
        )
        test_coil = Test(
            name="test_coil",
            value=0.,
            description="Test results from the coil"
        )
        @make_function(test_coil)
        def calc_test_consenser_coil(s=status_coil):
            if s == 0.:
                return 0.
            else:
                return 

    return chx

def make_evaporator(name: str, **kwargs) -> Evaporator:
    """Make the model of MCVT's evaporating heat-exchanger in ECLSS"""

    with maybe_make_system(name, Evaporator, **kwargs) as ehx:
        coil_status = make_health_status(
            name="coil_status",
            value=0,
            support=(0, 1, 2),
            description="Status of heat-exchanging coils in Evaporator"
        )
        leak_status = make_health_status(
            name="leak_status",
            value=0,
            support=(0, 1, 2),
            description="Status variable indicating the presence of leak in Evaporator"
        )
    return ehx

def make_expansion_valve(name: str, **kwargs) -> TXValve:
    """Make the model of a thermo-static expansion valve"""

    with maybe_make_system(name, TXValve, **kwargs) as txv:
        status = make_health_status(
            name="status",
            value=0,
            support=(0, 1, 2),
            description=""
        )
    return txv

def make_heat_pump(name: str, dt: Node, **kwargs) -> HeatPump:
    """Make the heat pump loop"""

    with maybe_make_system(name, HeatPump, **kwargs) as heat_pump:

        compressor = make_compressor(
            name="compressor",
            dt=dt,
            **kwargs)
        
        # Evaporator heat-exchange system
        evaporator = make_evaporator("evaporator")

        # Condenser heat-exchange system
        condenser = make_condenser("condenser")

        # Thermo-static expansion valve
        txvalve = make_expansion_valve("tx_valve")
    return heat_pump

def make_radiator(name: str, **kwargs) -> Radiator:
    """Make the radiator for ECLSS' Thermal Control System"""
    with maybe_make_system(name, Radiator, **kwargs) as radiator:
        paint_status = make_health_status(
            name="paint_status",
            value=0,
            support=(0, 1, 2),
            description="Status of the reflective paint"
        )
        dust_status = make_health_status(
            name="dust_status",
            value=0,
            support=(0, 1, 2),
            description="Status of dust-related performance loss of radiator"
        )
    return radiator

def make_pump(name: str, **kwargs) -> Pump:
    """Make model of a pump"""
    with maybe_make_system(name, Pump, **kwargs) as pump:
        status = make_health_status(
            name="status",
            value=0,
            support=(0, 1, 2),
            description="Status of operation of the pump"
        )
    return pump

def make_heater(name: str, **kwargs) -> Heater:
    """Make a model of the heater"""

    with maybe_make_system(name, Heater, **kwargs) as heater:
        status = make_health_status(
            name="status",
            value=0,
            support=(0, 1, 2),
            description="Overall status of the heater variable"
        )
    return heater

def make_fan(name: str, filter: bool=True, **kwargs) -> Fan:
    """Make a fan system"""

    with maybe_make_system(name, Fan, **kwargs) as fan:
        status = make_health_status(
            name="status",
            value=0,
            support=(0, 1, 2),
            description="Overall health status of fan"
        )
        filter_status = make_health_status(
            name="filter_status",
            value=0,
            support=(0, 1, 2),
            description="Status of the filter of the fan"
        )
    return fan

