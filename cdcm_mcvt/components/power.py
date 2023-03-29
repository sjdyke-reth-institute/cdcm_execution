#ovn!
"""Digital-twin of MCVT's Power System in `exlang`

Author:
    R Murali Krishnan
    
Date:
    03.27.2023
    
"""

__all__ = ["make_power_system", "make_power_generator", "make_generation_bus", "make_energy_storage", "make_power_converter"]

from cdcm import *
from cdcm_diagnostics import *

from .types import *
from ..abstractions import *

from typing import Union


def make_power_converter(name: str, **kwargs):
    return maybe_make_system(name, PowerConverter, **kwargs)

def make_energy_storage(name: str, **kwargs):
    return maybe_make_system(name, EnergyStorage, **kwargs)

def make_generation_bus(name: str, **kwargs):
    return maybe_make_system(name, GenerationBus, **kwargs)

def make_power_generator(name: str, **kwargs):
    return maybe_make_system(name, PowerGenerator, **kwargs)

def make_power_system(
        name: str, 
        num_step_up_converters: int=3,
        num_step_dn_converters: int=3,
        **kwargs) -> System:
    """Make the power system"""

    with System(name=name, **kwargs) as power_sys:

        # Power Generators
        solar = make_power_generator("solar")

        nuclear = make_power_generator("nuclear")

        # Power Converters
        power_sys.converters = {}
        # Step-up converters
        power_sys.converters["step_up"] = []
        for i in range(num_step_up_converters):
            step_up_converter = make_power_converter("step_up_converter_" + str(i + 1))
            power_sys.converters["step_up"].append(step_up_converter)

        # Step-down converters
        power_sys.converters["step_down"] = []
        for i in range(num_step_dn_converters):
            step_down_converter = make_power_converter("step_dn_converter_" + str(i + 1))
            power_sys.converters["step_down"].append(step_down_converter)
        
        # Generatrion Bus 
        gen_bus = make_generation_bus("gen_bus")

        # Batteries
        batteries = make_energy_storage("batteries")


        # Variables
        observables_powered = Variable(
            name="observables_powered",
            value=0.,
            description="Do we have enough power to obtain observables"
        )


    return power_sys