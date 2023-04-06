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
from functools import reduce, partial
from pprint import pprint

from collections import defaultdict



# Really need a `make_component` pattern in the code
def make_power_converter(name: str, **kwargs) -> PowerConverter:
    """Make power converter system"""
    with maybe_make_system(name, PowerConverter, *kwargs) as converter:
        status_power_converter = make_health_status(
            name="status_power_converter",
            value=0,
            support=(0, 1, 2),
            description="Status variable of the power converter"
        )
        @make_test("test_status_power_converter")
        def fn_test_status_power_converter(s=status_power_converter):
            if s <= 1:
                return 0.
            else:
                return 1.
        
        @make_functionality("func_power_converter")
        def fn_func_power_converter(s=status_power_converter):
            if s <= 1:
                return 0.
            else:
                return 1.

    return converter

def make_energy_storage(name: str, **kwargs) -> EnergyStorage:
    """Make an energy storage system"""
    with maybe_make_system(name, EnergyStorage, **kwargs) as storage:
        status_energy_storage = make_health_status(
            name="status_energy_storage",
            value=0,
            support=(0, 1, 2),
            description="Health status variable of the energy storage"
        )
        @make_test("test_status_energy_storage")
        def fn_test_status_power_converter(s=status_energy_storage):
            if s <= 1:
                return 0.
            else:
                return 1.
        
        @make_functionality("func_energy_storage")
        def fn_func_power_converter(s=status_energy_storage):
            if s <= 1:
                return 0.
            else:
                return 1.
    return storage

def make_batteries(name: str, num_cells: int, **kwargs):
    """Make battery system"""

    with make_energy_storage(name, **kwargs) as batteries:
        status_batteries = make_health_status(
            name="status_batteries",
            value=[0] * num_cells,
            support=(0, 1, 2),
            description="Status of each cell of the battery"
        )
        @make_test("test_status_battery")
        def fn_test_status_power_converter(s=status_batteries):
            if s <= 1:
                return 0.
            else:
                return 1.
        
        @make_functionality("func_battery")
        def fn_func_power_converter(s=status_batteries):
            if s <= 1:
                return 0.
            else:
                return 1.
    return batteries

def make_generation_bus(name: str, **kwargs) -> GenerationBus:
    """Make the generation bus"""

    with maybe_make_system(name, GenerationBus, **kwargs) as bus:
       status_gen_bus = make_health_status(
           name="status_gen_bus",
           value=0,
           support=(0, 1, 2),
           description="Status variable for the generation bus"
        )
       
       @make_test("test_status_gen_bus")
       def fn_test_status_power_converter(s=status_gen_bus):
            if s <= 1:
                return 0.
            else:
                return 1.
            
       @make_functionality("func_gen_bus")
       def fn_func_power_converter(s=status_gen_bus):
            if s <= 1:
                return 0.
            else:
                return 1.
    return bus

def make_power_generator(name: str, **kwargs) -> PowerGenerator:
    """Make the power generator system"""
    with maybe_make_system(name, PowerGenerator, **kwargs) as generator:
        status_power_gen = make_health_status(
            name="status_power_gen",
            value=0,
            support=(0, 1, 2),
            description="Health status variable of the power generator"
        )
        @make_test("test_status_power_gen")
        def fn_test_status_power_converter(s=status_power_gen):
            if s <= 1:
                return 0.
            else:
                return 1.
        
        @make_functionality("func_power_gen")
        def fn_func_power_converter(s=status_power_gen):
            if s <= 1:
                return 0.
            else:
                return 1.
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
        @make_test("test_status_dust")
        def fn_test_status_dust(s=status_dust):
            """Status of dust"""
            if s <= 1:
                return 0.
            else:
                return 1.

        status_paint = make_health_status(
            name="status_paint",
            value=0,
            support=(0, 1, 2),
            description="Health status variable indicating the paint degradation to the generator panels"
        )
        @make_test("test_status_paint")
        def fn_test_status_pain(s=status_paint):
            if s <= 1:
                return 0.
            else:
                return 1.
            
        coolant_leak = Variable(
            name="coolant_leak",
            value=0.,
            description="Leak in the coolant"
        )
            
        @make_functionality("func_nuclear_power_gen")
        def fn_func_nuclear_power_gen(cl=coolant_leak, sd=status_dust, sp=status_paint):
            """Functionality of nuclear power generation"""
            if cl > 0.:
                return 0.
            else:
                return sd * sp

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
        @make_test("test_status_dust")
        def fn_test_status_dust(s=status_dust):
            """Status of dust"""
            if s <= 1:
                return 0.
            else:
                return 1.

        status_mechanical = make_health_status(
            name="status_mechanical",
            value=0,
            support=(0, 1, 2),
            description="Health status indicating the mechanical health status of solar arrays"
        )
        @make_test("test_status_mechanical")
        def fn_test_status_mechanical(s=status_mechanical):
            """Status of dust"""
            if s <= 1:
                return 0.
            else:
                return 1.
            
        @make_functionality("func_solar_arrays")
        def fn_func_solar_arrays(sd=status_dust, sm=status_mechanical):
            """Procedure to calculate the functionality of arrays"""
            return sd * sm

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

        power_produce = Variable(
            name="power_produce",
            value=0.,
            description="Total power produced"
        )
        @make_function(power_produce)
        def fn_calc_power_produce(
            fs=solar.func_solar_arrays, 
            fn=nuclear.func_nuclear_power_gen):
            """Total power produced as a function of source functionalities"""
            return fs * 100. + fn * 200
            

        # Step-up converters
        step_up_converters = []
        for i in range(num_step_up_converters):
            step_up_converter = make_power_converter("step_up_converter_" + str(i + 1))
            step_up_converters.append(step_up_converter)

        # Step-down converters
        step_dn_converters = []
        for i in range(num_step_dn_converters):
            step_down_converter = make_power_converter("step_dn_converter_" + str(i + 1))
            step_dn_converters.append(step_down_converter)

        
        # Generatrion Bus 
        gen_bus = make_generation_bus("gen_bus")


        step_up_converter_statuses = [suc.status_power_converter for suc in step_up_converters] 
        step_dn_converter_statuses = [sdc.status_power_converter for sdc in step_dn_converters]

        func_power_flow = Functionality(
            name="func_power_flow",
            value=0.,
            description="Functionality of power flow"
        )

        func_parents = step_up_converter_statuses + step_dn_converter_statuses + [gen_bus.func_gen_bus]

        # Good candidate for a `reduce_product` pattern
        reduce_prod = partial(lambda func, init, *iterable: reduce(func, iterable, init), 
                              lambda a, b: a * b, 1.)

        fn_func_power_flow = Function(
            name="fn_func_power_flow",
            parents=func_parents,
            children=func_power_flow,
            func=reduce_prod,
            description="Procedure that calculate the power flow through"
        )

    return power_sys