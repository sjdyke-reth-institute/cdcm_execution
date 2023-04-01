#ovn!
"""Digital-twin of MCVT's Power System in `exlang`

Author:
    R Murali Krishnan
    
Date:
    03.30.2023
    
"""

__all__ = [
    "make_power_converter",
    "make_energy_storage",
    "make_batteries",
    "make_generation_bus",
    "make_power_generator",
    "make_nuclear_generator",
    "make_solar_arrays",
    "make_power_system"
    ]

from cdcm import *
from cdcm_abstractions import *

from .types import *
from ..abstractions import *

from typing import Union
from collections import defaultdict


def make_power_converter(name: str, **kwargs) -> PowerConverter:
    """Make power converter system"""
    with maybe_make_system(name, PowerConverter, *kwargs) as converter:
        status = make_health_status(
            name="status",
            value=0,
            support=(0, 1, 2),
            description="Status variable of the power converter"
        )

    return converter

def make_energy_storage(name: str, **kwargs) -> EnergyStorage:
    """Make an energy storage system"""
    with maybe_make_system(name, EnergyStorage, **kwargs) as storage:
        status = make_health_status(
            name="status",
            value=0,
            support=(0, 1, 2),
            description="Health status variable of the energy storage"
        )
    return storage

def make_batteries(name: str, num_cells: int, **kwargs):
    """Make battery system"""

    with make_energy_storage(name, **kwargs) as batteries:
        status_cells = make_health_status(
            name="status",
            value=[0] * num_cells,
            support=(0, 1, 2),
            description="Status of each cell of the battery"
        )
    return batteries

def make_generation_bus(name: str, **kwargs) -> GenerationBus:
    """Make the generation bus"""
    with maybe_make_system(name, GenerationBus, **kwargs) as bus:
       status = make_health_status(
           name="status",
           value=0,
           support=(0, 1, 2),
           description="Status variable for the generation bus"
       )

    return bus

def make_power_generator(name: str, **kwargs) -> PowerGenerator:
    """Make the power generator system"""
    with maybe_make_system(name, PowerGenerator, **kwargs) as generator:
        status = make_health_status(
            name="status",
            value=0,
            support=(0, 1, 2),
            description="Health status variable of the power generator"
        )
    return generator

def make_nuclear_generator(name: str, **kwargs) -> System:
    """Make a nuclear generator system"""
    with make_power_generator(name, **kwargs) as nuclear:
        status_dust = make_health_status(
            name="status_dust",
            value=0,
            support=(0, 1, 2),
            description="Health status variable indicating the dust despoition on generator panels"
        )

        status_paint = make_health_status(
            name="status_paint",
            value=0,
            support=(0, 1, 2),
            description="Health status variable indicating the paint degradation to the generator panels"
        )

    return nuclear

def make_solar_arrays(name: str, **kwargs) -> System:
    """Make solar arrays"""
    with make_power_generator(name, **kwargs) as solar_arrays:

        status_dust = make_health_status(
            name="status_dust",
            value=0,
            support=(0, 1, 2),
            description="Health status variable indicating the deposition of dust on the solar arrays"
        )

        status_mechanical = make_health_status(
            name="status_mechanical",
            value=0,
            support=(0, 1, 2),
            description="Health status indicating the mechanical health status of solar arrays"
        )

    return solar_arrays

def make_power_system(
        name: str, 
        num_step_up_converters: int=3,
        num_step_dn_converters: int=3,
        **kwargs) -> PowerSystem:
    """Make the power system"""

    with maybe_make_system(name, PowerSystem, **kwargs) as power_sys:

        # Batteries
        batteries = make_energy_storage("batteries")

        # Power Generators
        solar = make_solar_arrays("solar")

        nuclear = make_nuclear_generator("nuclear")

        # Step-up converters
        for i in range(num_step_up_converters):
            step_up_converter = make_power_converter("step_up_converter_" + str(i + 1))
            power_sys.converters["step_up"].append(step_up_converter)

        # Step-down converters
        for i in range(num_step_dn_converters):
            step_down_converter = make_power_converter("step_dn_converter_" + str(i + 1))
            power_sys.converters["step_down"].append(step_down_converter)
        
        # Generatrion Bus 
        gen_bus = make_generation_bus("gen_bus")

    return power_sys