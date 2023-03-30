#~ovn!
"""Model of the notional-real habitat in MCVT

Author:
    R Murali Krishnan
    
Date:
    03.30.2023
    
"""


__all__ = ["make_habitat"]

from cdcm import *

from .components import *


def make_habitat(name: str, **kwargs):
    """Make a habitat model"""

    with System(name=name, **kwargs) as habitat:
        pass

    return habitat