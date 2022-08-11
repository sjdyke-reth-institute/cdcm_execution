"""
Author: Amir Behjat

Date:
    7/12/2022


Makes the battery specs system with all its design and fixed parameters.

variable :: TypeOfVariable

(variable) = optional variable

 _________________
|                 |
| batterySpecsEnv | -> battery_specs  :: batterySpecs
|_________________|


"""

import math
import numpy as np

from cdcm import *

__all__ = ["make_battery_specs"]


def make_battery_specs():
    """
    Make a battery specs system. design[A long list of parameters] + All other physical constants that may affect multiple systems.

    Arguments
    - NULL

    """

    with System(name="battery_specs",
                description="The battery_specs system") as battery_specs:

        battery_nominal_max_current = Parameter(
            name="battery_nominal_max_current",
            value=11.0,
            units="A",
            description="The current battery can provide without any health issue (suggested by manufacturer) in living room conditions without extra cooling")
        battery_short_time_max_current = Parameter(
            name="battery_short_time_max_current",
            value=20.0,
            units="A",
            description="The current battery can provide for at most 10 seconds in living room conditions without extra cooling")
        battery_ultimate_max_current = Parameter(
            name="battery_ultimate_max_current",
            value=25.0,
            units="A",
            description="Maximum current battery can have in living room conditions without extra cooling")
        battery_weight = Parameter(
            name="battery_weight",
            value=5.0,
            units="kg",
            description="weight of the battery")  #  Not useful here, will be used for ESM
        battery_dimension = Parameter(
            name="battery_dimension",
            value=[0.4, 0.2, 0.35],
            units="m",
            description="length, width, and height of the battery")  #  Not useful here, will be used for ESM

    return battery_specs
