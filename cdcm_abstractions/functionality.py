#~ovn!
"""Definition of a `Functionality` variable

Author:
    R Murali Krishnan
    
Date:
    03.31.2023
    
"""

from cdcm import *
from typing import Any, Union

Scalar = Union[int, float]

class Functionality(Variable):
    """Functionality variable"""
    def __init__(self, name: str, value: Any = None, units: str = "", track: bool = True, **kwargs) -> None:
        super().__init__(name=name, value=value, units=units, track=track, **kwargs)

class BinaryFunctionality(Functionality):
    """Binary functionality variable"""
    def __init__(self, name: str, value: Any = None, units: str = "", track: bool = True, **kwargs) -> None:
        super().__init__(name=name, value=value, units=units, track=track, **kwargs)
