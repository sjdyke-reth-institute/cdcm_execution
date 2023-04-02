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


def make_compressor(name: str, 
                    dt: Node, 
                    operating_cost=100,
                    oil_life: Scalar=1.*365*24, 
                    time_units: str="hr", 
                    **kwargs) -> Compressor:
    """Make a compressor module"""

    # _Compressor = Compressor if isinstance(name, str) else maybe_make_system
    with maybe_make_system(name, Compressor, **kwargs) as compressor:
        status = make_health_status(
            name="status_compressor",
            value=0,
            support=(0, 1)
        )
        @make_functionality("func_compressor")
        def fn_func_compressor(s=status):
            """Model dependence of functionality on health status"""
            if s == 0:
                return 1.0
            elif s == 1:
                return 0.5
            else:
                return 0.25

        @make_test("test_status_compressor")
        def fn_test_status_compressor(s=status):
            """Model the diagnostic test for compressor from health status"""
            if s < 1:
                return 0.
            else:
                return 1.

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
        @make_functionality("func_condenser")
        def fn_func_condenser_coil(s=status_coil):
            if status_coil == 0:
                return 1.
            else:
                return 0.5
        @make_test("test_status_coil") 
        def fn_test_status_coil(s=status_coil):
            """Test for status coil"""
            return 0. if s < 1 else 1.

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
        @make_functionality("func_evaporator")
        def fn_func_evaporator(cs=coil_status, ls=leak_status):
            """Functionality of the evaporator depending on health status"""
            if (cs < 1) and (ls < 1):
                return 1.
            elif (cs < 2) and (ls <= 1):
                return 0.5
            else:
                return 0.25
        
        # What test does the evaporator have?
        # @make_test(...)
        # def fn_test_evaporator(...)
        #   ...
    return ehx

def make_expansion_valve(name: str, **kwargs) -> TXValve:
    """Make the model of a thermo-static expansion valve"""

    with maybe_make_system(name, TXValve, **kwargs) as txv:
        status = make_health_status(
            name="status_expansion_valve",
            value=0,
            support=(0, 1, 2),
            description=""
        )
        @make_functionality("func_expansion_valve")
        def fn_func_expansion_valve(s=status):
            """Functionality of the expansion valve"""
            return 1. if s < 2 else 0.25
    return txv

def make_radiator_panels(name: str, **kwargs) -> RadiatorPanels:
    """Make the radiator for ECLSS' Thermal Control System"""
    with maybe_make_system(name, RadiatorPanels, **kwargs) as radiator_panels:
        status_paint = make_health_status(
            name="status_paint",
            value=0,
            support=(0, 1),
            description="Status of the reflective paint"
        )
        status_dust = make_health_status(
            name="status_dust",
            value=0,
            support=(0, 1),
            description="Status of dust-related performance loss of radiator"
        )
        @make_functionality("func_radiator_panels")
        def fn_func_radiator_panels(ps=status_paint, ds=status_dust):
            """Calculate the functinoality of radiator panels"""
            if all(not s for s in [ps, ds]):
                return 1.
            elif any(not s for s in [ps, ds]):
                return 0.5
            else:
                return 0.25
            
        @make_test("test_status_paint")
        def fn_test_status_pain(sp=status_paint):
            """Test for the paint status"""
            return 0. if sp < 1 else 1.
        
        @make_test("test_status_dust")
        def fn_test_status_dust(sd=status_dust):
            """Test for the dust status"""
            return 0. if sd < 1 else 1.

    return radiator_panels

def make_pump(name: str, **kwargs) -> Pump:
    """Make model of a pump"""
    with maybe_make_system(name, Pump, **kwargs) as pump:
        status = make_health_status(
            name="status",
            value=0,
            support=(0, 1),
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

def make_heat_pump(name: str, dt: Node, **kwargs) -> HeatPump:
    """Make primary heat-exchanging loop (a heat-pump)"""

    with maybe_make_system(name, HeatPump, **kwargs) as heat_pump:

        # Compressor of the heat-pump
        compressor = make_compressor(name="compressor",dt=dt,**kwargs)
        
        # Evaporator of the heat-pump
        evaporator = make_evaporator("evaporator")

        # Condenser of the heat-pump 
        condenser = make_condenser("condenser")

        # Thermo-static expansion valve of the heat-pump
        txvalve = make_expansion_valve("tx_valve")


        @make_functionality("func_heat_exchange")
        def fn_func_heat_exchange(
            fe=evaporator.func_evaporator,
            fc=condenser.func_condenser):
            """Functionality of heat exchange in the heat-pump"""
            if all([fe, fc]):
                return 1.
            elif any([fe, fc]):
                return 0.5
            else:
                return 0.25
            
        @make_functionality("func_work_in")
        def fn_func_work_in(fc=compressor.func_compressor):
            """Functionality enabled by the compressor"""
            return fc
        
        @make_functionality("func_work_out")
        def fn_func_work_out(ft=txvalve.func_expansion_valve):
            """Functionality to take the work out"""
            return ft
        
        @make_functionality("func_heat_pump")
        def fn_func_heat_pump(
            fhe=heat_pump.func_heat_exchange,
            fwi=heat_pump.func_work_in,
            fwo=heat_pump.func_work_out):
            """Higher-order functionality for heat-pump"""
            if all([fhe, fwi, fwo]):
                return 1.
            else:
                return 0.
        
    return heat_pump

def make_radiator(name: str, **kwargs) -> System:
    """Make the radiator loop"""

    with maybe_make_system(name, System, **kwargs) as radiator:

        # Radiator panels        
        radiator_panels = make_radiator_panels("radiator_panels")

        # Pump
        pump = make_pump("pump")

    return radiator



