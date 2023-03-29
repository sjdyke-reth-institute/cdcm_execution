#ovn!
"""Digital-twin of MCVT's Power System in `exlang`

Author:
    R Murali Krishnan
    
Date:
    03.27.2023
    
"""

__all__ = ["make_generator", "make_batteries"]

from cdcm import *
from cdcm_diagnostics import *

from .types import *
from ..abstractions import *

from typing import Union


GENERATOR_SET = {'U', 'D'}
SOURCE_SET = {'S', 'N'}


def make_generator(
        name: str, 
        gen_type: str,
        **kwargs
) -> Union[StepUpConverter, StepDownConverter]:
    """Make a generator
    
    Arguments:
    ----------
    name        :    str
        Name of the generator
    gen_type    :   str, {'U', 'D'}
        Type of the generator
    """
    _gen_type = gen_type.upper()

    assert _gen_type in GENERATOR_SET

    Converter = StepUpConverter if _gen_type == 'U' else StepDownConverter

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

