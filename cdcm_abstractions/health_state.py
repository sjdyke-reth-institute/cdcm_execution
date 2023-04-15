#~ovn!
"""Definitions of a health state variable node

Author:
    R Murali krishnan
    
Date:
    04.15.2023
    
"""


__all__ = [
    "HealthState", 
    "CategoricalHealthState",
    "ContinuousHealthState",
    "make_health_state"
]

from typing import Union, Tuple, Optional
from cdcm import *


Scalar = Union[int, float]

class HealthState(State):
    """Health state, a systems' state that indicates the health of a system.
    
    This variable transitions with Markovian dynamics, or as a side-effect of
    an event.
    """
    def __init__(self, name: str, **kwargs):
        super().__init__(name=name, **kwargs)

class CategoricalHealthState(HealthState):
    """Categorical health state variable"""
    def __init__(self, name: str, **kwargs):
        super().__init__(name=name, **kwargs)

class ContinuousHealthState(HealthState):
    """Continuous health state variable"""
    def __init__(self, name: str, **kwargs):
        super().__init__(name=name, **kwargs)


def make_health_state(
        name: str, 
        value: Union[Scalar, bool],
        units: Optional[str]=None,
        description: Optional[str]=None,
        **kwargs) -> Union[CategoricalHealthState, ContinuousHealthState]:
    """Make a health state"""

    if isinstance(value, int):
        HealthState = CategoricalHealthState
    elif isinstance(value, float):
        HealthState = ContinuousHealthState
    else:
        raise TypeError(f"I am unable to infer the type of the Health State variable {name}")
    
    return HealthState(
        name=name,
        value=value,
        units="" if units is None else units,
        description="" if description is None else description,
        **kwargs)