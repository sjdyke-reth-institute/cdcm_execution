#ovn!
"""Digital-twin of MCVT's Power System in `exlang`

Author:
    R Murali Krishnan
    
Date:
    03.27.2023
    
"""

__all__ = ["make_power_converter", "make_batteries"]

from cdcm import *
from cdcm_diagnostics import *

from .types import *
from ..abstractions import *

from typing import Union


POWER_SOURCE_SET = {'S', 'N'}


def make_energy_storage():
    """Make an energy storage"""
    raise NotImplementedError("Implement me..")


def make_power_converter(
        name: str, 
        conv_type: str,
        **kwargs
) -> Union[StepUpConverter, StepDownConverter]:
    """Make a power converter
    
    Arguments:
    ----------
    name        :    str
        Name of the generator
    conv_type    :   str, {'U', 'D'}
        Type of the converter
            U - step-up converter
            D - step-down converter
    
    """

    assert conv_type.upper() in POWER_CONVERTER_SET

    Converter = POWER_CONVERTER_SET[conv_type.upper()]

    with Converter(name=name, **kwargs) as converter:
        status = make_health_status(
            name="status",
            value=0,
            support=(0, 1, 2),
            description="Status of the converter"
        )
    return converter


def make_batteries(name: str, 
                   num_units: int,
                   **kwargs) -> Batteries:
    """Make an energy storage"""
    with maybe_make_system(name, Batteries, **kwargs) as energy_storage:
        status = make_health_status(
            name="status",
            value=[0.] * num_units,
            support=(0, 1, 2),
            description="Status variable of an energy storage system"
        )
    return energy_storage

