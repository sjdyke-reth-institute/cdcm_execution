"""Abstractions helping to define status of operation of a system

Author:
    R Murali Krishnan
    
Date:
    03.24.2023
    
"""

__all__ = ["make_health_status", "DiscreteHealthStatus", "BinaryHealthStatus"]

from typing import Union, Tuple, Optional, Any
from cdcm import *

Scalar = Union[int, float]

class HealthStatus(Variable):
    """Health state"""

    @property
    def support(self) -> Tuple[Scalar, ...]:
        """Get the support of the status variable"""
        return self._support
    
    @support.setter
    def support(self, val) -> None:
        """Set the support of the status variable"""
        self._support = val

    @Variable.value.setter
    def value(self, val) -> None:
        """Set the value of the status variable
        REF: 
         - https://tinyurl.com/3xtf8u64
         - https://tinyurl.com/ywfnhcva
        """
        assert val in self.support
        Variable.value.fset(self, val)


    def __init__(self, 
                 name: str, 
                 support: Tuple[Scalar, ...],
                 **kwargs) -> None:
        self.support = support
        super().__init__(name=name, **kwargs)

class DiscreteHealthStatus(HealthStatus):
    """Discrete health state"""
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class BinaryHealthStatus(DiscreteHealthStatus):
    """Binary health state"""
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name=name, **kwargs)


def make_health_status(
    name: str, 
    value: Union[Scalar, bool],
    support: Tuple[int, ...]=(0, 1),
    units: Optional[str]=None,
    description: Optional[str]=None,
    **kwargs) -> Union[BinaryHealthStatus, DiscreteHealthStatus]:
    """Make a health status variable inferring the type of the variable from
    the provided information
    
    Arguments
    ---------
    name                :   str
        Name of the health status variable
    value:
    """
    HealthStatusConstructor = DiscreteHealthStatus if len(support) > 2 else BinaryHealthStatus

    return HealthStatusConstructor(
        name=name,
        value=value,
        support=support,
        units="" if units is None else units,
        description="" if description is None else description,
        **kwargs
    )