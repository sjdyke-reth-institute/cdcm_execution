#~ovn!
"""Definition of a `Functionality` variable

Author:
    R Murali Krishnan
    
Date:
    03.31.2023
    
"""

from cdcm import *
from typing import Any

class Functionality(Variable):
    """Functionality variable"""

    def __init__(self, *, value: Any = None, units: str = "", track: bool = True, **kwargs) -> None:
        super().__init__(value, units, track, **kwargs)
