"""
Author: Amir Behjat

Date:
    7/12/2022

Defines the shocksEnvironment interface/type/system/concept.

A `shocksEnvironment` is `System` that exposes the following interface:

variable :: TypeOfVariable

(variable) = optional variable

                                        ___________________
clock            :: Clock          => |                   |
                                      | shocksEnvironment | -> high-current_loads :: Variable
                                      |                   |
design           :: batterySpec    => |___________________|



"""


from cdcm import *
from . import make_current_shock_env_0
from battery_design import *

__all__ = ["make_shocks"]


def make_shocks(
    clock,
    battery_specs,
    make_current_shock_env=make_current_shock_env_0,
):
    """
    Make a shocks system.

    Arguments
    clock -- A clock object measuring time in seconds.
             TODO: Clock should be in Julian time.
    batterySpecs -- For all parameters affecting the system

    """
    with System(name="shocks", description="The shocks system") as shocks:

        current_shock = make_current_shock_env(clock, battery_specs)

    return shocks
