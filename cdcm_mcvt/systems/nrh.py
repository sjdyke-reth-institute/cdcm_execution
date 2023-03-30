#~ovn!
"""Model of the notional-real habitat in MCVT

Author:
    R Murali Krishnan
    
Date:
    03.30.2023
    
"""


__all__ = ["make_hab"]

from typing import Dict

from cdcm import *

from ..components import *


def make_hab(
        name: str, 
        dt: Node, 
        num_zones: int, 
        spl_properties: Dict, 
        sml_properties: Dict, 
        **kwargs) -> System:
    """Make a habitat model"""

    with System(name=name, **kwargs) as habitat:

        # Make environment control and life support system
        env_control = make_environment_control_system("eclss", dt, num_zones)

        # Make power system
        power_system = make_power_system("power")

        # Make structture
        dome = make_dome_structure("dome", spl_properties, sml_properties)

    return habitat