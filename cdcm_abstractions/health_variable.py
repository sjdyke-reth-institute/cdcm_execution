"""Abstractions helping to define status of operation of a system

Author:
    R Murali Krishnan
    
Date:
    03.24.2023
    
"""

__all__ = [
    "HealthVariable", 
    "CategoricalHealthVariable", 
    "BinaryHealthVariable",
    "make_health_variable",
    ]

from typing import Union, Tuple, Optional, Any
from cdcm import *

Scalar = Union[int, float]

class HealthVariable(Variable):
    """Health variable, a variable of the system that indicates the health
    of a system. 

    Their value can be changed as a side-effect of an external event, and/or
    by effect of a parent function node that compute the variable's value 
    based on its grandparent variable nodes.
    """

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
        References: 
         - https://tinyurl.com/3xtf8u64
         - https://tinyurl.com/ywfnhcva
        """
        assert val in self.support
        Variable.value.fset(self, val)


    def __init__(self, 
                 name: str, 
                 support: Tuple[Scalar, ...],
                 idx: Optional[int]=None,
                 **kwargs) -> None:
        self.support = support
        self.idx = idx
        super().__init__(name=name, **kwargs)

class CategoricalHealthVariable(HealthVariable):
    """Discrete health state"""
    def __init__(self, name: str, *, support: Tuple[Scalar, ...]=None, **kwargs) -> None:
        assert support is not None
        super().__init__(name=name, support=support, **kwargs)


class BinaryHealthVariable(CategoricalHealthVariable):
    """Binary health state"""
    def __init__(self, name: str, *, support: Tuple[Scalar, ...], **kwargs) -> None:
        assert len(support) == 2
        super().__init__(name=name, support=support, **kwargs)


class ContinuousHealthVariable(HealthVariable):
    """Continuous health status variable"""
    def __init__(self, name: str, support: Tuple[Scalar, ...], idx: Optional[int] = None, **kwargs) -> None:
        super().__init__(name, support, idx, **kwargs)

def make_health_variable(
    name: str, 
    value: Union[Scalar, bool],
    support: Optional[Tuple[int, ...]]=None,
    units: Optional[str]=None,
    description: Optional[str]=None,
    **kwargs) -> Union[CategoricalHealthVariable, ContinuousHealthVariable]:
    """Make a health variable.
    The sub-type of the variable is determined by the characterizing the 
    `value` and `support`.

    `value` :: float                    => ContinuousHealthVariable
    `value` :: int && len(support) > 2  => DiscreteHealthVariable
    `value` :: int && len(support) ==
    
    Arguments
    ---------
    name                :   str
        Name of the health status variable
    value               :
    """

    if isinstance(value, float):
        HealthVariableConstructor = ContinuousHealthVariable
    elif isinstance(value, int):
        HealthVariableConstructor = BinaryHealthVariable if support is None else CategoricalHealthVariable
    else:
        raise TypeError(f"CDCM cannot infer the type of status variable you are trying to create {type(value)}")

    return HealthVariableConstructor(
        name=name,
        value=value,
        support=(0., 1.) if support is None else support,
        units="" if units is None else units,
        description="" if description is None else description,
        **kwargs
    )